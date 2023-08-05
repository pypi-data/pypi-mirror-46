# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
"""Operators"""
from .nms import NonMaxSuppression
from .roi_align import RoIAlign
from .roi_pool import ROIPool
from .sigmoid_focal_loss import SigmoidFocalLoss

from .frozen_batch_norm import FrozenBatchNorm2D

from .empty_op import EmptyBatchNorm2d
from .empty_op import EmptyConv2d
from .empty_op import EmptyConvTranspose2d
from .empty_op import EmptyInterpolate
from .empty_op import EmptyLayer

from .yolo_layer import YOLOLayer


__all__ = [
    'NonMaxSuppression',
    'RoIAlign',
    'ROIPool',
    'SigmoidFocalLoss',
    'FrozenBatchNorm2D',
    'EmptyBatchNorm2d',
    'EmptyConv2d',
    'EmptyConvTranspose2d',
    'EmptyInterpolate',
    'EmptyLayer',
    'YOLOLayer',
]
