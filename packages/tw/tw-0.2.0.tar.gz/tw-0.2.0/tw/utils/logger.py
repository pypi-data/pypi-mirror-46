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
"""Logger to control display"""
import os
import time
import logging
from datetime import datetime


class Logger():
  """Logger helper"""

  def __init__(self, name=None):
    # init
    name = 'tw' if name is None else name
    self.logger = logging.getLogger(name)
    self.logger.setLevel(logging.DEBUG)
    self._start_timer = time.time()

  def init(self, name, output_dir):
    """Initilize the logger"""
    logger_path = os.path.join(output_dir, name + '.log')
    self.set_filestream(logger_path)
    self.set_screenstream()

  def set_filestream(self, filepath, level=logging.DEBUG):
    """Setting content output to file"""
    fh = logging.FileHandler(filepath)
    fh.setLevel(level)
    self.logger.addHandler(fh)

  def set_screenstream(self, level=logging.DEBUG):
    """Setting content output to screen"""
    ch = logging.StreamHandler()
    ch.setLevel(level)
    self.logger.addHandler(ch)

  def _print(self, show_type, content):
    """Format print string"""
    str_date = '[' + \
        datetime.strftime(datetime.now(), '%y.%m.%d %H:%M:%S') + '] '
    self.logger.info(str_date + show_type + ' ' + content)

  def sys(self, content):
    self._print('[SYS]', content)

  def net(self, content):
    self._print('[NET]', content)

  def train(self, content):
    self._print('[TRN]', content)

  def val(self, content):
    self._print('[VAL]', content)

  def test(self, content):
    self._print('[TST]', content)

  def warn(self, content):
    self._print('[WAN]', content)

  def info(self, content):
    self._print('[INF]', content)

  def cfg(self, content):
    self._print('[CFG]', content)

  def error(self, content):
    self._print('[ERR]', content)

  def iters(self, cur_iter, keys, values):
    _data = 'Iter:%d' % cur_iter
    for i, key in enumerate(keys):
      if isinstance(values[i], int) or isinstance(values[i], str):
        _data += ', %s:%s' % (str(key), str(values[i]))
      elif key == 'lr':
        _data += ', %s:%.6f' % (str(key), float(values[i]))
      else:
        _data += ', %s:%.4f' % (str(key), float(values[i]))
    return _data

  def tic(self):
    self._start_timer = time.time()

  def toc(self):
    return (time.time() - self._start_timer) * 1000


logger = Logger()
