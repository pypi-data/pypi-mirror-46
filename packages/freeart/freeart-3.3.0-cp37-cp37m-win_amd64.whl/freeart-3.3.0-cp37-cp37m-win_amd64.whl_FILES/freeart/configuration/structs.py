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
"""
Contains some structures used for the reconstruction configuration
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "18/10/2017"

import numpy
import logging
from silx.io import configdict
from .fileInfo import MatrixFileInfo, FreeARTFileInfo, DictInfo
from freeart.utils import h5utils
from freeart.utils.reconstrutils import saveMatrix
from silx.io import dictdump

logger = logging.getLogger(__name__)


class DataStored(object):
    """
    Define a simple sinogram for his data and his storage information

    :param str h5defaultPath: the default location of this data inside a h5
                              file.
    :param name: possible tag of the data.
    :param fileInfo: information about file contained this data
    :param data: the data
    """
    def __init__(self, h5defaultPath=None, name=None, fileInfo=None, data=None):
        assert(fileInfo is None or isinstance(fileInfo, FreeARTFileInfo))
        self.h5defaultPath = h5defaultPath
        self.name = name
        self.fileInfo = fileInfo
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, DataStored):
            return False
        dataEq = numpy.all(self.data == other.data) or \
                 (self.data is None and str(other.data) == '') or \
                 (other.data is None and str(self.data) == '')
        return self.name == other.name and \
               FreeARTFileInfo._equalOrNone(self.fileInfo, other.fileInfo) and \
               dataEq

    def __str__(self):
        return "name is %s " % self.name + \
               "fileInfo is %s " % self.fileInfo + \
               "data is %s " % self.data

    def loadData(self):
        if self.fileInfo is None or self.fileInfo.file_path() is None:
            logger.debug('No file info defined, can\'t load data')
            return self.data
        else:
            assert isinstance(self.fileInfo, FreeARTFileInfo)
            if self.data is not None:
                logger.debug('existing data, will be overwrite')
            data = self.fileInfo.load()
            if data is not None:
                self.data = data
            return self.data

    def save(self):
        # assert self.fileInfo is not None
        if self.fileInfo is None:
            logger.error('No file information specified, can\'t save the data')
            return
        return self.saveTo(self.fileInfo.file_path())

    def saveTo(self, path):
        if self.data is None:
            return

        self.fileInfo = MatrixFileInfo(file_path=path,
                                       data_path=self.fileInfo.data_path())
        extension = self.fileInfo.file_path().split('.')[-1].lower()
        if extension in ('h5', 'hdf5', 'nx', 'nxs'):
            h5utils.createH5WithDataSet(url=self.fileInfo,
                                        data=self.data,
                                        mode='a')
        elif extension in ('edf', ):
            saveMatrix(data=self.data, fileName=self.fileInfo.file_path(),
                       overwrite=True)
        elif extension in ('npy', ):
            numpy.save(self.fileInfo.file_path(), self.data)
        else:
            raise ValueError('extension type (%s) not managed' % extension)


indexSino = 0


class Sinogram(DataStored):
    """
    Sinogram class
    """
    SINO_DATASET = 'data/sinogram'
    def __init__(self, h5defaultPath=None, name=None, fileInfo=None, data=None):
        _name = name
        if h5defaultPath is None:
            global indexSino
            default = self.SINO_DATASET + str(indexSino)
            if _name is None:
                _name = 'sinogram' + str(indexSino)
            indexSino += 1
        else:
            default = h5defaultPath
        if _name is None:
            _name = 'sinogram' + str(indexSino)
            indexSino += 1
        DataStored.__init__(self, h5defaultPath=default,
                            name=_name, fileInfo=fileInfo, data=data)


class I0Sinogram(Sinogram):
    """I0 sinogram"""
    I0_DATASET = "data/I0"
    """Default location of the I0 sinogram in the .h5 file"""

    def __init__(self, fileInfo=None, data=None):
        Sinogram.__init__(self, h5defaultPath=self.I0_DATASET,
                          name='I0', fileInfo=fileInfo, data=data)


indexTxSino = 0


class TxSinogram(Sinogram):
    """Transmission sinogram"""
    TX_SINOGRAM_DATASET = "data/sinogramTX"
    """Default location of the transmission sinogram in the .h5 file"""

    def __init__(self, name=None, fileInfo=None, data=None):
        global indexTxSino
        Sinogram.__init__(self, h5defaultPath=self.TX_SINOGRAM_DATASET + str(indexTxSino),
                          name=name, fileInfo=fileInfo, data=data)
        indexTxSino += 1


indexFluoSino = 0


class FluoSino(Sinogram):
    """Fluorescence sinogram"""
    FLUO_DATASET = 'data/fluo_sinogram'
    """Default location of the fluorescence sinogram in the .h5 file"""

    def __init__(self, name, fileInfo, physElmt, ef, selfAbsMat, data=None):
        global indexFluoSino
        Sinogram.__init__(self, h5defaultPath=self.FLUO_DATASET + str(indexFluoSino),
                          name=name, fileInfo=fileInfo, data=data)
        indexFluoSino += 1
        self.physElmt = physElmt
        self.EF = ef
        assert(selfAbsMat is None or isinstance(selfAbsMat, SelfAbsMatrix))
        self.selfAbsMat = selfAbsMat

    def __eq__(self, other):
        return Sinogram.__eq__(self, other) and \
               self.EF == other.EF and \
               self.physElmt == other.physElmt

    def __str__(self):
        l = 'name = %s\n' % self.name
        l += 'physElmt = %s\n' % self.physElmt
        l += 'EF = %s\n' % self.EF
        l += str(self.selfAbsMat)
        return l


indexAbsMatrix = 0
class AbsMatrix(DataStored):
    """Absorption matrix class"""
    ABS_MAT_INDEX = "data/absmatrix/absm"
    """Default location of the absorption matrix in the .h5 file"""

    def __init__(self, name=None, fileInfo=None, data=None):
        global indexAbsMatrix
        DataStored.__init__(self, h5defaultPath=self.ABS_MAT_INDEX + str(indexAbsMatrix),
                            name=name, fileInfo=fileInfo, data=data)
        indexAbsMatrix += 1


indexSelfabsMatrix = 0
class SelfAbsMatrix(AbsMatrix):
    """Self absorption matrix class"""
    SELF_ABS_MAT_INDEX = "data/selfabsmatrix/selfabsm"
    """Default location of the self absorption matrix in the .h5 file"""

    def __init__(self, name=None, fileInfo=None, data=None):
        global indexSelfabsMatrix
        DataStored.__init__(self, h5defaultPath=self.SELF_ABS_MAT_INDEX + str(indexSelfabsMatrix),
                            name=name, fileInfo=fileInfo, data=data)
        indexSelfabsMatrix += 1


class MatComposition(DataStored):
    """Material /sample composition class"""
    MAT_COMP_DATASET = "data/materials/composition"
    """Default location of the sample composition in the .h5 file"""

    def __init__(self, name=None, fileInfo=None, data=None):
        DataStored.__init__(self, h5defaultPath=self.MAT_COMP_DATASET,
                            name=name, fileInfo=fileInfo, data=data)


class MaterialsDic(DataStored, configdict.ConfigDict):
    """Materials dictionary"""
    MATERIALS_DICT = "data/materials/matDict"
    """Default location of the materials dictionary in the .h5 file"""

    def __init__(self, name=None, fileInfo=None, data=None):
        configdict.ConfigDict.__init__(self, defaultdict=data)
        DataStored.__init__(self, h5defaultPath=self.MATERIALS_DICT,
                            name=name, fileInfo=fileInfo, data=data)

    def saveTo(self, path):
        self.fileInfo = DictInfo(file_path=path,
                                 data_path=self.fileInfo.data_path())
        assert self.fileInfo.is_valid()
        extension = self.fileInfo.file_path().split('.')[-1].lower()
        if extension in ('h5', 'hdf5', 'nx', 'nxs'):
            dictdump.dicttoh5(h5file=self.fileInfo.file_path(),
                              treedict=self.data,
                              h5path=self.fileInfo.data_path() or self.MATERIALS_DICT)
        elif extension in ('ini', 'cfg'):
            dictdump.dicttoini(ddict=self.data,
                               inifile=self.fileInfo.file_path())
        else:
            raise ValueError('Extension type (%s) not managed' % extension)


class Materials(object):
    """Define a matrix with int values. Each value is associated with a fisx
     material
    """
    def __init__(self, materials=None, matComposition=None):
        assert(materials is None or isinstance(materials, MaterialsDic))
        assert(matComposition is None or isinstance(matComposition, DataStored))

        self.materials = materials
        if materials is None:
            self.materials = MaterialsDic()
        self.matComposition = matComposition
        if self.matComposition is None:
            self.matComposition = MatComposition()

    def __eq__(self, other):
        return isinstance(other, Materials) and \
               self.materials == other.materials and \
               self.matComposition == other.matComposition

    def loadData(self):
        """

        """
        def compatibilityPy2Py3():
            # insure python 2 - python 3 compatibility
            mat = {}
            for key in self.materials.data:
                mat[key] = self.materials.data[key]
                if 'Comment' in mat[key] and hasattr(mat[key]['Comment'], 'astype'):
                    mat[key]['Comment'] = mat[key]['Comment'].astype('U13')
                if "CompoundList" in mat[key] and hasattr(mat[key]["CompoundList"], 'astype'):
                    mat[key]["CompoundList"] = mat[key]["CompoundList"].astype('U13')

            self.materials.data = mat

        if(self.materials is not None and
           FreeARTFileInfo._equalOrNone(self.materials.fileInfo, None) is False and
           self.materials.fileInfo.is_valid()):
            self.materials.loadData()
            if self.materials.data:
                compatibilityPy2Py3()

        if(self.matComposition is not None and
                   FreeARTFileInfo._equalOrNone(self.matComposition.fileInfo,
                                                None) is False and
               self.matComposition.fileInfo.is_valid()):
            self.matComposition.loadData()

    def save(self):
        """Save data using the information contained in the fileInfo"""
        if(self.materials is not None and
                   FreeARTFileInfo._equalOrNone(self.materials.fileInfo, None) is False):
            self.materials.save()
        if(self.matComposition is not None and
                   FreeARTFileInfo._equalOrNone(self.matComposition.fileInfo, None) is False):
            self.matComposition.save()

    def saveTo(self, file):
        """Save data using the information contained in the fileInfo or file
        if invalid"""
        self.materials.saveTo(file)
        self.matComposition.saveTo(file)

    def __str__(self):
        l = '  - materials is \n' + str(self.materials)
        l += '\n  - composition is \n' + str(self.matComposition)
        return l


class Detector(object):
    """
    Detector class

    :param float x:
    :param float y:
    :param float z:
    :param float width:
    """
    def __init__(self, x, y, z, width):
        self.x = x
        self.y = y
        self.z = z
        self.width = width

    def toDict(self):
        return {
            'det_width': self.width,
            'det_pos_x': self.x,
            'det_pos_y': self.y,
            'det_pos_z': self.z,
        }

    def getPosition(self):
        return (self.x, self.y, self.z)

    def __str__(self):
        res = 'x=%s\n' % self.x
        res += 'y=%s\n' % self.y
        res += 'z=%s\n' % self.z
        res += 'width=%s\n' % self.width
        return res

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z \
               and self.width == other.width
