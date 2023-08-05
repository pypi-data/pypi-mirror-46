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

import queue

from tinypipe.blocks.pipe import base as pipe_base


class FunctionPipe(pipe_base.FetchRetryPipe):
  def __init__(self,
               fn,
               max_retry=None,
               fetch_time=None):
    super(FunctionPipe, self).__init__(
        max_retry=max_retry, fetch_time=fetch_time)
    self._fn = fn

  def _run(self):
    try:
      data = self._fetch_data()
      out = self._fn(data)
      if self._qout is not None:
        self._qout.put(out)
      self._qin.task_done()
    except queue.Empty:
      pass
