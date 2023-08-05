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
"""Matcher
"""
import torch


class Matcher():
  def __init__(self,
               high_threshold,
               low_threshold,
               allow_low_quality_matches=False,
               below_low_thresh_label=-1,
               between_thresh_label=-2):
    """Generally, we could get a set of boxlist of ground truth like [M, 4],
     and a prediction boxlist like [N, 4]. Then, by computing IoU, the result
     matrix is [M, N] IoU scores [0, 1]. Next, we need to divide the matrix
     into three parts:
      - low confidence: background --> -1
      - middle: maybe emmm? --> -2
      - high confidence: foreground --> [0, N] (the number of object)

    Arguments:
      high_threshold (float): quality values greater than or equal to
          this value are candidate matches.
      low_threshold (float): a lower quality threshold used to stratify
          matches into three levels:
          1) matches >= high_threshold
          2) BETWEEN_THRESHOLDS matches in [low_threshold, high_threshold)
          3) BELOW_LOW_THRESHOLD matches in [0, low_threshold)
      allow_low_quality_matches (bool): if True, produce additional matches
          for predictions that have only low-quality match candidates. See
          set_low_quality_matches_ for more details.
    """
    assert low_threshold <= high_threshold
    self.high_threshold = high_threshold
    self.low_threshold = low_threshold
    self.allow_low_quality_matches = allow_low_quality_matches
    self.below_low_thresh_label = below_low_thresh_label
    self.between_thresh_label = between_thresh_label

  def __call__(self, match_matrix):
    """
    Arguments:
      match_quality_matrix (Tensor[float]): an MxN tensor, containing the
      pairwise quality between M ground-truth elements and N predicted elements.
    Returns:
      matches (Tensor[int64]): an N tensor where N[i] is a matched gt in
      [0, M - 1] or a negative value indicating that prediction i could not
      be matched.
    """
    # empty targets or proposals not supported during training
    if match_matrix.numel() == 0:
      if match_matrix.shape[0] == 0:
        raise ValueError(
            "No ground-truth boxes available for one of the images "
            "during training")
      else:
        raise ValueError(
            "No proposal boxes available for one of the images "
            "during training")

    # match_quality_matrix is M (gt) x N (predicted)
    # Max over gt elements (dim 0) to find best gt candidate for each prediction
    matched_val, matched_idx = match_matrix.max(dim=0)
    if self.allow_low_quality_matches:
      all_matches = matched_idx.clone()

    # Assign candidate matches with low quality to negative (unassigned) values
    below_low_threshold = matched_val < self.low_threshold
    between_thresholds = (matched_val >= self.low_threshold) \
        & (matched_val < self.high_threshold)
    matched_idx[below_low_threshold] = self.below_low_thresh_label
    matched_idx[between_thresholds] = self.between_thresh_label

    if self.allow_low_quality_matches:
      self.set_low_quality_matches(matched_idx, all_matches, match_matrix)

    return matched_idx

  def set_low_quality_matches(self, matched_idx, all_matches, match_matrix):
    """Produce additional mathces even if these matches with low confidence.
    e.g. for some situation, the IoU between gt and prediction maybe totally
    below low_threshold, where there is no any matches. Therefore, we could add
    some of low threshold matches but these matches is the high scores among
    these low confidence matches.
    """
    # For each gt, find the prediction with which it has highest quality
    highest_quality_foreach_gt, _ = match_matrix.max(dim=1)
    # Find highest quality match available, even if it is low, including ties
    gt_pred_pairs_of_highest_quality = torch.nonzero(
        match_matrix == highest_quality_foreach_gt[:, None])
    # Example gt_pred_pairs_of_highest_quality:
    #   tensor([[    0, 39796],
    #           [    1, 32055],
    #           [    1, 32070],
    #           [    2, 39190],
    #           [    2, 40255],
    #           [    3, 40390],
    #           [    3, 41455],
    #           [    4, 45470],
    #           [    5, 45325],
    #           [    5, 46390]])
    # Each row is a (gt index, prediction index)
    # Note how gt items 1, 2, 3, and 5 each have two ties

    pred_inds_to_update = gt_pred_pairs_of_highest_quality[:, 1]
    matched_idx[pred_inds_to_update] = all_matches[pred_inds_to_update]
