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
"""Extend base for extend a series of structure like boxlist, masklist and 
  keypointlist. Offering an unified interface to resize, crop, transpose, and etc.
"""
import abc


class Extend(abc.ABC):
  def __init__(self):
    pass

  @abc.abstractmethod
  def __repr__(self):
    """output basic information"""
    raise NotImplementedError

  @abc.abstractclassmethod
  def __getitem__(self, idx):
    """get someone elements"""
    raise NotImplementedError

  @abc.abstractclassmethod
  def convert(self, mode):
    """convert from a mode to another"""
    raise NotImplementedError

  @abc.abstractclassmethod
  def to(self, *args, **kwargs):
    """to another dtype or device"""
    raise NotImplementedError

  @abc.abstractclassmethod
  def transpose(self, method):
    """flip/rotate/..."""
    raise NotImplementedError

  @abc.abstractclassmethod
  def resize(self, size, *args, **kwargs):
    """resize current contents"""
    raise NotImplementedError

  @abc.abstractclassmethod
  def crop(self, box):
    """Crop a patch according to box"""
    raise NotImplementedError
