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
"""Mask Converter
  Manage mask and feeding to network.
1) Mask Format
- binary image (as a segment of a whole iamge)
- polygon: [x1, y1, x2, y2, x3, y3, ...]
- rle: encoded format.
2) To: From a kind of mask format to another
3) Vis: visualization mask
"""
import cv2
import skimage
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pycocotools import mask as cocomask


class MaskConverter():
  def __init__(self, src_mode, dst_mode):
    # check
    assert src_mode in ['binary', 'polygon', 'rle']
    assert dst_mode in ['binary', 'polygon', 'rle']

    # mode
    self.src_mode = src_mode
    self.dst_mode = dst_mode
    self.converter = None

    # select func
    if self.src_mode == 'binary' and self.dst_mode == 'polygon':
      self.converter = self.convert_binary_to_polygon
    elif self.src_mode == 'polygon' and self.dst_mode == 'binary':
      self.converter = self.convert_polygon_to_binary
    else:
      raise NotImplementedError(src_mode, dst_mode)

  def __call__(self, mask, **kwargs):
    return self.converter(mask, **kwargs)

  def convert_binary_to_polygon(self, mask):
    """Convert mask to Polygon format.
    Inputs:
      Mask with shape [h, w] (for whole image) and filled with binary data.
        or mask is a 'str' it will as image loaded.
    PS:
      Polygons is not coco format (segm).
    Returns:
      polygon: [x, y, x, y, x, y]
      bbox: corresponding [xywh] -> left top xy, w and h in pixels
      area: areas in pixels
    """
    # if mask represent a path
    if isinstance(mask, str):
      mask = skimage.io.imread(mask)

    assert isinstance(mask, np.ndarray)
    assert len(mask.shape) == 2

    polygons = []
    encoded_mask = cocomask.encode(np.asfortranarray(np.uint8(mask)))
    area = cocomask.area(encoded_mask)
    bbox = cocomask.toBbox(encoded_mask).tolist()
    contours, hierarchy = cv2.findContours(
        (mask).astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # overflow
    if len(contours) == 0:
      return None, None, None

    # general
    polygons = [list(np.reshape(contours[0], [-1]))]

    # too small
    if len(polygons[0]) <= 8:
      return None, None, None

    return polygons, bbox, area

  def convert_polygon_to_binary(self, polygons, img_h, img_w):
    if isinstance(polygons, list):
      # polygons -- a single object might consist of multiple parts
      # we merge all parts into one mask rle code
      rles = cocomask.frPyObjects(polygons, img_h, img_w)
      rle = cocomask.merge(rles)
    elif isinstance(polygons['counts'], list):
      # uncompressed RLE
      rle = cocomask.frPyObjects(polygons, img_h, img_w)
    else:
      # rle
      rle = polygons
    # binary like format
    return cocomask.decode(rle)


if __name__ == "__main__":
  converter = MaskConverter('binary', 'polygon')
  mask = skimage.io.imread('asserts/mask.png')
  polygon, bbox, area = converter(mask)

  # original mask
  plt.subplot(121)
  plt.imshow(mask)
  plt.gca().add_patch(matplotlib.patches.Rectangle(
      (bbox[0], bbox[1]), bbox[2], bbox[3],
      linewidth=1, edgecolor='r', facecolor='none'))
  plt.title('original')
  plt.axis('off')

  # mask->segm->mask
  plt.subplot(122)
  new_mask = converter.convert_polygon_to_binary(
      polygon, mask.shape[0], mask.shape[1])
  plt.imshow(new_mask)
  plt.gca().add_patch(matplotlib.patches.Rectangle(
      (bbox[0], bbox[1]), bbox[2], bbox[3],
      linewidth=1, edgecolor='r', facecolor='none'))
  plt.title('mask->polygon->mask')
  plt.axis('off')
  plt.show()

  print(polygon)
