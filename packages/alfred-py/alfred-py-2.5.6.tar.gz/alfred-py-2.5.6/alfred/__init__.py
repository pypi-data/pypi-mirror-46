# -*- coding: utf-8 -*-
# file: __init__.py
# author: JinTian
# time: 05/02/2018 9:20 PM
# Copyright 2018 JinTian. All Rights Reserved.
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
# ------------------------------------------------------------------------
"""Bring in all of the public Alfred interface into this module."""
import importlib
# pylint: disable=g-bad-import-order

from .modules import *
from .vis import *
from .fusion import *
globals().update(importlib.import_module('alfred').__dict__)