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
import torch
import torch.nn.functional as F


class MaskProjector():
  """Mask Projector
  Arguments:
      masks: extra["masks"] [N, 1, 28, 28]
      boxes: BoxList(with img_h, img_w)

  Returns:
      results: [N, 1, img_h, img_w]
  """

  def __init__(self,
               threshold=0.5,
               padding=1):
    """Project mask head results on specified image"""
    self.threshold = threshold
    self.padding = padding

  def expand_mask(self, mask, padding):
    """Fill padding around the mask [N, N]
    """
    n, h, w = mask.shape
    # scale short line rules
    short = h if h < w else w
    pad2 = 2 * padding
    scale = float(short + pad2) / short
    # pad
    padded_mask = mask.new_zeros((n, h + pad2, w + pad2))
    padded_mask[:, padding: -padding, padding: -padding] = mask
    return padded_mask.to(torch.float32), scale

  def expand_bbox(self, box, scale):
    """Expand bbox because of the padding
    """
    return torch.stack((box[0] * scale,
                        box[1] * scale,
                        box[2] * scale,
                        box[3] * scale))

  def project_mask(self, mask, box, im_h, im_w, thresh, padding):
    """ Project mask to specified size
      mask: Tensor[1, 28, 28]
      box: Tensor[4]
    """
    # expand masks
    # mask, scale = self.expand_mask(mask, padding)
    # box = self.expand_bbox(box, 1.0).to(dtype=torch.int32)
    box = box.to(dtype=torch.int32)

    # fill in bbox
    h = max(int(box[3] - box[1] + 1), 1)
    w = max(int(box[2] - box[0] + 1), 1)

    # resize
    mask = F.interpolate(input=mask[None],
                         size=(h, w),
                         mode="bilinear",
                         align_corners=False)

    # to bool
    if thresh > 0:
      mask = mask[0][0] > thresh
    else:
      raise NotImplementedError

    # paste to image
    im_mask = torch.zeros((im_h, im_w), dtype=torch.uint8)
    x1 = max(box[0], 0)
    y1 = max(box[1], 0)
    x2 = min(box[2] + 1, im_w)
    y2 = min(box[3] + 1, im_h)
    im_mask[y1:y2, x1:x2] = mask[(y1-box[1]): (y2-box[1]),
                                 (x1-box[0]): (x2-box[0])]
    return im_mask

  def __call__(self, boxlist):
    """
    Arguments:
      masks: extra["masks"] [N, 1, 28, 28]
      boxes: BoxList

    Returns:
      results: [N, 1, img_h, img_w]
    """
    results = []
    # for each objects
    for mask, bbox in zip(boxlist.field("masks"), boxlist.bbox):
      resized_mask = self.project_mask(mask,  # [1, 28, 28]
                                       bbox,  # [4]
                                       boxlist.size[1],
                                       boxlist.size[0],
                                       self.threshold,
                                       self.padding)
      results.append(resized_mask)
    return results
