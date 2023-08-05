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
"""string"""


def concat_keys_and_values(keys, vals):
  """ Format keys and values in string.
  e.g.
    keys = ['a', 'b', 'c']
    vals = [4, 5, 6]
    str = 'a:4, b:5, c:6'
  """
  fmt = ''
  for tup in zip(keys, vals):
    fmt += ', {0}: {1}'.format(tup[0], tup[1])
  return fmt


def join_dots(*inputs):
  """['123', '456', '789'] -> '123.456.789'"""
  return '.'.join([item for item in inputs])


def typelist(dtype_list):
  """(type1, type2, type3)"""
  return '(' + ', '.join([item.__name__ for item in dtype_list]) + ')'


def class_members(obj):
  """return class members in string."""
  return ', '.join(['%s: %s' % item for item in sorted(obj.__dict__.items())])
