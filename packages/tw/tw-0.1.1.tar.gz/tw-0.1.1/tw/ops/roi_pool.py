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
"""RoI Pool"""
from torch import nn
from torch.nn.modules.utils import _pair
from torch.autograd import Function
from torch.autograd.function import once_differentiable
from tw import _C


class _ROIPool(Function):
  @staticmethod
  def forward(ctx, inputs, roi, output_size, spatial_scale):
    ctx.output_size = _pair(output_size)
    ctx.spatial_scale = spatial_scale
    ctx.input_shape = inputs.size()
    output, argmax = _C.roi_pool_forward(
        inputs, roi, spatial_scale, output_size[0], output_size[1]
    )
    ctx.save_for_backward(inputs, roi, argmax)
    return output

  @staticmethod
  @once_differentiable
  def backward(ctx, grad_output):
    inputs, rois, argmax = ctx.saved_tensors
    output_size = ctx.output_size
    spatial_scale = ctx.spatial_scale
    bs, ch, h, w = ctx.input_shape
    grad_input = _C.roi_pool_backward(
        grad_output,
        inputs,
        rois,
        argmax,
        spatial_scale,
        output_size[0],
        output_size[1],
        bs,
        ch,
        h,
        w,
    )
    return grad_input, None, None, None


class ROIPool(nn.Module):
  def __init__(self, output_size, spatial_scale):
    super(ROIPool, self).__init__()
    self.output_size = output_size
    self.spatial_scale = spatial_scale

  def forward(self, inputs, rois):
    return _ROIPool.apply(input, rois, self.output_size, self.spatial_scale)

  def __repr__(self):
    tmpstr = self.__class__.__name__ + "("
    tmpstr += "output_size=" + str(self.output_size)
    tmpstr += ", spatial_scale=" + str(self.spatial_scale)
    tmpstr += ")"
    return tmpstr
