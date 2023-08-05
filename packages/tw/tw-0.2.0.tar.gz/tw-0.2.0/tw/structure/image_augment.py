# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import random
import skimage
import numpy as np
import imgaug as ia
from .image_collect import ImageCollect


class ImageAugment():
  """We expected a augmentar which could boost the samples together with labels
    such as bounding box, segmentation and keypoint.

  # support landmark
  - images: [H, W, C]
  - segms: [H, W]
  - bbox: [x1, y1, x2, y2]
  - keypoint: ...
  - heatmap: ...

  # support augmentation
  """

  def __init__(self, transform):
    # self.transform = transform
    self.aug = transform

  @staticmethod
  def resize_aspect(img_h, img_w, min_sizes, max_sizes):
    if not isinstance(min_sizes, list):
      min_sizes = [min_sizes]
    if not isinstance(max_sizes, list):
      max_sizes = [max_sizes]
    # short edge resize
    max_size = max_sizes[0]
    min_size = random.choice(min_sizes)
    if max_size is not None:
      min_original = float(min((img_w, img_h)))
      max_original = float(max((img_w, img_h)))
      if max_original / min_original * min_size > max_size:
        min_size = int(round(max_size * min_original / max_original))
    if (img_w <= img_h and img_w == min_size) or \
       (img_h <= img_w and img_h == min_size):
      pass
    elif img_w < img_h:
      new_h = int(min_size * img_h / img_w)
      new_w = min_size
    else:
      new_w = int(min_size * img_w / img_h)
      new_h = min_size
    return new_h, new_w

  @staticmethod
  def resize_with_pad(img, img_h, img_w):
    """aspect to a fixed size, and other part to padding zero
    Arguments:
      img: numpy.ndarray(h, w, c)
      img_h: output height of image
      img_w: output width of image

    Returns:
      a numpy.ndarray(img_h, img_w, c)
    """
    h, w, c = img.shape
    dim_diff = np.abs(h - w)
    # Upper (left) and lower (right) padding
    pad1, pad2 = dim_diff // 2, dim_diff - dim_diff // 2
    # Determine padding
    pad = ((pad1, pad2), (0, 0), (0, 0)) if h <= w else (
        (0, 0), (pad1, pad2), (0, 0))
    # Add padding
    img = np.pad(img, pad, 'constant', constant_values=127.5) / 255.
    # Resize and normalize
    img = skimage.transform.resize(img, (img_h, img_w, c), mode='reflect')
    # return
    return img

  def augment_bboxes(self, bboxes, img_h, img_w, det=None):
    """det is a self.aug.to_deterministic()
    """
    if det is None:
      det = self.aug.to_deterministic()

    # construct ia bounding box class
    ia_bbs = [ia.BoundingBox(*bbox, label=i) for i, bbox in enumerate(bboxes)]

    # sticky on image
    ia_bbs_img = ia.BoundingBoxesOnImage(ia_bbs, (img_h, img_w))

    # augment
    aug_bbs = det.augment_bounding_boxes(ia_bbs_img)

    # remove out exterior
    refine_bbs = aug_bbs.remove_out_of_image(
        fully=True, partly=False).clip_out_of_image()

    # new idx
    bbs_idx = [bbox.label for bbox in refine_bbs.bounding_boxes]
    bbs_list = refine_bbs.to_xyxy_array().tolist()

    # bbs_idx e.g. [0, 1, 3, 5, 6]
    return bbs_list, bbs_idx

  def augment_segms(self):
    # add
    image_segms = [ia.SegmentationMapOnImage(
        segm, segm.shape, 2) for i, segm in enumerate(segms)]

    # transform
    aug_segms = [det.augment_segmentation_maps(segm).get_arr_int()
                 for segm in image_segms]
    ret.append(aug_segms)

  def augment_polygons(self, polygons, img_h, img_w, det=None):
    if det is None:
      det = self.aug.to_deterministic()

    # construct ia polygons
    ia_pgs = []
    for p in polygons:
      ia_pgs.append(ia.Polygon([i for i in zip(p[0][::2], p[0][1::2])]))

    # stick on image
    ia_pgs_img = ia.PolygonsOnImage(ia_pgs, shape=(img_h, img_w))
    aug_pgs = det.augment_polygons(ia_pgs_img).polygons

    # return
    pgs_list = [[p.exterior.reshape([-1]).tolist()] for p in aug_pgs]
    return pgs_list

  def augment_collect(self, collect: ImageCollect):
    """Return an agumented collect"""
    ret = ImageCollect(collect.img_id, collect.path)
    det = self.aug.to_deterministic()

    # augment and assign to ret
    h, w = collect.image_size()
    img = ret.assign_image(det.augment_image(collect.image()))

    # augment bbox
    if collect.has_bboxes():
      bboxes_list, bboxes_idx = self.augment_bboxes(
          collect.bboxes('xyxy'), h, w, det)
    else:
      bboxes_idx = None
      bboxes_list = None

    # filter labels
    if collect.has_labels():
      labels = collect.labels()
      if bboxes_idx is not None:
        labels = [labels[i] for i in bboxes_idx]
    else:
      labels = None

    # augment masks
    if collect.has_segms():
      if collect._segms[0].mode == 'polygon':
        segms = self.augment_polygons(collect.segms('polygon'), h, w, det)
        segms_mode = 'polygon'
      elif collect._segms[0].mode == 'binary':
        segms = self.augment_segms(collect.segms('binary'), h, w, det)
        segms_mode = 'binary'
      else:
        raise NotImplementedError
      if bboxes_idx is not None:
        segms = [segms[i] for i in bboxes_idx]
    else:
      segms = None
      segms_mode = None

    if collect.has_heatmaps():
      raise NotImplementedError

    if collect.has_kps():
      raise NotImplementedError

    ret.adds(bboxes=bboxes_list, bbox_mode='xyxy',
             segms=segms, segm_mode=segms_mode,
             labels=labels)

    return ret
