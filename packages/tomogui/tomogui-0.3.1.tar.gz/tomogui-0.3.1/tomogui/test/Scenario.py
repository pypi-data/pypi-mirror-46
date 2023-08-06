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
from collections import OrderedDict
import numpy
from silx.gui import qt
import tempfile
import os
import shutil
from tomogui.gui.ProjectWidget import ProjectWindow
from tomogui.configuration import config as tomoguiconfig
try:
    from tomogui.gui.datasource.QDataSourceFluoWidget import QDataSourceFluoWidget
    from tomogui.gui.reconstruction.freeartRM import FreeartReconsDialog
    from freeart.configuration import structs, fileInfo
    from freeart.configuration import config as freeartconfig
    from freeart.configuration import read
    has_freeart = True
except:
    has_freeart = False
    from tomogui.third_party.configuration import structs, fileInfo
    from tomogui.third_party.configuration import config as freeartconfig
    from tomogui.third_party.configuration import read

app = qt.QApplication.instance() or qt.QApplication([])


class _ScenarioBase(unittest.TestCase):
    pass


class ScenarioProject(_ScenarioBase):
    DET_X = 20
    N_PROJECTION = 40

    def setUp(self):
        self.mainWindow = ProjectWindow()
        self.mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.sinos = []
        self.iSino = 0
        self.tempdir = tempfile.mkdtemp()
        self._file = os.path.join(self.tempdir, 'storeConfig.h5')

    def tearDown(self):
        qt.QApplication.processEvents()
        self.mainWindow.close()
        shutil.rmtree(self.tempdir)

    def setReconstructionType(self, _type):
        """
        Define the reconstruction type to be run
        """
        self.mainWindow.mainWidget.getDataSourceWidget().setReconstructionType(_type)

    def getReconstructionType(self):
        return self.mainWindow.mainWidget.getDataSourceWidget().getReconstructionType()

    def setI0(self, extension='.edf'):
        data = numpy.random.random((self.N_PROJECTION, self.DET_X))

        if extension == '.h5':
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, 'I0.h5'),
                                                data_path='/data/I0')
        elif extension == '.edf':
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, 'I0.edf'))
        else:
            file_info = None

        self.I0 = structs.I0Sinogram(data=data + 1, fileInfo=file_info)
        if file_info is not None:
            self.I0.save()
        self._getNormWidget().I0Normalization.setI0(self.I0)

    def addNewSinogram(self, extension='.edf'):
        rtype = self.getReconstructionType()
        if rtype in (freeartconfig._ReconsConfig.FLUO_ID, freeartconfig._ReconsConfig.COMPTON_ID):
            self._addNewFluoSino(extension)
        else:
            self._addNewTxSino(extension)

    def _addNewFluoSino(self, extension='.edf'):
        data = numpy.random.random((self.N_PROJECTION, self.DET_X))
        if extension == '.edf':
            file_path = 'fluo_' + str(self.iSino) + '.edf'
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, file_path))
        elif extension == '.h5':
            file_path = 'fluo_' + str(self.iSino) + '.h5'
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, file_path),
                                                data_path='/data/fluosinogram_' + str(self.iSino))
        else:
            file_info = None
        sino = structs.FluoSino(fileInfo=file_info,
                                name='element'+str(self.iSino),
                                data=data,
                                physElmt='Fe',
                                ef=1.0,
                                selfAbsMat=None)
        if file_info is not None:
            sino.save()
        self._getQDSFluo().fluoSinogramsSelector.addSinogram(sino)
        self.iSino = self.iSino + 1

    def _addNewTxSino(self, extension='.edf'):
        data = numpy.random.random((self.N_PROJECTION, self.DET_X))
        if extension == '.edf':
            file_path = 'fluo_' + str(self.iSino) + '.edf'
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, file_path))
        elif extension == '.h5':
            file_path = 'sinogram_' + str(self.iSino) + '.h5'
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, file_path),
                                                data_path='/data/sinogram_' + str(self.iSino))
        else:
            file_info = None
        sino = structs.TxSinogram(data=data, fileInfo=file_info)
        if file_info is not None:
            sino.save()
        self._getQDSTx().txSinogramSelector.addSinogram(sino)
        self.iSino = self.iSino + 1

    def setFluoReconsMode(self, mode):
        assert(self.getReconstructionType() in (freeartconfig._ReconsConfig.FLUO_ID,
                                                freeartconfig._ReconsConfig.COMPTON_ID))
        self._getQDSFluo().setFluoReconsMode(mode)

    def _getQDSFluo(self):
        return self.mainWindow.mainWidget.getDataSourceWidget().qdsFluo

    def _getQDSTx(self):
        return self.mainWindow.mainWidget.getDataSourceWidget().qdsTx

    def _getNormWidget(self):
        return self.mainWindow.mainWidget.getNormalizationWidget()

    def _getMaterialsWidget(self):
        return self.mainWindow.mainWidget.getMaterialsWidget()

    def save(self, merge=False):
        self.mainWindow.mainWidget.saveConfiguration(self._file, merge=merge)

    def loadFileConfig(self, _file):
        assert os.path.exists(_file)
        return read(_file)

    def setIt(self, extension='.edf'):
        assert extension in (None, '.edf', '.h5')
        assert self.getReconstructionType() in (freeartconfig._ReconsConfig.FLUO_ID,
                                                freeartconfig._ReconsConfig.COMPTON_ID)
        data = numpy.random.random((self.N_PROJECTION, self.DET_X))

        if extension == '.h5':
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, 'It.h5'),
                                                data_path='/data/It')
        elif extension == '.edf':
            file_info = fileInfo.MatrixFileInfo(file_path=os.path.join(self.tempdir, 'It.edf'))
        else:
            file_info = None

        self.It = structs.Sinogram(data=data, fileInfo=file_info)
        if file_info is not None:
            self.It.save()
        self._getQDSFluo().setIt(self.It)

    def setCenterOfRotation(self, offset=0):
        self._getNormWidget().setCenterOfRotation(int(self.DET_X / 2 + offset))

    def tryToGuessMatImgBackground(self):
        self._getMaterialsWidget().tryToGuessBackground()

    def setMaterials(self):
        composition = numpy.ndarray((self.DET_X, self.DET_X), dtype='S10')
        composition[:, :] = ''
        composition[5:12, :] = 'mat1'
        materials_dict = {
            'mat1':
                OrderedDict({
                    'CompoundList': ['H', 'O'],
                    'CompoundFraction': [0.42, 0.36],
                    'Density': 1.0,
                    'Thickness': 1.0,
                    'Comment': 'wothout'
                },)
        }

        matCompFileInfo = fileInfo.MatrixFileInfo(
                file_path=os.path.join(self.tempdir, 'materials.h5'),
                data_path=structs.MatComposition.MAT_COMP_DATASET)
        matDictFileInfo = fileInfo.DictInfo(
                file_path=os.path.join(self.tempdir, 'materials.h5'),
                data_path=structs.MaterialsDic.MATERIALS_DICT)
        materials = structs.Materials(
                materials=structs.MaterialsDic(data=materials_dict,
                                               fileInfo=matDictFileInfo),
                matComposition=structs.MatComposition(data=composition,
                                                      fileInfo=matCompFileInfo))
        materials.save()
        self._getMaterialsWidget().setMaterials(materials)

    def runReconstruction(self):
        """ function equivalent of the one from
        tomogui.gui.reconstruction.ReconsManager"""
        def _deduceTxforFluoAbsMat(configFluo):
            """Deduce from a fluorescence configuration the TxConfig to be run
            in order to reconstruct the absorption matrix. In this case
            configFluo.absMat is a sinogram and not an absorption matrix yet
            """
            configTx = freeartconfig.TxConfig()
            configTx.minAngle = configFluo.minAngle
            configTx.maxAngle = configFluo.maxAngle
            configTx.center = configFluo.center
            configTx.includeLastProjection = configFluo.includeLastProjection
            configTx.useAFileForI0 = configFluo.useAFileForI0
            configTx.I0 = configFluo.I0
            configTx.solidAngleOff = configFluo.solidAngleOff
            configTx.beamCalcMethod = configFluo.beamCalcMethod
            configTx.voxelSize = configFluo.voxelSize
            configTx.projections = configFluo.projections
            configTx.definitionReduction = configFluo.definitionReduction
            configTx.projectionNumberReduction = configFluo.projectionNumberReduction
            configTx.acquiInverted = configFluo.acquiInverted
            configTx.dampingFactor = configFluo.dampingFactor
            configTx.sinograms = [
                structs.TxSinogram(name='It',
                                   fileInfo=configFluo.absMat.fileInfo,
                                   data=configFluo.absMat.data)
                ]
            return configTx

        config = self.mainWindow.mainWidget.getConfiguration(self._file)

        qt.QApplication.processEvents()
        if config.reconsType == tomoguiconfig.FBPConfig.FBP_ID:
            if has_silx_RM is True:
                return SilxReconsDialog(parent=None, cfgFile=None, config=config,
                                        platformId=platformId, deviceId=deviceId)
            else:
                msg = qt.QMessageBox()
                msg.setIcon(qt.QMessageBox.Warning)
                msg.setText('Can\'t launch FBP reconstruction(s)')
                text = 'Import fail with error: %s' % error_silx_FBP_import
                msg.setInformativeText('Can\'t run reconstruction until defined')
                msg.exec_()
                exit(0)

        # TODO: this should be removed
        for iSino, sino in enumerate(config.sinograms):
            assert config.sinograms[iSino].data is not None
            if config.sinograms[iSino].fileInfo is not None:
                config.sinograms[iSino].save()
                config.sinograms[iSino].loadData()
            assert config.sinograms[iSino].data is not None

        if config.reconsType == freeartconfig._ReconsConfig.TX_ID:
            return FreeartReconsDialog(parent=None, config=config)
        elif config.reconsType in (freeartconfig._ReconsConfig.FLUO_ID,
                                   freeartconfig._ReconsConfig.COMPTON_ID):
            # In the case we have to reconstruct the self attenuation matrix first
            if config.isAbsMatASinogram is True:
                txConfig = _deduceTxforFluoAbsMat(config)
                # run abs mat reconstruction
                widget = FreeartReconsDialog(parent=None, config=txConfig)
                widget.show()
                widget.iterate(wait=True)
                widget.close()
                qt.QApplication.processEvents()
                # update configuration to integrate the absorption matrix
                reconsAlgos = widget.mainWindow.freeartInterpreter.getReconstructionAlgorithms()
                assert (len(reconsAlgos) is 1)
                reconsPh = reconsAlgos[list(reconsAlgos.keys())[0]].getPhantom()
                config.absMat.fileInfo = None
                config.absMat.data = reconsPh
                assert (reconsPh is not None)
                config.isAbsMatASinogram = False

            return FreeartReconsDialog(parent=None, config=config)

    def _createFluoItI0Project(self, extension):
        """Function used for the 'CompleteFluo*' tests"""
        assert has_freeart is True
        _extension = extension
        self.setReconstructionType(freeartconfig._ReconsConfig.FLUO_ID)
        self.setFluoReconsMode(QDataSourceFluoWidget.GEN_ABS_SELF_ABS_OPT)
        if type(extension) in (tuple, list):
            _extension = extension[0]
        self.addNewSinogram(extension=_extension)
        if type(extension) in (tuple, list):
            _extension = extension[1]
        self.setIt(extension=_extension)
        if type(extension) in (tuple, list):
            _extension = extension[0]
        self.setI0(extension=_extension)
        self.setCenterOfRotation(offset=2)
        qt.QApplication.instance().processEvents()
        self.tryToGuessMatImgBackground()
        qt.QApplication.instance().processEvents()
        self.setMaterials()

        emptyMask = numpy.ndarray((self.DET_X, self.DET_X), dtype='S10')
        emptyMask[:, :] = ''
        self.assertFalse(numpy.array_equal(
                self._getMaterialsWidget().mainWindow.maskToolWidget._mask,
                emptyMask)
        )

    def _reconstructAbsMat(self):
        """Function used for the 'CompleteFluo*' tests"""
        widget = self.runReconstruction()
        self.assertTrue(widget.mainWindow.freeartInterpreter.config.isAbsMatASinogram is False)
        absMat = widget.mainWindow.freeartInterpreter.config.absMat.data
        self.assertFalse(numpy.array_equal(
                absMat,
                numpy.zeros(absMat.shape)))
        return widget
