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


class ImageList():
  """A list of image as inputs for training, images with possibly varying sizes
    are padding by zero to the same size.
  """

  def __init__(self, tensors, size_divisible=0):
    """Arguments:
      tensors: a list of image tensor (e.g. [[3, 400, 800], [3, 200, 600]])
      size_divisible: to padding a size that could be dvisible.
    """
    self.tensors = tensors
    self.sizes = None

    if not isinstance(tensors, (tuple, list)):
      raise ValueError(type(tensors))

    # where the minimum edge should be same
    # so we could get max the edges
    max_size = list(max(s) for s in zip(*[img.shape for img in tensors]))

    # size divisible for network
    if size_divisible > 0:
      stride = size_divisible
      max_size[1] = int(math.ceil(max_size[1] / stride) * stride)
      max_size[2] = int(math.ceil(max_size[2] / stride) * stride)

    # new tensor shape [N, C, max_H, max_W]
    batch_shape = (len(tensors), ) + tuple(max_size)
    # create a new tensor with same dtype and device
    batch_imgs = tensors[0].new(*batch_shape).zero_()
    # copy image to left top, padding right bottom
    for t, img in zip(tensors, batch_imgs):
      img[: t.shape[0], : t.shape[1], : t.shape[2]].copy_(t)

    # save
    self.tensors = batch_imgs
    # keep original size
    self.sizes = [t.shape[-2:] for t in tensors]

  def __len__(self):
    return len(self.sizes)

  def to(self, *args, **kwargs):
    self.tensors = self.tensors.to(*args, **kwargs)
    return self
