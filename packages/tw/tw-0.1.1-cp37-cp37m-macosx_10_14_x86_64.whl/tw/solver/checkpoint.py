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
"""Snapshot
  We assume a standard storage method, the all model should be uniform keys.
    {
      'model': torch.nn.Module,
      'global_step': int,
      'optimizer': torch.Optimizer,
      'lr': torch.LR,
      'extra': ...,
    }
"""
import torch
from tw.utils.logger import logger
from tw.utils import filesystem as fs

class Snapshot():
  def __init__(self):
    self._model = {}
    self._step = None
    self._optimizer = None
    self._lr = None
    self._extra = None

  def step(self):
    if self._lr and self._optimizer:
      return self._step
    else:
      return -1

  def optimizer(self):
    if self._optimizer == {}:
      raise ValueError(self._optimizer)
    return self._optimizer

  def lr(self):
    if not self._lr:
      raise ValueError(self._lr)
    return self._lr

  def model(self):
    if self._model == {}:
      raise ValueError(self._model)
    return self._model

  def load(self, model, src, device):
    """Offer an advanced model loaded strategy.

    Arguments:
      model (nn.Module): a pre-defined pytorch model.
      src (str/dict): path-to-model-weights file.
      device (torch.Device): map_location to specify location.

    Returns:
      model (dict): including all key-values defined in path.
    """
    if isinstance(src, str):
      if src.startswith('http'):
        return self._load_from_url(model, src, device)
      else:
        return self._load_from_path(model, src, device)
    elif isinstance(src, dict):
      return self._load_from_dict(model, src, device)
    else:
      raise ValueError(src)

  def _load_from_url(self, model, path, device):
    import wget
    import os
    res = path.split('/')
    root = os.path.join('models', res[-2])
    dst = os.path.join(root, res[-1])
    fs.mkdirs(root)
    if not os.path.exists(dst):
      wget.download(path, dst)
    else:
      logger.info('Load cached pre-trained model from {}'.format(dst))
    return self._load_from_path(model, dst, device)

  def _load_from_path(self, model, path, device):
    content = torch.load(path, map_location=device)
    return self._load_from_dict(model, content, device)

  def _load_from_dict(self, model, content, device):
    """Compare the name and shape with model"""
    # from  other source
    if 'model' not in content:
      self._model = content
      return

    # load default content
    params = content['model']
    self._step = content['global_step'] if 'global_step' in content else -1
    self._optimizer = content['optimizer'] if 'optimizer' in content else None
    self._lr = content['lr'] if 'lr' in content else None
    self._extra = content['extra'] if 'extra' in content else None

    # get model name and shape
    model_shapes = {}
    for k, v in model.state_dict().items():
      model_shapes[k] = str(list(v.size()))

    # match name and shape
    for k, v in params.items():
      # if name not match
      if k not in model_shapes:
        logger.warn('{} could not be matched in current model'.format(k))
        continue
      # if shape not match
      if str(list(v.size())) != model_shapes[k]:
        logger.warn('{} could match the orginal size {}'.format(
            str(list(v.size())), model_shapes[k]))
        continue
      # matched
      self._model[k] = v

  def save(self, step, model, solver, root):
    torch.save({
        'model': model.state_dict(),
        'global_step': step,
        'optimizer': solver.Optimizer().state_dict() if solver else None,
        'lr': solver.LR().state_dict() if solver else None,
    }, '{}/model.{:08d}.pth'.format(root, step))

  def print_model(self, model):
    logger.net("Model Parameter Lists:")
    logger.net("{:60s} {:25s} {}".format('Variables', 'Shape', 'Trianable'))
    for k, v in model.named_parameters():
      logger.net("{:60s} {:25s} {}".format(
          k, str(list(v.data.size())), v.requires_grad))
