# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016 European Synchrotron Radiation Facility
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
"""test that the TxConfig and FluoConfig class are correct
"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "18/10/2017"

import unittest
from .. import config, iniConfigIO, h5ConfigIO, structs, fileInfo
import tempfile
import numpy
import os
import shutil
from freeart.utils import h5utils, reconstrutils
from silx.io import configdict
from silx.io import url
from collections import OrderedDict
import silx
from silx.io import dictdump
from silx.utils.testutils import ParametricTestCase


class TestIniTx(unittest.TestCase):
    """Make sure we can read and write correctly tx configuration to the ini
    format"""
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        txSinoFile = os.path.join(self.tempdir, 'txSino.edf')

        _fileInfo = fileInfo.MatrixFileInfo(file_path=txSinoFile)
        assert _fileInfo.is_valid()
        sino = structs.TxSinogram(data=numpy.arange(100).reshape(10, 10),
                                  fileInfo=_fileInfo)
        sino.save()
        sino.loadData()
        self.txConf = config.TxConfig(
            sinograms=(sino, ),
            projections='2:6',
            minAngle=0,
            maxAngle=1.2,
            dampingFactor=1.)

        self.outFileTx = os.path.join(self.tempdir, 'tx.cfg')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def testReadWrite(self):
        writer = iniConfigIO.IniConfigWriter()
        writer.write(filePath=self.outFileTx,
                     reconsConfiguration=self.txConf)
        reader = iniConfigIO.IniConfigReader()
        confTxLoaded = reader.read(self.outFileTx)
        self.assertTrue(isinstance(confTxLoaded, config.TxConfig))
        self.assertTrue(confTxLoaded == self.txConf)


class TestIniFluo(unittest.TestCase):
    """Make sure we can read and write correctly fluo configuration to the ini
    format"""
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        fluoSinoFile = os.path.join(self.tempdir, 'fluoSino.edf')

        fluoSino = structs.FluoSino(
            fileInfo=fileInfo.MatrixFileInfo(file_path=fluoSinoFile),
            data=numpy.arange(100).reshape(10, 10),
            name='mySinogram',
            physElmt='O',
            ef=12,
            selfAbsMat=None)
        fluoSino.save()
        self.assertTrue(fluoSino.fileInfo.is_valid())

        detector = structs.Detector(x=1, y=2, z=3, width=0.1)
        absMat = structs.AbsMatrix(
            data=numpy.arange(100).reshape(10, 10),
            fileInfo=fileInfo.MatrixFileInfo(
                    file_path=os.path.join(self.tempdir, 'absMat.edf'))
        )
        assert type(absMat.fileInfo) is structs.MatrixFileInfo
        absMat.save()
        absMat.loadData()
        self.assertTrue(absMat.fileInfo.is_valid())

        self.fluoConf = config.FluoConfig(outBeamCalMethod=None,
                                          sinoI0=None,
                                          absMat=absMat,
                                          isAbsMatASinogram=True,
                                          detector=detector,
                                          minAngle=0,
                                          maxAngle=1.2,
                                          dampingFactor=1.,
                                          centerOfRotation=6.,
                                          acquiInverted=True)
        self.fluoConf.addSinogram(fluoSino)
        self.outFileFluo = os.path.join(self.tempdir, 'fluo.cfg')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def testReadWrite(self):
        writer = iniConfigIO.IniConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = iniConfigIO.IniConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)


class TestH5Tx(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.outFileTx = os.path.join(self.tempdir, 'reconsTx.h5')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def testSaveWithFilePath(self):
        """Make sure a simple tx reconstruction is saved correctly"""
        sinoFile = os.path.join(self.tempdir, 'sino.edf')
        sinogram = structs.TxSinogram(
            data=numpy.arange(100).reshape(10, 10),
            fileInfo=fileInfo.MatrixFileInfo(file_path=sinoFile),
            name='sinogramTest')
        sinogram.save()
        self.txConf = config.TxConfig(sinograms=(sinogram,),
                                      projections='2:6',
                                      minAngle=0,
                                      maxAngle=1.2,
                                      dampingFactor=1.,
                                      I0=1.0)

        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(self.outFileTx, self.txConf)

        reader = h5ConfigIO.H5ConfigReader()
        confLoaded = reader.read(self.outFileTx)
        self.assertTrue(self.txConf == confLoaded)

    def testSaveWithI0AsANumpyArray(self):
        """Make sure a tx reconstruction using a sinogram to be normalized
        is saved correctly"""
        sinogram = structs.TxSinogram(
            fileInfo=fileInfo.MatrixFileInfo(
                file_path=self.outFileTx,
                data_path='data2/test/sinogramDiffPlace'
            ),
            data=numpy.arange(100).reshape(10, 10),
            name='sinotest'
        )
        sinogram.save()
        self.assertTrue(sinogram.fileInfo.is_valid())

        infoFileI0 = fileInfo.MatrixFileInfo(
            file_path=os.path.join(self.tempdir, 'I0.edf'),
            data_slice=32)
        I0 = structs.I0Sinogram(data=numpy.arange(100).reshape(10, 10),
                                fileInfo=infoFileI0)
        I0.save()
        self.assertTrue(infoFileI0.is_valid())
        self.txConf = config.TxConfig(sinograms=(sinogram, ),
                                      projections='2:6',
                                      minAngle=0,
                                      maxAngle=1.2,
                                      dampingFactor=1.,
                                      I0=I0)
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(self.outFileTx, self.txConf)
        reader = h5ConfigIO.H5ConfigReader()
        confLoaded = reader.read(self.outFileTx)
        self.assertTrue(self.txConf.I0 == confLoaded.I0)
        self.assertTrue(self.txConf == confLoaded)


class TestH5Fluo(ParametricTestCase):
    """Make sure we can read and write correctly fluo configuration to the ini
    format"""

    NBFluoSino = 5

    def _addFluoSinograms(self, fileExtension, addSelfAbsMat=False,
                          selfAbsMat=None):
        def createFileInfo(fileExtension, name, data):
            if fileExtension is None:
                # TODO : try with official one
                # in this case all data are stored in the same .h5 file
                sourceFile = None
                path = "data/" + name + str(iSino)
                file_info = fileInfo.MatrixFileInfo(file_path=self.outFileFluo,
                                                    data_path=path)
                sourceFile = self.outFileFluo

                h5utils.createH5WithDataSet(url=file_info,
                                            data=dataSino,
                                            mode='a')

            elif fileExtension in ('.h5', '.hdf5'):
                # generate a new h5 file
                fileName = name + 'File' + str(iSino) + '.h5'
                sourceFile = os.path.join(self.tempdir, fileName)

                path = "data/" + name + str(iSino)
                _url = url.DataUrl(file_path=fileName, data_path=path)
                h5utils.createH5WithDataSet(url=_url,
                                            data=dataSino,
                                            mode='a')
                file_info = fileInfo.MatrixFileInfo(file_path=_url.file_path(),
                                                    data_path=_url.data_path())
            elif fileExtension.lower() == '.edf':
                fileName = name + 'File' + str(iSino) + '.edf'
                sourceFile = os.path.join(self.tempdir, fileName)

                file_info = fileInfo.MatrixFileInfo(file_path=sourceFile)
                reconstrutils.saveMatrix(data=dataSino, fileName=sourceFile)
            else:
                raise NotImplementedError('Not managed for other types')

            return file_info, sourceFile

        for iSino in range(self.NBFluoSino):
            dataSino = numpy.arange(100).reshape(10, 10)
            selfAbsMat = None

            fileInfoSino, sourceFileSino = createFileInfo(fileExtension,
                                                          'fluoSino',
                                                          dataSino)
            if addSelfAbsMat is True:
                dataSelfAbsMat = dataSino
                fileInfoSAM, sourceFileSAM = createFileInfo(fileExtension,
                                                            'selfAbsMat',
                                                            dataSelfAbsMat)
                selfAbsMat = structs.SelfAbsMatrix(fileInfo=fileInfoSAM,
                                                   data=dataSelfAbsMat)
            sinogram = structs.FluoSino(fileInfo=fileInfoSino,
                                        data=dataSino,
                                        name='mySinogram',
                                        physElmt='O',
                                        ef=12,
                                        selfAbsMat=selfAbsMat)
            self.fluoConf.addSinogram(sinogram)

    def _addMaterials(self, fileExtension, filePath):
        composition = numpy.arange(100).reshape(10, 10)
        materials = {
            'mat1':
                OrderedDict({
                'CompoundList': ['H', 'O'],
                'CompoundFraction': [0.42, 0.36],
                'Density': 1.0,
                'Thickness': 1.0,
                'Comment': 'wothout'
                }),
            'mat2':
                OrderedDict({
                'CompoundList': ['Y', 'O'],
                'CompoundFraction': [0.42, 0.0],
                'Density': 0.2,
                'Thickness': 0.5,
                'Comment': ''
            }),
        }
        if fileExtension is None:
            # save composition
            _url = url.DataUrl(file_path=filePath,
                               data_path=structs.MatComposition.MAT_COMP_DATASET)
            h5utils.createH5WithDataSet(url=_url,
                                        data=composition,
                                        mode='a')

            dictdump.dicttoh5(h5file=filePath,
                              treedict=materials,
                              h5path=structs.MaterialsDic.MATERIALS_DICT.lstrip("::"),
                              mode='a')
            file_info_dict = fileInfo.MatrixFileInfo(file_path=filePath,
                                                     data_path=structs.MaterialsDic.MATERIALS_DICT)
            file_info_comp = fileInfo.MatrixFileInfo(file_path=filePath,
                                                     data_path=structs.MatComposition.MAT_COMP_DATASET)
        elif fileExtension == '.h5':
            # Then both materials and materials composition are stored in the same .h5
            h5File = os.path.join(self.tempdir, 'matCompo.h5')
            path = "/data/matCompositions"
            _url = url.DataUrl(file_path=filePath, data_path=path)
            h5utils.createH5WithDataSet(url=_url,
                                        data=composition)
            file_info_comp = fileInfo.MatrixFileInfo(file_path=h5File,
                                                     data_path=path)

            h5File = os.path.join(self.tempdir, 'matDict.h5')
            path = '/materials'
            dictdump.dicttoh5(h5file=h5File,
                              treedict=materials,
                              h5path=path)

            file_info_dict = fileInfo.DictInfo(file_path=h5File,
                                               data_path=path)

        elif fileExtension == '.npy':
            npzFile = os.path.join(self.tempdir, 'matCompo.npy')
            file_info_comp = fileInfo.MatrixFileInfo(npzFile)
            numpy.save(npzFile, composition)

            dicFile = os.path.join(self.tempdir, 'matDict.dict.ini')
            tmp = configdict.ConfigDict(materials)
            tmp.write(dicFile)

            assert os.path.isfile(dicFile)
            p = dictdump.load(dicFile)
            assert(p == tmp)
            file_info_dict = fileInfo.MatrixFileInfo(dicFile)
        else:
            raise ValueError('Extansion not managed')

        self.fluoConf.materials = structs.Materials(
            materials=structs.MaterialsDic(fileInfo=file_info_dict,
                                           data=materials),
            matComposition=structs.MatComposition(fileInfo=file_info_comp,
                                                  data=composition)
        )
        self.fluoConf.materials.save()

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.outFileFluo = os.path.join(self.tempdir, 'fluo.h5')

        detector = structs.Detector(x=1, y=2, z=3, width=0.1)

        self.fluoConf = config.FluoConfig(outBeamCalMethod=None,
                                          sinoI0=None,
                                          absMat=None,
                                          isAbsMatASinogram=True,
                                          detector=detector,
                                          minAngle=0,
                                          maxAngle=1.2,
                                          dampingFactor=1.,
                                          centerOfRotation=6.,
                                          acquiInverted=True)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def testI0intSinosIncludedInH5(self):
        """Make sure the data are correctly write and read if all 
        fluorescence sinogram are stored in the same .h5 file"""
        self._addFluoSinograms(fileExtension=None)
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testI0intSinosNotIncludedInH5ButOtherH5(self):
        """Make sure all the data are correctly write and read if all
        fluorescence sinogram are stored in a different .h5 file"""
        self._addFluoSinograms(fileExtension='.h5')
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)
        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testI0intSinosNotIncludedInH5ButOtherEDF(self):
        """Make sure all the data are correctly write and read if all
        fluorescence sinogram are stored in a .edf file"""
        self._addFluoSinograms(fileExtension='.edf')
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testWithMaterialsInH5(self):
        """Test that can load and save if materials are stored in the .h5 file
        where the configuration is also store"""
        self._addMaterials(fileExtension=None, filePath=self.outFileFluo)
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)
        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))

        # ..warning:: As dictdump is not retrieving the correct types we have to update the
        # materials dict but the loaded one will keep the API of the dict
        mat = {}
        for key in confFluoLoaded.materials.materials.data:
            mat[key] = confFluoLoaded.materials.materials.data[key]
            assert("CompoundFraction" in mat[key])
            assert("CompoundList" in mat[key])
            mat[key]["CompoundFraction"] = list(mat[key]["CompoundFraction"])
            mat[key]["CompoundList"] = list(mat[key]["CompoundList"])

        confFluoLoaded.materials.materials.data = mat
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testWithMaterialsExternalH5(self):
        """Test that can load and save if materials are stored in a different
         .h5 file where the configuration is also store"""
        self._addMaterials(fileExtension='.h5', filePath=self.outFileFluo)
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))

        # ..warning:: As dictdump is not retrieving the correct types we have to update the
        # materials dict but the loaded one will keep the API of the dict
        mat = {}
        for key in confFluoLoaded.materials.materials.data:
            mat[key] = confFluoLoaded.materials.materials.data[key]
            assert("CompoundFraction" in mat[key])
            assert("CompoundList" in mat[key])
            mat[key]["CompoundFraction"] = list(mat[key]["CompoundFraction"])
            mat[key]["CompoundList"] = list(mat[key]["CompoundList"])
        confFluoLoaded.materials.materials.data = mat

        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testWithMaterialsExternalNPY(self):
        """Test that can load and save if materials are stored in a different
         .npy file and a different.dict file"""
        self._addMaterials(fileExtension='.npy', filePath=self.outFileFluo)
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        a= self.fluoConf.materials.materials
        b= confFluoLoaded.materials.materials
        confFluoLoaded.materials.loadData()

        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testWithSelfAbsMatricesIncludedInSameH5(self):
        self._addFluoSinograms(fileExtension=None,
                               addSelfAbsMat=True,
                               selfAbsMat=None)
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testWithSelfAbsMatricesIncludedInDifferentH5(self):
        # TODO : merge all selfAbsMat and fluoSinograms with subTest
        self._addFluoSinograms(fileExtension=None,
                               addSelfAbsMat=True,
                               selfAbsMat='.h5')
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)

    def testWithSelfAbsMatricesIncludedInDifferentEDF(self):
        self._addFluoSinograms(fileExtension=None,
                               addSelfAbsMat=True,
                               selfAbsMat='.edf')
        writer = h5ConfigIO.H5ConfigWriter()
        writer.write(filePath=self.outFileFluo,
                     reconsConfiguration=self.fluoConf)

        reader = h5ConfigIO.H5ConfigReader()
        confFluoLoaded = reader.read(self.outFileFluo)
        self.assertTrue(isinstance(confFluoLoaded, config.FluoConfig))
        self.assertTrue(confFluoLoaded == self.fluoConf)


def suite():
    test_suite = unittest.TestSuite()
    for t in (TestIniTx, TestIniFluo, TestH5Tx, TestH5Fluo):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(t))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
