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
"""kv db"""
import atexit
import pickle
from datetime import datetime


class FastKV():
  def __init__(self, dump_when_exit=True, dump_interval=-1):
    self.kv = {
        'info': {
            'name': 'tw',
            'path': './',
            'created_time': self._timestamp(),
            'modified_time': self._timestamp(),
            'count': 0,
        },
        'dump': {
            'bind_keys': None,
            'bind_scope': None,
            'interval': dump_interval,
            'exit': dump_when_exit,
        },
        'db': {
            'default': {}
        },
    }
    atexit.register(self._exit)

  def init(self, name='tw', path='./'):
    self.kv['info']['name'] = name
    self.kv['info']['path'] = path
    return self

  def init_from_db(self, pkl_path):
    """restore data from pkl"""
    with open(pkl_path, 'rb') as fp:
      restore = pickle.load(fp)
    self.kv = restore
    print(self.kv)
    return self

  def set_dump_interval(self, invl: int):
    if invl > 0:
      self.kv['dump']['interval'] = invl
    return self

  def _timestamp(self):
    return datetime.strftime(datetime.now(), '%y%m%d%H%M%S')

  def __str__(self):
    ret = 'Fast KV Overview:\n'
    ret += ' INFO:\n'
    for key in self.kv['info']:
      ret += '  {}: {}\n'.format(key, self.kv['info'][key])
    ret += ' DUMP:\n'
    for key in self.kv['dump']:
      ret += '  {}: {}\n'.format(key, self.kv['dump'][key])
    ret += ' DB:\n'
    for key in self.kv['db']:
      ret += '  {}: {}\n'.format(key, list(self.kv['db'][key].keys()))
    return ret

  def _exit(self):
    if self.kv['dump']['exit']:
      self.dump()

  def _insert(self, key, value, scope):
    if scope not in self.kv['db']:
      self.kv['db'][scope] = {}
    if key not in self.kv['db'][scope]:
      self.kv['db'][scope][key] = []
    self.kv['db'][scope][key].append(value)
    self.kv['info']['modified_time'] = self._timestamp()

  def get(self, scope, key):
    return self.kv['db'][scope][key]

  def dump(self):
    export_path = '{}/{}.{}.kv.pkl'.format(self.kv['info']['path'],
                                           self.kv['info']['name'],
                                           self.kv['info']['modified_time'])
    with open(export_path, 'wb') as fw:
      pickle.dump(self.kv, fw)

  def bind_keys(self, keys, scope='default'):
    assert isinstance(keys, (list, tuple))
    self.kv['dump']['bind_keys'] = keys
    self.kv['dump']['bind_scope'] = scope

  def bupdate(self, values, step=None):
    assert len(self.kv['dump']['bind_keys']) == len(values)
    return self.update(keys=self.kv['dump']['bind_keys'],
                       values=values,
                       step=step,
                       scope=self.kv['dump']['bind_scope'])

  def update(self, keys, values, step=None, scope='default'):
    assert isinstance(keys, (list, tuple))
    assert isinstance(values, (list, tuple))
    # insert
    for key, value in zip(keys, values):
      if step:
        self._insert(key, (step, value), scope)
      else:
        self._insert(key, value, scope)
     # record
    self.kv['info']['count'] += 1
    # dump
    if self.kv['dump']['interval'] > 0 and \
       self.kv['info']['count'] % self.kv['dump']['interval'] == 0:
      self.dump()
