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
import math
import abc
import torch


class BoxCoder(abc.ABC):
  def __init__(self):
    pass

  @abc.abstractmethod
  def encode(self, *args, **kwargs):
    pass

  @abc.abstractmethod
  def decode(self, *args, **kwargs):
    pass


class BoxCoderRCNN(BoxCoder):
  """BoudingBox used in RCNN-series

  Encoder: x1y1x2y2 -> centered xywh -> network(targets)
  1) proposals(ex): from anchor generators
  2) reference boxes(gt): from ground truth
    w = x2 - x1 + 1
    h = y2 - y1 + 1
    ctr_x = x1 + 0.5 * w
    ctr_y = y1 + 0.5 * h

    wx, wy, ww, wh = weights (weighted)
    dx = wx * (gt_ctr_x - ex_ctr_x) / ex_w
    dy = wy * (gt_ctr_y - ex_ctr_y) / ex_h
    dw = ww * log(gt_w / ex_w)
    dh = wh * log(gt_h / ex_h)

    targets = stack(dx, dy, dw, dh)

  Decoder: network -> x1y1x2y2

    Step1: top_n anchors transform 
      w = x2 - x1 + 1
      h = y2 - y1 + 1
      ctr_x = x1 + 0.5 * w
      ctr_y = y1 + 0.5 * h

    Step2: get real codes from network output [N, H*W*12(dx, dy, dw, dh)]
      dx = [N, 0::4] / wx
      dy = [N, 1::4] / wy
      dw = [N, 2::4] / ww
      dh = [N, 3::4] / wh

      pred_ctr_x = dx * w + ctr_x
      pred_ctr_y = dy * y + ctr_y
      pred_w = exp(dw) * w
      pred_h = exp(dh) * h

      pred_x1 = pred_ctr_x - 0.5 * pred_w
      pred_y1 = pred_ctr_y - 0.5 * pred_h
      pred_x2 = pred_ctr_x + 0.5 * pred_w
      pred_y2 = pred_ctr_y + 0.5 * pred_h
  """

  def __init__(self, weights, bbox_xform_clip=math.log(1000./16)):
    """
    Arguments:
      weights: tuple([x, y, w, h])
      bbox_xform_clip: prevent the overflow
    """
    super(BoxCoderRCNN, self).__init__()
    assert len(weights) == 4
    self.weights = weights
    self.bbox_xform_clip = bbox_xform_clip

  def encode(self, references, proposals):
    """ Encode a set of proposals with respect to some reference boxes
    """
    # proposals
    ex_w = proposals[:, 2] - proposals[:, 0] + 1
    ex_h = proposals[:, 3] - proposals[:, 1] + 1
    ex_ctr_x = proposals[:, 0] + 0.5 * ex_w
    ex_ctr_y = proposals[:, 1] + 0.5 * ex_h

    # reference
    gt_w = references[:, 2] - references[:, 0] + 1
    gt_h = references[:, 3] - references[:, 1] + 1
    gt_ctr_x = references[:, 0] + 0.5 * gt_w
    gt_ctr_y = references[:, 1] + 0.5 * gt_h

    wx, wy, ww, wh = self.weights
    dx = wx * (gt_ctr_x - ex_ctr_x) / ex_w
    dy = wy * (gt_ctr_y - ex_ctr_y) / ex_h
    dw = ww * torch.log(gt_w / ex_w)
    dh = wh * torch.log(gt_h / ex_h)

    target = torch.stack((dx, dy, dw, dh), dim=1)
    return target

  def decode(self, encodes, anchors):
    """From a set of original boxes and encoded relative box offsets, get the 
      decoded boxes.

    Arguments:
      encodes: Tensor([N*H*W*3, 4~]) encoded boxes from rpn
      anchors: Tensor([N*H*W*3, 4])
    """
    anchors = anchors.to(encodes.dtype)
    # get centered xywh
    w = anchors[:, 2] - anchors[:, 0] + 1
    h = anchors[:, 3] - anchors[:, 1] + 1
    ctr_x = anchors[:, 0] + 0.5 * w
    ctr_y = anchors[:, 1] + 0.5 * h

    # decode the boxes from network
    wx, wy, ww, wh = self.weights

    # divided weights
    dx = encodes[:, 0::4] / wx
    dy = encodes[:, 1::4] / wy
    dw = encodes[:, 2::4] / ww
    dh = encodes[:, 3::4] / wh

    # prevent too large for exp
    dw = torch.clamp(dw, max=self.bbox_xform_clip)
    dh = torch.clamp(dh, max=self.bbox_xform_clip)

    # restore
    pred_ctr_x = dx * w[:, None] + ctr_x[:, None]
    pred_ctr_y = dy * h[:, None] + ctr_y[:, None]
    pred_w = torch.exp(dw) * w[:, None]
    pred_h = torch.exp(dh) * h[:, None]

    # convert to xyxy mode
    preds = torch.zeros_like(encodes)
    preds[:, 0::4] = pred_ctr_x - 0.5 * pred_w
    preds[:, 1::4] = pred_ctr_y - 0.5 * pred_h
    preds[:, 2::4] = pred_ctr_x + 0.5 * pred_w - 1
    preds[:, 3::4] = pred_ctr_y + 0.5 * pred_h - 1

    return preds
