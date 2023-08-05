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
"""Bounding Box
"""
import torch
from .extend import Extend


class BoxList(Extend):
  def __init__(self, bbox, size, mode="xyxy"):
    """ The BoxList is binding in a single image
    Arguments:
      bbox: a [N, 4] tensor
      size: [width, height] represent image size
      mode: "xyxy", "xywh", "centered_xywh"
        "xyxy": left top, right bottom
        "xywh": center point, width, height
      normalized: true for normalized to [0, 1] cooradinate in terms of
        image width and height
    """
    super(BoxList, self).__init__()
    assert len(size) == 2
    assert bbox.ndimension() == 2
    assert bbox.size(-1) == 4  # 4 elements
    assert mode in ["xyxy", "xywh"]
    # xywh -> xyxy
    if mode == 'xywh':
      xmin, ymin, w, h = bbox.split(1, dim=-1)
      bbox = torch.cat((xmin,
                        ymin,
                        xmin + (w - 1).clamp(min=0),
                        ymin + (h - 1).clamp(min=0)), dim=-1)
      mode = 'xyxy'

    # set
    self.size = size
    self.bbox = bbox
    self.mode = mode
    self.extra = {}

  def __len__(self):
    return self.bbox.size(0)

  def __repr__(self):
    s = self.__class__.__name__ + "("
    s += "num={}, ".format(len(self))
    s += "mode={}, ".format(self.mode)
    s += "w={}, ".format(self.size[0])
    s += "h={}, ".format(self.size[1])
    s += "field=({})".format(', '.join([key for key in self.extra]))
    return s

  def __getitem__(self, item):
    """slice for list
    """
    bbox = BoxList(self.bbox[item], self.size, self.mode)
    for k, v in self.extra.items():
      bbox.add_field(k, v[item])
    return bbox

  def convert(self, mode):
    if self.mode == mode:
      return self
    raise NotImplementedError

  def to(self, *args, **kwargs):
    self.bbox = self.bbox.to(*args, **kwargs)
    for key in self.extra:
      if isinstance(self.extra[key], torch.Tensor):
        self.extra[key] = self.extra[key].to(*args, **kwargs)
    return self

  def transpose(self, method):
    """
    Transpose bounding box (flip or rotate in 90 degree steps)
    :param method: One of :py:attr:`PIL.Image.FLIP_LEFT_RIGHT`,
      :py:attr:`PIL.Image.FLIP_TOP_BOTTOM`, :py:attr:`PIL.Image.ROTATE_90`,
      :py:attr:`PIL.Image.ROTATE_180`, :py:attr:`PIL.Image.ROTATE_270`,
      :py:attr:`PIL.Image.TRANSPOSE` or :py:attr:`PIL.Image.TRANSVERSE`.
    """
    if method not in ('FLIP_LEFT_RIGHT', 'FLIP_TOP_BOTTOM'):
      raise NotImplementedError(
          "Only FLIP_LEFT_RIGHT and FLIP_TOP_BOTTOM implemented")
    image_width, image_height = self.size
    xmin, ymin, xmax, ymax = self.bbox.split(1, dim=-1)
    if method == 'FLIP_LEFT_RIGHT':
      transposed_xmin = image_width - xmax - 1
      transposed_xmax = image_width - xmin - 1
      transposed_ymin = ymin
      transposed_ymax = ymax
    elif method == 'FLIP_TOP_BOTTOM':
      transposed_xmin = xmin
      transposed_xmax = xmax
      transposed_ymin = image_height - ymax
      transposed_ymax = image_height - ymin
    transposed_boxes = torch.cat(
        (transposed_xmin,
         transposed_ymin,
         transposed_xmax,
         transposed_ymax), dim=-1)
    bbox = BoxList(transposed_boxes, self.size, mode="xyxy")
    for k, v in self.extra.items():
      if not isinstance(v, torch.Tensor):
        v = v.transpose(method)
      bbox.add_field(k, v)
    return bbox

  def resize(self, size, *args, **kwargs):
    """Resize bbox to target size
      target_shape: a tuple with (width, height)
    """
    assert self.mode == "xyxy"

    ratio_w = float(size[0])/self.size[0]
    ratio_h = float(size[1])/self.size[1]

    # square
    if ratio_w == ratio_h:
      scaled_box = self.bbox * ratio_w
      bbox = BoxList(scaled_box, (size[0], size[1]), self.mode)
      for k, v in self.extra.items():
        if not isinstance(v, torch.Tensor):
          v = v.resize(size, *args, **kwargs)
        bbox.add_field(k, v)
      return bbox

    # rect
    scaled_box = torch.stack(
        (self.bbox[:, 0] * ratio_w,
         self.bbox[:, 1] * ratio_h,
         self.bbox[:, 2] * ratio_w,
         self.bbox[:, 3] * ratio_h), dim=1)
    scaled_box = scaled_box.view(-1, 4)
    bbox = BoxList(scaled_box, (size[0], size[1]), self.mode)

    # for extra fields
    for k, v in self.extra.items():
      if not isinstance(v, torch.Tensor):
        v = v.resize(size, *args, **kwargs)
      bbox.add_field(k, v)

    return bbox

  def crop(self, box):
    """Cropss a rectangular region from this bounding box. The box is a 4-tuple
      defining the left, upper, right, and lower pixel coordinate.
    """
    xmin, ymin, xmax, ymax = self.bbox.split(1, dim=-1)
    w, h = box[2] - box[0], box[3] - box[1]
    cropped_xmin = (xmin - box[0]).clamp(min=0, max=w)
    cropped_ymin = (ymin - box[1]).clamp(min=0, max=h)
    cropped_xmax = (xmax - box[0]).clamp(min=0, max=w)
    cropped_ymax = (ymax - box[1]).clamp(min=0, max=h)

    # # TODO should I filter empty boxes here?
    # is_empty = (cropped_xmin == cropped_xmax) | (cropped_ymin == cropped_ymax)

    cropped_box = torch.cat(
        (cropped_xmin, cropped_ymin, cropped_xmax, cropped_ymax), dim=-1)
    bbox = BoxList(cropped_box, (w, h), mode="xyxy")
    for k, v in self.extra.items():
      if not isinstance(v, torch.Tensor):
        v = v.crop(box)
      bbox.add_field(k, v)
    return bbox

  def add_field(self, key, value):
    self.extra[key] = value

  def field(self, key):
    return self.extra[key]

  def has_field(self, key):
    return key in self.extra

  def area(self):
    """Return area for each bbox
    """
    box = self.bbox
    if self.mode == "xyxy":
      area = (box[:, 2]-box[:, 0] + 1) * (box[:, 3] - box[:, 1] + 1)
    else:
      raise NotImplementedError
    return area

  def copy(self):
    """Return a duplicate includes all"""
    bbox = BoxList(self.bbox, self.size, self.mode)
    for k, v in self.extra.items():
      bbox.add_field(k, v)
    return bbox

  def copy_with_fields(self, fields, skip_missing=False):
    """Return a duplicate with specified fields"""
    bbox = BoxList(self.bbox, self.size, self.mode)
    if not isinstance(fields, (list, tuple)):
      fields = [fields]
    for field in fields:
      if self.has_field(field):
        bbox.add_field(field, self.field(field))
      elif not skip_missing:
        raise KeyError(
            "Field '{}' not found in {}".format(field, self))
    return bbox

  def assign(self, boxlist):
    """assign all by another boxlist"""
    for k, v in boxlist.extra.items():
      self.add_field(k, v)

  def clamp_to_image(self, remove_empty=True):
    if self.mode == 'xyxy':
      self.bbox[:, 0].clamp_(min=0, max=self.size[0] - 1)
      self.bbox[:, 1].clamp_(min=0, max=self.size[1] - 1)
      self.bbox[:, 2].clamp_(min=0, max=self.size[0] - 1)
      self.bbox[:, 3].clamp_(min=0, max=self.size[1] - 1)
      if remove_empty:
        return self[(self.bbox[:, 3] > self.bbox[:, 1]) &
                    (self.bbox[:, 3] > self.bbox[:, 0])]
      return self
    raise "Not support for non-xyxy mode."

  def filter_small_boxes(self, min_size):
    """Only keep boxes with both sides >= min_size
    Arguments:
      boxlist: (Boxlist)
      min_size: (int)
    """
    x1, y1, x2, y2 = self.bbox.unbind(dim=1)
    keep = (x2 - x1 + 1 >= min_size) & (y2 - y1 + 1 >= min_size)
    self.bbox = self.bbox[keep.nonzero().squeeze(1)]

  @staticmethod
  def concat(list_of_boxlist):
    """
    Arguments:
      list_of_boxlist: (Boxlist [N, 4], Boxlist [M, 4], ...)

    Returns:
      merged_boxlist: (BoxList [N+M, 4])
    """
    bbox_list = []
    extra = {}
    for i, boxlist in enumerate(list_of_boxlist):
      if i == 0:
        mode = boxlist.mode
        size = boxlist.size
        bbox = boxlist.bbox
        extra_keys = boxlist.extra.keys()
        for key in extra_keys:
          extra[key] = []
      else:
        assert mode == boxlist.mode
        assert size == boxlist.size
        assert extra_keys == boxlist.extra.keys()
      # append
      bbox_list.append(boxlist.bbox)
      for key in extra_keys:
        extra[key].append(boxlist.field(key))

    # add into
    merged_boxlist = BoxList(torch.cat(bbox_list), size, mode)
    for key in extra:
      merged_boxlist.add_field(key, torch.cat(extra[key]))
    return merged_boxlist

  @staticmethod
  def iou(boxlist1, boxlist2):
    """Compute the intersection over union of two set of boxes.
    Arguments:
      box1: (BoxList) bounding boxes, sized [N,4].
      box2: (BoxList) bounding boxes, sized [M,4].

    Returns:
      (tensor) iou, sized [N, M].
    """
    if boxlist1.size != boxlist2.size:
      raise RuntimeError("unequalled size {}, {}".format(boxlist1, boxlist2))
    assert boxlist1.mode == boxlist2.mode
    N = len(boxlist1)
    M = len(boxlist2)
    area1 = boxlist1.area()
    area2 = boxlist2.area()
    box1, box2 = boxlist1.bbox, boxlist2.bbox
    lt = torch.max(box1[:, None, :2], box2[:, :2])  # [N,M,2]
    rb = torch.min(box1[:, None, 2:], box2[:, 2:])  # [N,M,2]
    wh = (rb - lt + 1).clamp(min=0)  # [N,M,2]
    inter = wh[:, :, 0] * wh[:, :, 1]  # [N,M]
    iou = inter / (area1[:, None] + area2 - inter)
    return iou
