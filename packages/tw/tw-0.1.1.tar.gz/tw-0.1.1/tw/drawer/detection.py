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
"""Drawer for keypoint, detection, mask
"""
import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
from tw.structure import BoxList


class DrawDet():
  def __init__(self):
    """A drawer could support bbox, mask, kps, heatmap and labels from BoxList.

    Returns:
       A numpy-like image with box and mask
    """
    # draw label
    self._with_label = False
    self._names = None
    self._font_size = 12
    self._offset = 0

    # draw bbox
    self._with_bbox = False
    self._box_thick = 2

    # draw mask
    self._with_mask = False
    self._mask_alpha = 0.5
    self._mask_thick = 2

    # draw kps
    self._with_kps = False

    # draw heatmap
    self._with_heatmap = False

    # draw scale
    self._scale = True
    self._scale_size = 800.0

  @staticmethod
  def _alpha(color, alpha):
    assert len(color) == 3
    return [(1-alpha)*color[0] + alpha * 255,
            (1-alpha)*color[1] + alpha * 255,
            (1-alpha)*color[2] + alpha * 255]

  @staticmethod
  def _random_colors(N):
    np.random.seed(1)
    colors = [tuple((255*np.random.rand(3)).astype(np.int)) for _ in range(N)]
    return colors

  @staticmethod
  def _apply_mask(image, mask, color, alpha=0.5):
    for n, c in enumerate(color):
      image[:, :, n] = np.where(mask[:, :, 0] == 1,
                                image[:, :, n] * (1 - alpha) + alpha * c,
                                image[:, :, n])
    return image

  def set_bbox(self, thick=2):
    self._with_bbox = True
    self._box_thick = thick
    return self

  def _draw_bbox(self, image, bbox, color):
    x1, y1, x2, y2 = bbox
    image = cv2.rectangle(
        image, (x1, y1), (x2, y2), self._alpha(color, 0.1), self._box_thick)
    return image

  def set_mask(self, alpha=0.5, thick=2):
    self._with_mask = True
    self._mask_alpha = alpha
    self._mask_thick = thick
    return self

  def _draw_mask(self, image, mask, color):
    """mask should has same size with image"""
    image = self._apply_mask(image, mask, color, self._mask_alpha)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image = cv2.drawContours(
        image, contours, -1, self._alpha(color, 0.0), self._mask_thick)
    return image

  def set_kps(self):
    self._with_kps = True
    return self

  def _draw_kps(self, image):
    raise NotImplementedError

  def set_heatmap(self):
    self._with_heatmap = True
    return self

  def _draw_heatmap(self, image):
    raise NotImplementedError

  def set_label(self, size=10, offset=0, names=None):
    self._with_label = True
    self._font_size = size
    self._offset = offset
    self._names = names
    return self

  def _draw_label(self, image, x, y, color, label=None, score=None):
    if label is None:
      caption = '{}'.format(score)
    else:
      name = self._names[int(label + self._offset)]
      caption = '{}'.format(name) \
          if score is None else '{}: {:.2f}'.format(name, score)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Ubuntu-B.ttf', self._font_size)
    w, h = font.getsize(caption)
    draw.rectangle((x, y, x + w, y - h),
                   fill=(color[2], color[1], color[0]))
    draw.text((x, y-h-1), caption, font=font, fill='white')
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image

  def __call__(self,
               image,  # [H, W, C]
               boxlist: BoxList,
               conf=0.45,  # filter low bbox
               is_show=False,
               is_save=False,
               save_path=None):

    # aspect resize by short edge to 1024
    h, w, c = image.shape
    if self._scale:
      ratio = self._scale_size / h if h < w else self._scale_size / w
      (w, h) = (int(w * ratio), int(h * ratio))
      image = cv2.resize(image, (w, h), interpolation=cv2.INTER_CUBIC)

    # resize pred bbox to image size
    boxlist = boxlist.resize((w, h))

    # filter small conf objects
    if conf is not None:
      scores = boxlist.field("scores")
      boxlist = boxlist[torch.nonzero(scores > conf).squeeze(1)]
      scores = boxlist.field("scores").cpu().numpy()

    # to numpy
    if self._with_bbox:
      bboxes = boxlist.bbox.cpu().numpy()
    if self._with_label:
      labels = boxlist.field("labels").cpu().numpy()
    if self._with_mask:
      masks = [mask[:, :, None].numpy()
               for mask in self._mask_projector(boxlist)]

    # make unique color for categories
    classes = np.unique(labels)
    colors = self._random_colors(len(classes))
    cls_to_color = {label: colors[idx] for idx, label in enumerate(classes)}

    # draw each objects
    for i, label in enumerate(labels):
      # get color
      color = cls_to_color[label]
      # draw label
      if self._with_label:
        score = 1.0 if conf is None else scores[i]
        image = self._draw_label(image, bboxes[i], label, score, color)
      # draw bbox
      if self._with_bbox:
        image = self._draw_bbox(image, bboxes[i], color)
      # draw mask
      if self._with_mask:
        image = self._draw_mask(image, masks[i], color)

    if is_show:
      cv2.imshow('det', image)
      cv2.waitKey(0)

    if is_save and save_path is not None:
      cv2.imwrite(save_path, image)

    return image
