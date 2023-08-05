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
"""Pooler
  Implement a variety of roi pooling operation on feature maps.
  
  Step1:
    input proposals: BoxList([1000, 4], objectness:1000)
    input feature maps: [(1, 256, 200, 304), (1, 256, 100, 152), ...]
    So, we should first determine which proposals belong to which layer of 
      feature maps.

"""
import torch
from torch import nn
from ..ops import RoIAlign


class Pooler(nn.Module):
  def __init__(self,
               output_size,  # output size for the pooled region
               scales,  # scales for each Pooler
               sampling_ratio):  # sampling ratio for ROIAlign
    """Pooler for Detection with or without FPN. It currently hard-code 
      ROIAlign in the implementation, but that can be made more generic later 
      on. Also, the requirement of passing the scales is not strictly necessary, 
      as they can be inferred from the size of the feature map / size of 
      original image, which is available thanks to the BoxList.
    """
    super(Pooler, self).__init__()
    poolers = []
    for scale in scales:
      poolers.append(RoIAlign(output_size, scale, sampling_ratio))
    self.poolers = nn.ModuleList(poolers)
    self.num_levels = len(self.poolers)
    self.output_size = output_size
    # -log2(0.25) = 2
    self.kmin = - \
        torch.log2(torch.tensor(scales[0], dtype=torch.float32)).item()
    # -log2(0.03125) = 5
    self.kmax = - \
        torch.log2(torch.tensor(scales[-1], dtype=torch.float32)).item()

  def _map_roi_to_feature_level(self,
                                boxlists,  # list[BoxList]
                                kmin,
                                kmax,
                                canonical_scale=224,
                                canonical_level=4,
                                eps=1e-6):
    areas = [boxlist.area() for boxlist in boxlists]
    areas = torch.sqrt(torch.cat(areas, dim=0))
    target_lvs = canonical_level + torch.log2(areas/canonical_scale + eps)
    target_lvs = torch.clamp(torch.floor(target_lvs), min=kmin, max=kmax)
    # [1000]
    return target_lvs.to(torch.int64) - kmin

  def _convert_to_roi_format(self, boxlists):
    cat_boxlists = torch.cat([boxlist.bbox for boxlist in boxlists], dim=0)
    device, dtype = cat_boxlists.device, cat_boxlists.dtype
    # [1000, 1] -> with i
    ids = torch.cat(
        [torch.full((len(boxlist), 1), i, dtype=dtype, device=device)
         for i, boxlist in enumerate(boxlists)],
        dim=0)
    rois = torch.cat([ids, cat_boxlists], dim=1)
    # [1000, 5(ids, xyxy)]
    return rois

  def forward(self, x, boxlists):
    """ Implement Pooler on each feature maps via the boxlist
      x: feature map lists
      boxlists: list[BoxList]
    """
    rois = self._convert_to_roi_format(boxlists)

    # for C4 directly output
    if self.num_levels == 1:
      return self.poolers[0](x[0], rois)

    # for FPN
    levels = self._map_roi_to_feature_level(boxlists, self.kmin, self.kmax)
    results = torch.zeros(
        (len(rois), x[0].shape[1], self.output_size[0], self.output_size[1]),
        dtype=x[0].dtype,
        device=x[0].device)

    # pooling
    for level, (per_level_feature, pooler) in enumerate(zip(x, self.poolers)):
      idx_in_level = torch.nonzero(levels == level).squeeze(1)
      rois_per_level = rois[idx_in_level]
      results[idx_in_level] = pooler(per_level_feature, rois_per_level)

    # list [NxTensor(256, 7, 7)]
    return results
