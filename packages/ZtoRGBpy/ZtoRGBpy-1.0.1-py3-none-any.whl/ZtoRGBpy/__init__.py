# -*- coding: utf-8 -*-
# =================================================================================
#  Copyright 2019 Glen Fletcher <mail@glenfletcher.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  All documentation this file as docstrings or comments are licensed under the
#  Creative Commons Attribution-ShareAlike 4.0 International License; you may
#  not use this documentation except in compliance with this License.
#  You may obtain a copy of this License at
#
#    https://creativecommons.org/licenses/by-sa/4.0
#
# =================================================================================
"""
Reference
=========

Complex number to perceptually uniform RGB subset mapping library
Supports direct transformation of numpy arrays using remap, and
integration with matplotlib using imshow, colorbar and colorwheel.

.. moduleauthor:: Glen Fletcher <mail@glenfletcher.com>
"""

from ZtoRGBpy._core import remap, Scale, LinearScale, LogScale, \
    RGBColorProfile, sRGB_HIGH, sRGB_LOW, sRGB
from ZtoRGBpy._info import __authors__, __copyright__, __license__, \
    __contact__, __version__, __title__, __desc__

try:
    from ZtoRGBpy._mpl import colorbar, colorwheel, imshow
except ImportError:
    # pylint: disable=C0111
    _mpl_requirement = "Requires matplotlib>=1.3,<3"

    def colorbar():
        raise NotImplementedError(_mpl_requirement)

    def colorwheel():
        raise NotImplementedError(_mpl_requirement)
    
    def imshow():
        raise NotImplementedError(_mpl_requirement)

_real_module = {}

for name in list(locals().keys()):
    if name[0] != "_":
        _real_module[name] = locals()[name].__module__
        locals()[name].__module__ = "ZtoRGBpy"
