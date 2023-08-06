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
"""Full silx test suite.

silx.gui tests depends on Qt.
To disable them, set WITH_QT_TEST environement variable to 'False'.
"""

__authors__ = ["T. Vincent"]
__license__ = "MIT"
__date__ = "29/04/2016"


import logging
import os
import unittest
from .test_version import suite as test_version_suite
from .test_pymcaAPI import suite as test_pymca_suite
from .test_scenarii import suite as test_scenarii_suite
from ..gui.test import suite as test_gui_suite
from .test_scripts import suite as test_scripts_suite

logger = logging.getLogger(__name__)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_version_suite())
    test_suite.addTest(test_gui_suite())
    test_suite.addTest(test_pymca_suite())
    test_suite.addTest(test_scenarii_suite())
    test_suite.addTest(test_scripts_suite())
    return test_suite


def run_tests():
    """Run test complete test_suite"""
    runner = unittest.TextTestRunner()
    if not runner.run(suite()).wasSuccessful():
        print("Test suite failed")
        return 1
    else:
        print("Test suite succeeded")
        return 0
