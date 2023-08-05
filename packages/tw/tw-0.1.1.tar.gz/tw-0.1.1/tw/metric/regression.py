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
"""MAE and RMSE"""
import torch


class RegressionIndicator():
  def __init__(self, mae=True, rmse=True, mse=False, r_square=False):
    """Compute RegressionIndicator"""

    if mse or r_square:
      raise NotImplementedError

    self.has_mae = mae
    self.has_rmse = rmse
    self.has_mse = mse
    self.has_r_square = r_square

    self.mae = 0
    self.rmse = 0
    self.mse = 0
    self.r_square = 0

  def __call__(self, output, target):
    """Compute MAE and RMSE
      Inputs:
        output: [N,]
        target: [N,]
      Returns:
        list with shape(k): the correct percentage among N inputs.
    """
    error = output-target
    self.mae = torch.mean(torch.abs(error))
    self.rmse = torch.sqrt(torch.mean(error*error))
    return {'mae': self.mae, 'rmse': self.rmse}
