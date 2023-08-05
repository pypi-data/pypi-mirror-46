# Copyright 2019 Siu-Kei Muk (David). All Rights Reserved.
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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import queue
import threading
from typing import List

from tinypipe.blocks import pipe as pipe_lib


class Pipeline(object):
  def __init__(self, capacity=None, cooldown_secs=None):
    self._capacity = capacity
    self._cooldown_secs = cooldown_secs
    self._pipes = []

    self._lock = threading.Lock()
    self._chain = None
    self._qin = None

    self._built = False
    self._running = False
    self._join_called = False

  def append(self, pipe: pipe_lib.Pipe):
    if not isinstance(pipe, pipe_lib.Pipe):
      raise TypeError("`pipe` must be a `Pipe` instance. Given: {}"
                      .format(pipe))

    # TODO: Do we actually need a lock here?
    if not self._built:
      with self._lock:
        if not self._built:
          self._pipes.append(pipe)
          return
    logging.warning("No further pipe could be added after the pipeline has "
                    "been built. Ignoring pipe: {}".format(pipe))

  def extend(self, pipes: List[pipe_lib.Pipe]):
    [self.append(pipe) for pipe in pipes]

  def put(self, data):
    if not self._built:
      raise RuntimeError("Pipeline must be built to begin accepting data.")
    
    if self._join_called:
      logging.warning("No further data is accepted after `join()` is called. "
                      "Ignoring data: {}".format(data))
      return
    
    self._qin.put(data)

  def build(self):
    if self._built: return

    with self._lock:
      if self._built: return
      self._built = True
      self._qin = queue.Queue()
      self._chain = pipe_lib.ChainedPipe(self._pipes,
                                         capacity=self._capacity,
                                         cooldown_secs=self._cooldown_secs)
      self._chain.build(self._qin, None)

  def start(self):
    if not self._built:
      raise RuntimeError("Pipeline must be built before running. "
                         "Call `build()` before `start()`.")
    self._running = True
    self._chain.start()

  def join(self):
    if not self._running:
      logging.warning("Pipeline is not running. "
                      "The call `Pipeline.join()` has not effect.")
      return
    self._join_called = True
    self._chain.wrap_up()
    self._running = False
