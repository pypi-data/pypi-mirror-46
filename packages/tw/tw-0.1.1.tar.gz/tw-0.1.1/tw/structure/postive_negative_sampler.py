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
"""This class samples batches, ensuring that they contain a fixed proportion
of positives.
"""
import torch


class PostiveNegativeSampler(object):
  def __init__(self, batch_size_per_image, positive_fraction):
    """
    Arguments:
      batch_size_per_image (int): number of elements to be selected per image
      positive_fraction (float): percentace of positive elements per batch
    """
    self.batch_size_per_image = batch_size_per_image
    self.positive_fraction = positive_fraction

  def __call__(self, matched_idxs):
    """
    Arguments:
      matched idxs: list of tensors containing -1, 0 or positive values.
        Each tensor corresponds to a specific image. -1 values are ignored, 
        0 are considered as negatives and > 0 as positives.

    Returns:
      pos_idx (list[tensor])
      neg_idx (list[tensor])

      Returns two lists of binary masks for each image. The first list contains
      the positive elements that were selected, and the second list the
      negative example. 0 for not, 1 for selected.
    """
    pos_idx = []
    neg_idx = []
    for matched_idxs_per_image in matched_idxs:
      positive = torch.nonzero(matched_idxs_per_image >= 1).squeeze(1)
      negative = torch.nonzero(matched_idxs_per_image == 0).squeeze(1)

      num_pos = int(self.batch_size_per_image * self.positive_fraction)
      # protect against not enough positive examples
      num_pos = min(positive.numel(), num_pos)
      num_neg = self.batch_size_per_image - num_pos
      # protect against not enough negative examples
      num_neg = min(negative.numel(), num_neg)

      # randomly select positive and negative examples
      perm1 = torch.randperm(
          positive.numel(), device=positive.device)[:num_pos]
      perm2 = torch.randperm(
          negative.numel(), device=negative.device)[:num_neg]

      pos_idx_per_image = positive[perm1]
      neg_idx_per_image = negative[perm2]

      # create binary mask from indices
      pos_idx_per_image_mask = torch.zeros_like(
          matched_idxs_per_image, dtype=torch.uint8)
      neg_idx_per_image_mask = torch.zeros_like(
          matched_idxs_per_image, dtype=torch.uint8)
      pos_idx_per_image_mask[pos_idx_per_image] = 1
      neg_idx_per_image_mask[neg_idx_per_image] = 1

      pos_idx.append(pos_idx_per_image_mask)
      neg_idx.append(neg_idx_per_image_mask)

    return pos_idx, neg_idx
