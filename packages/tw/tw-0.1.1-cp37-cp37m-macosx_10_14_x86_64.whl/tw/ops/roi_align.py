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
"""RoI Align"""
from torch import nn
from torch.nn.modules.utils import _pair
from torch.autograd import Function
from torch.autograd.function import once_differentiable
from tw import _C


class _RoIAlign(Function):
  @staticmethod
  def forward(ctx,
              fwd_input,
              roi,
              output_size,
              spatial_scale,
              sampling_ratio):
    ctx.save_for_backward(roi)
    ctx.output_size = _pair(output_size)
    ctx.spatial_scale = spatial_scale
    ctx.sampling_ratio = sampling_ratio
    ctx.input_shape = fwd_input.size()
    outputs = _C.roi_align_forward(fwd_input,
                                   roi,
                                   spatial_scale,
                                   output_size[0],
                                   output_size[1],
                                   sampling_ratio)
    return outputs

  @staticmethod
  @once_differentiable
  def backward(ctx, grad_output):
    rois, = ctx.saved_tensors
    output_size = ctx.output_size
    spatial_scale = ctx.spatial_scale
    sampling_ratio = ctx.sampling_ratio
    bs, ch, h, w = ctx.input_shape
    grad_input = _C.roi_align_backward(grad_output,
                                      rois,
                                      spatial_scale,
                                      output_size[0],
                                      output_size[1],
                                      bs,
                                      ch,
                                      h,
                                      w,
                                      sampling_ratio)
    return grad_input, None, None, None, None


class RoIAlign(nn.Module):
  def __init__(self, output_size, spatial_scale, sampling_ratio):
    super(RoIAlign, self).__init__()
    self.output_size = output_size
    self.spatial_scale = spatial_scale
    self.sampling_ratio = sampling_ratio

  def forward(self, inputs, rois):
    return _RoIAlign.apply(inputs,
                           rois,
                           self.output_size,
                           self.spatial_scale,
                           self.sampling_ratio)

  def __repr__(self):
    tmpstr = self.__class__.__name__ + "("
    tmpstr += "output_size=" + str(self.output_size)
    tmpstr += ", spatial_scale=" + str(self.spatial_scale)
    tmpstr += ", sampling_ratio=" + str(self.sampling_ratio)
    tmpstr += ")"
    return tmpstr
