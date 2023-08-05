# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
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
"""Image Collections
 For a image collect, it should include a series of
 - image
 - object
  - bounding box
  - segmentation
  - keypoint
 - heatmap
"""
import collections
import cv2
from .mask_converter import MaskConverter


class _Meta():
  def __init__(self, value=None, mode=None):
    self.value = value
    self.mode = mode


class ImageCollect():
  def __init__(self, img_id, path=None, load=False, toRGB=False):
    """Image Collect is a helper to manage the image resource and
      prepare for training or inference by union format.

      We design for each meta has own dictionary, for it is possible for that
      some objects have bboxes but no segms.
    """
    # corresponding dataset idx
    self._id = img_id
    self._path = path
    # image numpy array [H, W, C]
    self._image = None
    self._image = self.image(toRGB) if load else None
    # bounding box
    self._bboxes = collections.OrderedDict()
    # mask
    self._segms = collections.OrderedDict()
    self._segms_b2p = MaskConverter('binary', 'polygon')
    self._segms_p2b = MaskConverter('polygon', 'binary')
    # kps
    self._kps = collections.OrderedDict()
    # heatmap
    self._heatmaps = collections.OrderedDict()
    # labels
    self._labels = collections.OrderedDict()
    # counts
    self._count = 0
    self._metas = [self._bboxes, self._segms, self._kps, self._labels]

  def __len__(self):
    return self._count

  @property
  def img_id(self):
    return self._id

  @property
  def path(self):
    return self._path

  def assert_same(self):
    """assert input should have same number of object"""
    assert len(set([(isinstance(arg, list), len(arg))
                    for arg in self._metas if len(arg) != 0])) == 1

  def add_bbox(self, idx, bbox, mode='xyxy'):
    assert mode in ['xyxy', 'xywh']
    if idx in self._bboxes:
      raise IndexError(idx)
    self._bboxes[idx] = _Meta(bbox, mode)

  def bboxes(self, mode):
    """we allow to convert another mode, and return a list."""
    assert mode in ['xyxy', 'xywh']
    rets = []
    for _, bbox in self._bboxes.items():
      v = bbox.value
      if bbox.mode == mode:
        rets.append(v)
      elif bbox.mode == 'xyxy' and mode == 'xywh':
        rets.append([v[0], v[1], v[2]-v[0]+1, v[3]-v[1]+1])
      elif bbox.mode == 'xywh' and mode == 'xyxy':
        rets.append([v[0], v[1], v[2]+v[0]-1, v[3]+v[1]-1])
    return rets

  def has_bboxes(self):
    return True if len(self._bboxes) else False

  def add_segm(self, idx, segm, mode='polygon'):
    assert mode in ['polygon', 'binary']
    if idx in self._segms:
      raise IndexError(idx)
    self._segms[idx] = _Meta(segm, mode)

  def segms(self, mode):
    assert mode in ['polygon', 'binary']
    rets = []
    for _, segm in self._segms.items():
      v = segm.value
      if segm.mode == mode:
        rets.append(v)
      elif segm.mode == 'binary' and mode == 'polygon':
        rets.append(self._segms_b2p(v))
      elif segm.mode == 'polygon' and mode == 'binary':
        h, w = self.image_size()
        rets.append(self._segms_p2b(v, img_h=h, img_w=w))
    return rets

  def has_segms(self):
    return True if len(self._segms) else False

  def add_kps(self, idx, kps, mode=None):
    if idx in self._kps:
      raise IndexError(idx)
    self._kps[idx] = _Meta(kps, mode)

  def has_kps(self):
    return True if len(self._kps) else False

  def add_heatmap(self, idx, heatmap, mode=None):
    if idx in self._heatmaps:
      raise IndexError(idx)
    self._heatmaps[idx] = _Meta(heatmap, mode)

  def has_heatmaps(self):
    return True if len(self._heatmaps) else False

  def add_label(self, idx, label, mode=None):
    if idx in self._labels:
      raise IndexError(idx)
    self._labels[idx] = _Meta(label, mode)

  def has_labels(self):
    return True if len(self._labels) else False

  def labels(self, mode=None):
    return [label.value for _, label in self._labels.items()]

  def image_size(self):
    return self._image.shape[:2]

  def image(self, toRGB=False):
    """If image not been loaded, it could be loaded now"""
    if self._image is None:
      self._image = cv2.imread(self._path)
    if toRGB:
      self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2RGB)
    return self._image

  def assign_image(self, image):
    """Directly assgin image from external"""
    if self._image is None:
      self._image = image
    else:
      raise "Image had loaded."
    return self._image

  def add(self, bbox=None, bbox_mode='xyxy',
          segm=None, segm_mode='polygon',
          kps=None, kps_mode=None,
          heatmap=None, heatmap_mode=None,
          label=None, label_mode=None):
    # add bbox
    if bbox is not None:
      self.add_bbox(self._count, bbox, bbox_mode)
    # add segm
    if segm is not None:
      self.add_segm(self._count, segm, segm_mode)
    # add kps
    if kps is not None:
      self.add_kps(self._count, kps, kps_mode)
    # add label
    if label is not None:
      self.add_label(self._count, label, label_mode)
    # add heatmap
    if heatmap is not None:
      self.add_heatmap(self._count, heatmap, heatmap_mode)
    self._count += 1

  def adds(self, bboxes=None, bbox_mode='xyxy',
           segms=None, segm_mode='polygon',
           kps=None, kps_mode=None,
           heatmaps=None, heatmap_mode=None,
           labels=None, label_mode=None):
    """batch add"""
    # add bbox
    counts = []

    if bboxes is not None:
      for i, bbox in enumerate(bboxes):
        self.add_bbox(self._count + i, bbox, bbox_mode)
      counts.append(len(bboxes))

    # add segm
    if segms is not None:
      for i, segm in enumerate(segms):
        self.add_segm(self._count + i, segm, segm_mode)
      counts.append(len(segms))

    # add kps
    if kps is not None:
      for i, kp in enumerate(kps):
        self.add_kps(self._count + i, kp, kps_mode)
      counts.append(len(kps))

    # add label
    if labels is not None:
      for i, label in enumerate(labels):
        self.add_label(self._count + i, label, label_mode)
      counts.append(len(labels))

    # add heatmap
    if heatmaps is not None:
      for i, heatmap in enumerate(heatmaps):
        self.add_heatmap(self._count + i, heatmap, heatmap_mode)
      counts.append(len(heatmaps))

    # make sure all number is identical
    assert len(set(counts)) == 1
    self._count += counts[0]
