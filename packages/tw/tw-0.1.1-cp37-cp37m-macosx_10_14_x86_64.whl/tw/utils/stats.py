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
"""Stats"""
import sys


class AverMeter():
  def __init__(self):
    """Computes and stores the average and current value"""
    self.reset()

  def reset(self):
    self.val = 0
    self.avg = 0
    self.sum = 0
    self.count = 0

  def update(self, val):
    self.val = val
    self.sum += val
    self.count += 1
    self.avg = self.sum / self.count


class AverSet():
  def __init__(self):
    """Collect network training stats info"""
    self.db = {}

  def reset(self, key=None):
    if key is None:
      for each_key in self.db:
        self.db[each_key].reset()
    else:
      self.db[key].reset()

  def update(self, keys, vals=None):
    """if keys is a dict represents {'key': val, 'key': vale}"""
    if isinstance(keys, dict):
      return self.update(list(keys.keys()), list(keys.values()))
    # normal method
    for tup in zip(keys, vals):
      if tup[0] not in self.db:
        self.db[tup[0]] = AverMeter()
      else:
        self.db[tup[0]].update(tup[1])

  def __str__(self):
    rets = ''
    for idx, key in enumerate(self.db):
      if idx == 0:
        rets = '{0}:{1:.3f}'.format(key, self.db[key].avg)
      elif key == 'lr':
        rets += ', {0}:{1:.6f}'.format(key, self.db[key].avg)
      else:
        rets += ', {0}:{1:.3f}'.format(key, self.db[key].avg)
    return rets

  def __getitem__(self, key):
    return self.db[key]


class OptimMeter():
  def __init__(self, key, metric):
    self.key = key
    self.step = 0
    self.metric = metric
    if self.metric == 'min':
      self.value = sys.float_info.max
    elif self.metric == 'max':
      self.value = -sys.float_info.max
    else:
      raise ValueError('Current only could using \'max\' or \'min\'')
    self.extra = None

  def update(self, step, value, extra=None):
    if self.metric == 'min' and value < self.value:
      self.step = step
      self.value = value
      self.extra = extra
    elif self.metric == 'max' and value > self.value:
      self.step = step
      self.value = value
      self.extra = extra


class OptimSet():
  def __init__(self, keys, metrics='min'):
    """Optimal records for meters
    """
    self.db = {}
    if isinstance(metrics, str):
      metrics = [metrics] * len(keys)
    for key, metric in zip(keys, metrics):
      self.db[key] = OptimMeter(key, metric)

  def update(self, key, step, value, extra=None):
    """ ('mse', 100000, 3.1415) """
    if key not in self.db:
      raise ValueError(key)
    self.db[key].update(step, value, extra)

  def __getitem__(self, key):
    return self.db[key]


if __name__ == "__main__":
  stats = AverSet()
  a = ['t0', 't1']
  b = [4, 5]
  for i in range(10):
    b[0] += i
    b[1] += i
    stats.update(a, b)
  print(stats)
