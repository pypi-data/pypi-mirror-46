# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""Add the configuration missing, for silx for example"""

__authors__ = ["Henri Payno"]
__license__ = "MIT"
__date__ = "31/10/2017"

try:
    from freeart.configuration.config import _ReconsConfig, _SimpleSinoConfig
    from freeart.configuration.configIO import ConfigReader
except:
    from ..third_party.configuration.config import _ReconsConfig, _SimpleSinoConfig
    from ..third_party.configuration.configIO import ConfigReader


class FBPConfig(_SimpleSinoConfig):
    FBP_ID = 'FBP'

    def __init__(self, sinograms=None, *var, **kw):
        _SimpleSinoConfig.__init__(self, reconsType=FBPConfig.FBP_ID,
                                   sinograms=sinograms, *var, **kw)

# patch compatible configuration types
_ReconsConfig.RECONS_TYPES.append(FBPConfig.FBP_ID)
ConfigReader.dictReconsTypeToReconsConf[FBPConfig.FBP_ID] = FBPConfig
