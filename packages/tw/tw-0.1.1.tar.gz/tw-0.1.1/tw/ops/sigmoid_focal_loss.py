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
"""Sigmoid Focal Loss"""
import torch
from torch import nn
from torch.nn.modules.utils import _pair
from torch.autograd import Function
from torch.autograd.function import once_differentiable
from tw import _C


# TODO: Use JIT to replace CUDA implementation in the future.
class _SigmoidFocalLoss(Function):
  @staticmethod
  def forward(ctx, logits, targets, gamma, alpha):
    ctx.save_for_backward(logits, targets)
    num_classes = logits.shape[1]
    ctx.num_classes = num_classes
    ctx.gamma = gamma
    ctx.alpha = alpha

    losses = _C.sigmoid_focalloss_forward(
        logits, targets, num_classes, gamma, alpha
    )
    return losses

  @staticmethod
  @once_differentiable
  def backward(ctx, d_loss):
    logits, targets = ctx.saved_tensors
    num_classes = ctx.num_classes
    gamma = ctx.gamma
    alpha = ctx.alpha
    d_loss = d_loss.contiguous()
    d_logits = _C.sigmoid_focalloss_backward(
        logits, targets, d_loss, num_classes, gamma, alpha
    )
    return d_logits, None, None, None, None


def sigmoid_focal_loss_cpu(logits, targets, gamma, alpha):
  num_classes = logits.shape[1]
  gamma = gamma[0]
  alpha = alpha[0]
  dtype = targets.dtype
  device = targets.device
  class_range = torch.arange(
      1, num_classes+1, dtype=dtype, device=device).unsqueeze(0)

  t = targets.unsqueeze(1)
  p = torch.sigmoid(logits)
  term1 = (1 - p) ** gamma * torch.log(p)
  term2 = p ** gamma * torch.log(1 - p)
  return -(t == class_range).float() * term1 * alpha - ((t != class_range) * (t >= 0)).float() * term2 * (1 - alpha)


class SigmoidFocalLoss(nn.Module):
  def __init__(self, gamma, alpha):
    super(SigmoidFocalLoss, self).__init__()
    self.gamma = gamma
    self.alpha = alpha

  def forward(self, logits, targets):
    device = logits.device
    if logits.is_cuda:
      loss_func = _SigmoidFocalLoss.apply
    else:
      loss_func = sigmoid_focal_loss_cpu

    loss = loss_func(logits, targets, self.gamma, self.alpha)
    return loss.sum()

  def __repr__(self):
    tmpstr = self.__class__.__name__ + "("
    tmpstr += "gamma=" + str(self.gamma)
    tmpstr += ", alpha=" + str(self.alpha)
    tmpstr += ")"
    return tmpstr
