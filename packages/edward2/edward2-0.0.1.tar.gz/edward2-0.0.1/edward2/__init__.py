# coding=utf-8
# Copyright 2019 The Google Research Authors.
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

"""Edward2 probabilistic programming language.

For user guides, see:

+ [Overview](
   https://github.com/google-research/google-research/blob/master/simple_probabilistic_programming/README.md)
+ [Upgrading from Edward to Edward2](
   https://github.com/google-research/google-research/blob/master/simple_probabilistic_programming/Upgrading_From_Edward_To_Edward2.md)

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_probability import distributions
from edward2 import generated_random_variables
from edward2.generated_random_variables import *  # pylint: disable=wildcard-import
from edward2.generated_random_variables import make_random_variable
from edward2.program_transformations import make_log_joint_fn
from edward2.random_variable import RandomVariable
from edward2.trace import get_next_tracer
from edward2.trace import tape
from edward2.trace import trace
from edward2.trace import traceable

from tensorflow.python.util.all_util import remove_undocumented


_allowed_symbols = [
    "RandomVariable",
    "get_next_tracer",
    "make_log_joint_fn",
    "make_random_variable",
    "tape",
    "trace",
    "traceable",
]
for name in dir(generated_random_variables):
  if name in sorted(dir(distributions)):
    _allowed_symbols.append(name)

remove_undocumented(__name__, _allowed_symbols)
