#/*##########################################################################
# Copyright (C) 20016-2017 European Synchrotron Radiation Facility
#
# This file is part of tomogui. Interface for tomography developed at
# the ESRF by the Software group.
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
#############################################################################*/


__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "23/02/2018"


import unittest
from .Scenario import ScenarioProject, has_freeart as Scenario_project_has_freeart
from tomogui.configuration import config as tomoguiconfig
from silx.gui import qt
import numpy
import h5py
import os
try:
    import freeart
    from freeart.configuration import config as freeartconfig
    import tomogui.gui.reconstruction.freeartRM
    from tomogui.gui.datasource.QDataSourceFluoWidget import QDataSourceFluoWidget
    freeart_missing = False
except ImportError:
    freeart_missing = True
try:
    from silx.opencl.backprojection import Backprojection
    has_silx_FBP = True
except ImportError:
    has_silx_FBP = False


@unittest.skipIf(freeart_missing, "freeart missing")
class TxProject(ScenarioProject):
    """Test that the usage of the project window for Tx is correct"""

    N_SINOGRAM = 2
    """Number of sinogram to generate"""

    def __init__(self, *args, **kwargs):
        ScenarioProject.__init__(self, *args, **kwargs)

    def setUp(self):
        ScenarioProject.setUp(self)

    def tearDown(self):
        ScenarioProject.tearDown(self)

    def testScenarioItOnly(self):
        """Test the scenario where we give all information and normalization is
        made by a single value"""
        self.setReconstructionType(freeartconfig._ReconsConfig.TX_ID)
        [self.addNewSinogram() for i in range(self.N_SINOGRAM)]

        self.save()
        config = self.loadFileConfig(self._file)
        self.assertTrue(len(config.sinograms) is self.N_SINOGRAM)

    def testScenarioItI0(self):
        """Test the scenario where we give all information and normalization is
        made by a sinogram"""
        self.setReconstructionType(freeartconfig._ReconsConfig.TX_ID)
        self.setI0()
        [self.addNewSinogram() for i in range(self.N_SINOGRAM)]

        self.save()
        config = self.loadFileConfig(self._file)
        self.assertTrue(len(config.sinograms) is self.N_SINOGRAM)


@unittest.skipIf(freeart_missing, "freeart missing")
class FluoProject(ScenarioProject):
    """Test that the usage of the project window for fluorescence is correct"""

    N_SINOGRAM = 3

    def __init__(self, *args, **kwargs):
        ScenarioProject.__init__(self, *args, **kwargs)

    def setUp(self):
        ScenarioProject.setUp(self)

    def testScenarioGiveItI0(self):
        """Check a project creation when we want to create the absorption
        matrix from It and I0"""
        self.setReconstructionType(freeartconfig._ReconsConfig.FLUO_ID)
        self.setFluoReconsMode(QDataSourceFluoWidget.GEN_ABS_SELF_ABS_OPT)
        [self.addNewSinogram() for i in range(self.N_SINOGRAM)]

    def testScenarioGiveAbsMatOnly(self):
        """Check a project creation where the absorption matrix only is given
        """
        self.setReconstructionType(freeartconfig._ReconsConfig.FLUO_ID)
        self.setFluoReconsMode(QDataSourceFluoWidget.GIVE_ABS_MAT_GEN_SELF_ABS_OPT)
        [self.addNewSinogram() for i in range(self.N_SINOGRAM)]

    def testScenarioGiveAbsMats(self):
        """Check a project where the absorption matrix and the self attenuation
        matrices are gave"""
        self.setReconstructionType(freeartconfig._ReconsConfig.FLUO_ID)
        self.setFluoReconsMode(QDataSourceFluoWidget.GIVE_ABS_MAT_AND_SELF_ABS_MAT_OPT)
        [self.addNewSinogram() for i in range(self.N_SINOGRAM)]

        self.save()
        self.loadFileConfig(self._file)

    def testCompleteFluoH5(self):
        """
        Test the scenario where the user want to make a fluorescence
        reconstruction starting from It and I0.

        Test the following case:
            * start from .h5 configuration file and with dataset contained into
               .h5 files
        """
        projExt = '.h5'
        fileExt = '.h5'

        # create the project
        self._file = os.path.join(self.tempdir, 'storeConfig' + projExt)
        self._createFluoItI0Project(fileExt)
        self.save(merge=False)

        # run reconstruction of the absorption matrix from It and I0
        widget = self._reconstructAbsMat()

        # reconstruct the fluorescence sinogram
        reconsAlg = widget.mainWindow.freeartInterpreter.getReconstructionAlgorithms()
        self.assertTrue(len(reconsAlg) > 0)
        algoName = list(reconsAlg)[0]
        self.assertTrue(len(reconsAlg[algoName].getPhantom().ravel()) is 0)

        widget.iterate(wait=True)
        qt.QApplication.instance().processEvents()
        self.assertFalse(numpy.array_equal(
                reconsAlg[algoName].getPhantom(),
                numpy.zeros(reconsAlg[algoName].getPhantom().shape)
        ))

    def testCompleteFluoCFG(self):
        """
        Test the scenario where the user want to make a fluorescence
        reconstruction starting from It and I0.

        Test the following case:
            * start from .cfg configuration file and with dataset contained into
               single .edf files
        """
        projExt = '.cfg'
        fileExt = '.edf'

        # create the project
        self._file = os.path.join(self.tempdir, 'storeConfig' + projExt)
        self._createFluoItI0Project(fileExt)
        self.save(merge=False)

        # run reconstruction of the absorption matrix from It and I0
        widget = self._reconstructAbsMat()

        # reconstruct the fluorescence sinogram
        reconsAlg = widget.mainWindow.freeartInterpreter.getReconstructionAlgorithms()
        self.assertTrue(len(reconsAlg) > 0)
        algoName = list(reconsAlg)[0]
        self.assertTrue(len(reconsAlg[algoName].getPhantom().ravel()) is 0)

        widget.iterate(wait=True)
        qt.QApplication.instance().processEvents()
        self.assertFalse(numpy.array_equal(
                reconsAlg[algoName].getPhantom(),
                numpy.zeros(reconsAlg[algoName].getPhantom().shape)
        ))

    def testCompleteFluoNoFileInfo(self):
        """
        Test the scenario where the user want to make a fluorescence
        reconstruction starting from It and I0.

        Test the following case:
            * start from data 'injected' into tomogui (used from pymca for example).
               this mean without any fileInfo
        """
        projExt = None
        fileExt = None

        # create the project
        self._file = None
        self._createFluoItI0Project(fileExt)

        # run reconstruction of the absorption matrix from It and I0
        widget = self._reconstructAbsMat()

        # reconstruct the fluorescence sinogram
        reconsAlg = widget.mainWindow.freeartInterpreter.getReconstructionAlgorithms()
        self.assertTrue(len(reconsAlg) > 0)
        algoName = list(reconsAlg)[0]
        self.assertTrue(len(reconsAlg[algoName].getPhantom().ravel()) is 0)

        widget.iterate(wait=True)
        qt.QApplication.instance().processEvents()
        self.assertFalse(numpy.array_equal(
                reconsAlg[algoName].getPhantom(),
                numpy.zeros(reconsAlg[algoName].getPhantom().shape)
        ))

    def testFullScenarioAllStoreIn(self):
        """
        Test the scenario where the user want to make a fluorescence
        reconstruction starting from It and I0.

        Test the following case:
            * Sinograms, It, I0... are stored into different .edf and .h5 files
              and we want to save them all into the same .h5 file with the
              configuration.
        """
        projExt = '.h5'
        fileExt = '.h5', '.edf'

        # create the project
        self._file = os.path.join(self.tempdir, 'storeConfig' + projExt)
        self._createFluoItI0Project(fileExt)
        self.save(merge=True)

        # check the .h5 file is complete...
        with h5py.File(self._file, 'r') as _file:
            self.assertTrue('data' in _file.keys())
            self.assertTrue('reconstruction' in _file.keys())

            data_node = _file['data']
            self.assertTrue('absmatrix' in data_node)
            self.assertTrue('materials' in data_node)

        # run reconstruction of the absorption matrix from It and I0
        widget = self._reconstructAbsMat()

        # reconstruct the fluorescence sinogram
        reconsAlg = widget.mainWindow.freeartInterpreter.getReconstructionAlgorithms()
        self.assertTrue(len(reconsAlg) > 0)
        algoName = list(reconsAlg)[0]
        self.assertTrue(len(reconsAlg[algoName].getPhantom().ravel()) is 0)

        widget.iterate(wait=True)
        qt.QApplication.instance().processEvents()
        self.assertFalse(numpy.array_equal(
                reconsAlg[algoName].getPhantom(),
                numpy.zeros(reconsAlg[algoName].getPhantom().shape)
        ))


@unittest.skipIf(has_silx_FBP is False, "silx FBP missing")
class FBPProject(ScenarioProject):
    """Test that the usage of the project window for Tx is correct"""

    N_SINOGRAM = 2
    """Number of sinogram to generate"""

    def __init__(self, *args, **kwargs):
        ScenarioProject.__init__(self, *args, **kwargs)

    def setUp(self):
        ScenarioProject.setUp(self)

    def tearDown(self):
        ScenarioProject.tearDown(self)

    def test(self):
        """Test the scenario where we give all information and normalization is
        made by a sinogram"""
        self.setReconstructionType(tomoguiconfig.FBPConfig.FBP_ID)
        self.setI0()
        [self.addNewSinogram() for i in range(self.N_SINOGRAM)]

        self.save()
        config = self.loadFileConfig(self._file)
        self.assertTrue(len(config.sinograms) is self.N_SINOGRAM)


def suite():
    test_suite = unittest.TestSuite()
    for testClass in (TxProject, FluoProject, FBPProject):
        test_suite.addTest(
            unittest.defaultTestLoader.loadTestsFromTestCase(testClass))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
