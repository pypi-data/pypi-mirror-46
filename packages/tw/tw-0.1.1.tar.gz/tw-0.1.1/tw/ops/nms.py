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
"""NMS ops"""
import torch
from tw import _C


class NonMaxSuppression(torch.nn.Module):
  def forward(self, boxlist, score_field, thresh, max_proposals=0):
    if thresh < 0:
      return boxlist
    keep = _C.nms(boxlist.bbox, boxlist.field(score_field), thresh)
    if max_proposals > 0:
      keep = keep[: max_proposals]
    return boxlist[keep]
