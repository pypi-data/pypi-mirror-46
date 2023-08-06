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
Contains the python representation of the reconstruction parameters
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "18/10/2017"


from freeart.unitsystem import metricsystem
from silx.io import url
from silx.io import configdict
import numpy
import time
try:
    from freeart import version
except:
    version = ''
from . import structs, fileInfo
import os


class _ReconsConfig(object):

    TX_ID = "Transmission"
    COMPTON_ID = "Compton"
    FLUO_ID = "Fluorescence"

    RECONS_TYPES = [TX_ID, COMPTON_ID, FLUO_ID]

    PRECISION_TO_TYPE = {
        'simple': numpy.float32,
        'double': numpy.float64
    }

    reconsParams = None
    """
    The reconstruction parameters (oversampling...) to launch once configured
    """

    def __init__(self, reconsType=None, minAngle=None, maxAngle=None,
                 projections=None, defReduction=1, projNumReduction=1,
                 oversampling=1, solidAngleOff=False,
                 includeLastProjection=True, I0=None, beamCalcMethod=0,
                 centerOfRotation=-1, acquiInverted=False, precision='double'):
        """

        :param reconsType:
        :param centerOfRotation: if -1 then will take the middle
        :param precision: calcul precision, can be simple or double.
        """
        if reconsType not in _ReconsConfig.RECONS_TYPES:
            raise ValueError('reconsType not recognized')
        if minAngle is not None and not (0 <= minAngle <= 2.*numpy.pi):
            raise ValueError('min angle not in [0, 2pi]')
        if minAngle is not None and not (0 <= maxAngle <= 2.*numpy.pi):
            raise ValueError('max angle not in [0, 2pi]')
        if (minAngle is not None or maxAngle is not None) and not minAngle <= maxAngle:
            raise ValueError('False condition: minAngle <= maxAngle')

        self.precision = precision
        assert self.precision in self.PRECISION_TO_TYPE
        self.reconsType = reconsType
        self.center = centerOfRotation
        self.projections = projections
        """The projections to be consider for the reconstruction"""
        self.definitionReduction = defReduction
        """
        Should we take a pixel each definition_reduction for the reconstruction
        """
        self.projectionNumberReduction = projNumReduction
        """
        Should we take one projection each projection_number_reduction for the
         reconstruction.
        """
        self.voxelSize = metricsystem.cm
        """voxel size"""
        self.oversampling = oversampling
        """Oversampling value"""
        self.solidAngleOff = solidAngleOff
        """Should we always set the the value of the solid angle to 1"""
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.includeLastProjection = includeLastProjection
        self.setI0(I0)
        self.beamCalcMethod = beamCalcMethod
        self.acquiInverted = acquiInverted

    def setI0(self, I0):
        if type(I0) is str or (hasattr(I0, 'dtype') and numpy.issubdtype(I0.dtype,
                                                                   numpy.character)):
            self._I0 = structs.I0Sinogram()
            _url = url.DataUrl(path=I0)
            if _url.file_path():
                file_extension = _url.file_path().split('.')[-1]
            else:
                file_extension = ''
            if file_extension.lower() == 'edf':
                self._I0.fileInfo = fileInfo.MatrixFileInfo(file_path=_url.file_path(),
                                                            data_slice=_url.data_slice())
                assert self._I0.fileInfo.is_valid()
            elif file_extension.lower() in ('h5', 'hdf5', 'nx', 'nxs'):
                self._I0.fileInfo = fileInfo.MatrixFileInfo(file_path=_url.file_path(),
                                                            data_path=_url.data_path())
                assert self._I0.fileInfo.is_valid()
            self.useAFileForI0 = True
        elif isinstance(I0, structs.I0Sinogram):
            self._I0 = I0
            self.useAFileForI0 = True
        else:
            self._I0 = 1.0 if I0 is None else I0
            self.useAFileForI0 = False

    def getI0(self):
        return self._I0

    I0 = property(getI0, setI0)

    def toDict(self):
        """Convert the configuration to a silx ConfigDict"""
        dic = configdict.ConfigDict()
        dic['general_settings'] = self._getGeneralSettings()
        dic['normalization'] = self._getNormalization()
        dic['reconstruction_properties'] = self._getReconsProp()
        dic['reduction_data'] = self._getReductionDataInfo()
        dic['projection_information'] = self._getProjInfo()
        return dic

    def _getGeneralSettings(self):
        return {
            'reconstruction_type': self.reconsType,
            'date ': str(time.strftime("%d/%m/%Y")),
            'freeart_version': version,
            'precision': self.precision
        }

    def _getNormalization(self):
        if isinstance(self.I0, structs.DataStored):
            if self.I0.fileInfo is None:
                i0_out = ''
            else:
                i0_out = self.I0.fileInfo.path()
        else:
            i0_out = self.I0
        return {
            'rotation_center': self.center,
            'normalizationi0fromafile': self.useAFileForI0,
            'i0': i0_out,
        }

    def _getReconsProp(self):
        return {
            'voxel_size': self.voxelSize,
            'oversampling': self.oversampling,
            'bean_calculation_method': self.beamCalcMethod,
            'solid_angle_is_off': self.solidAngleOff,
            'include_last_angle': self.includeLastProjection
        }

    def _getReductionDataInfo(self):
        return {
            'definition_reducted_by': self.definitionReduction,
            'projection_number_reducted_by': self.projectionNumberReduction,
        }

    def _getProjInfo(self):
        return {
            'min_angle': self.minAngle,
            'max_angle': self.maxAngle,
            'projections_sel': self.projections or ':',
            'acqui_inv': self.acquiInverted
        }

    def _fromDict(self, dict):
        """set the configuration fron a silx ConfigDict"""
        self._setGenSettingFrmDict(dict)
        self._setNormalizationFrmDict(dict)
        self._setReconsPropFrmDict(dict)
        self._setReducDataFrmDict(dict)
        self._setProjInfoFrmDict(dict)
        return self

    def _setGenSettingFrmDict(self, dict):
        assert('general_settings' in dict)
        assert('reconstruction_type' in dict['general_settings'])
        self.reconsType = dict['general_settings']['reconstruction_type']
        if type(self.reconsType) is not str:
            self.reconsType = str(self.reconsType.tostring().decode())
        assert('precision' in dict['general_settings'])
        self.precision = dict['general_settings']['precision']
        if type(self.precision) is not str:
            self.precision = str(self.precision.tostring().decode())

    def _setNormalizationFrmDict(self, dict):
        assert('normalization' in dict)
        info = dict['normalization']
        assert('rotation_center' in info)
        assert('i0' in info)
        self.center = info['rotation_center']
        i0 = info['i0']
        if hasattr(i0, 'dtype') and not numpy.issubdtype(i0.dtype, numpy.number):
            i0 = str(i0.tostring().decode())
        self.setI0(i0)

    def _setReconsPropFrmDict(self, dict):
        assert('reconstruction_properties' in dict)
        info = dict['reconstruction_properties']
        assert('voxel_size' in info)
        assert('oversampling' in info)
        assert('bean_calculation_method' in info)
        assert('solid_angle_is_off' in info)
        assert('include_last_angle' in info)
        self.voxelSize = float(info['voxel_size'])
        self.oversampling = int(info['oversampling'])
        self.beamCalcMethod = int(info['bean_calculation_method'])
        self.solidAngleOff = bool(info['solid_angle_is_off'])
        self.includeLastProjection = bool(info['include_last_angle'])

    def _setReducDataFrmDict(self, dict):
        assert('reduction_data' in dict)
        info = dict['reduction_data']
        assert('definition_reducted_by' in info)
        assert('projection_number_reducted_by' in info)
        self.definitionReduction = info['definition_reducted_by']
        self.projectionNumberReduction = info['projection_number_reducted_by']

    def _setProjInfoFrmDict(self, dict):
        assert('projection_information' in dict)
        info = dict['projection_information']
        assert('min_angle' in info)
        assert('max_angle' in info)
        assert('projections_sel' in info)
        assert('acqui_inv' in info)
        self.minAngle = info['min_angle']
        self.maxAngle = info['max_angle']
        self.projections = info['projections_sel']
        if not type(self.projections) is str:
            self.projections = str(self.projections.tostring().decode())
        self.acquiInverted = bool(info['acqui_inv'])

    def __eq__(self, other):
        projectionsAreEqual = self.projections == other.projections or \
            self.projections is None and other.projections == ':' or \
            self.projections == ':' and other.projections is None

        return self.reconsType == other.reconsType and \
               self.maxAngle == other.maxAngle and \
               self.minAngle == other.minAngle and \
               self.I0 == other.I0 and \
               self.center == other.center and \
               self.includeLastProjection == other.includeLastProjection and \
               self.useAFileForI0 == other.useAFileForI0 and \
               self.solidAngleOff == other.solidAngleOff and \
               self.beamCalcMethod == other.beamCalcMethod and \
               self.voxelSize == other.voxelSize and \
               self.definitionReduction == other.definitionReduction and \
               projectionsAreEqual and \
               self.projectionNumberReduction == other.projectionNumberReduction and \
               self.acquiInverted == other.acquiInverted and \
               self.precision == other.precision


    def __str__(self):
        res = 'reconsType is %s \n' % self.reconsType
        res = res + 'oversampling is %s \n' % self.oversampling
        res = res + 'minAngle is %s \n' % self.minAngle
        res = res + 'maxAngle is %s \n' % self.maxAngle
        res = res + 'I0 is %s \n' % self.I0
        res = res + 'center is %s \n' % self.center
        res = res + 'includeLastProjection is %s \n' % self.includeLastProjection
        res = res + 'useAFileForI0 is %s \n' % self.useAFileForI0
        res = res + 'solidAngleOff is %s \n' % self.solidAngleOff
        res = res + 'beamCalcMethod is %s \n' % self.beamCalcMethod
        res = res + 'voxelSize is %s \n' % self.voxelSize
        res = res + 'definitionReduction is %s \n' % self.definitionReduction
        res = res + 'projections is %s \n' % self.projections
        res = res + 'acquiInverted is %s \n' % self.acquiInverted
        res = res + 'projectionNumberReduction is %s \n' % self.projectionNumberReduction
        return res

    def setFileInfoToH5File(self, refFile, save=False):
        """
        Change all the fileInfo to point ot the given h5 file

        :param refFile: the h5 file to store information
        :param save: if true once the file info updated, save the dataset
        """
        assert fileInfo
        fn, file_extension = os.path.splitext(refFile)
        assert file_extension in ('.hdf5', '.hdf', '.h5')
        if self.I0 is not None and self.useAFileForI0 is True:
            self.I0.loadData()
            self.I0.fileInfo = fileInfo.MatrixFileInfo(file_path=refFile,
                                                       data_path=structs.I0Sinogram.I0_DATASET)
            if save is True:
                self.I0.save()


class _ItReconsConfig(_ReconsConfig):
    """Define parameters needed for an iterative reconstruction

    :param dampingFactor: if the dampingFactor is None then will be deduced
                          automatically
    """
    def __init__(self, dampingFactor=None, *var, **kw):
        _ReconsConfig.__init__(self, *var, **kw)
        self.dampingFactor = dampingFactor

    def _getReconsProp(self):
        dict = _ReconsConfig._getReconsProp(self)
        dict['relaxation_factor'] = self.dampingFactor
        return dict

    def _setReconsPropFrmDict(self, dict):
        _ReconsConfig._setReconsPropFrmDict(self, dict)
        assert('relaxation_factor' in dict['reconstruction_properties'])
        self.dampingFactor = dict['reconstruction_properties']['relaxation_factor']

    def __eq__(self, other):
        return _ReconsConfig.__eq__(self, other) and self.dampingFactor == other.dampingFactor


class _SimpleSinoConfig(_ItReconsConfig):
    def __init__(self, reconsType, sinograms=None, computeLog=True, *var, **kw):
        _ItReconsConfig.__init__(self, *var, reconsType=reconsType, **kw)
        self.sinograms = []
        """list of sinograms to be reconstructed"""
        if sinograms:
            for sinogram in sinograms:
                assert isinstance(sinogram, self._defaultSinoType())
                self.addSinogram(sinogram)

    def addSinogram(self, sinogram):
        if sinogram is None:
            return
        elif isinstance(sinogram, self._defaultSinoType()):
            _sinogram = sinogram
        # case of h5 file
        elif type(sinogram) is str or (hasattr(sinogram, 'dtype') and
                                           numpy.issubdtype(sinogram.dtype, numpy.character)):
            _sinogram = self._defaultSinoType()()
            # Raw check for hdf5 file
            if '::' in str(sinogram):
                _sinogram.fileInfo = fileInfo.MatrixFileInfo(file_path=str(sinogram))
            else:
                _sinogram.fileInfo = fileInfo.MatrixFileInfo(file_path=str(sinogram))
        else:
            _sinogram = self._defaultSinoType()()
            _sinogram.data = sinogram

        assert isinstance(_sinogram, self._defaultSinoType())
        self.sinograms.append(_sinogram)

    def _defaultSinoType(self):
        return structs.Sinogram

    def setFileInfoToH5File(self, refFile, save=False):
        """
        Change all the fileInfo to point ot the given h5 file

        :param refFile: the h5 file to store information
        :param save: if true once the file info updated, save the dataset
        """
        _ItReconsConfig.setFileInfoToH5File(self, refFile, save)
        for _sinogram in self.sinograms:
            had_data = self.data is not None
            _sinogram.loadData()
            has_data = self.data is not None
            # assert had_data == has_data or had_data is False
            _sinogram.fileInfo = fileInfo.MatrixFileInfo(file_path=refFile,
                                                         data_path=_sinogram.h5defaultPath)
            has_data = self.data is not None
            # assert had_data == has_data or had_data is False

            if save is True:
                _sinogram.save()
                has_data = self.data is not None
                # assert had_data == has_data or had_data is False

    def toDict(self):
        dic = _ItReconsConfig.toDict(self)
        dic[self._getDataSourceHeader()] = self._getDataSourceInfo()
        self._sinogramsToDict(dic)
        return dic

    def _sinogramsToDict(self, dic):
        sinogramsDict = self.getSinogramsFileDict()
        for iSinoFile, sinoFile in enumerate(sinogramsDict):
            index = 0
            section = 'sino_file_' + str(iSinoFile)
            dic[section] = {}
            for sinogram in sinogramsDict[sinoFile]:
                assert isinstance(sinogram, self._defaultSinoType())
                if sinogram.fileInfo is not None:
                    url = sinogram.fileInfo.path()
                    dic[section]['sino_url_' + str(index)] = url
                    dataNameID = 'data_name_' + str(index)
                    dic[section][dataNameID] = sinogram.name
                    index += 1
        return dic

    def _getDataSourceHeader(self):
        return 'data_source_tx'

    def _getDataSourceInfo(self):
        return {}

    def _fromDict(self, dict):
        _ItReconsConfig._fromDict(self, dict)
        self._sinogramsFromDict(dict)
        return self

    def _sinogramsFromDict(self, dict):
        iFile = 0
        section = 'sino_file_' + str(iFile)
        while section in dict:
            index = 0
            info = dict[section]
            sino_url = 'sino_url_' + str(index)
            while sino_url in dict[section]:
                fileUrl = info[sino_url]
                if not type(fileUrl) is str:
                    fileUrl = str(fileUrl.tostring().decode())

                _url = url.DataUrl(path=fileUrl)
                dataNameID = 'data_name_' + str(index)
                name = info[dataNameID]
                if hasattr(name, 'astype'):
                    name = str(name.astype('U13'))
                _fileInfo = structs.MatrixFileInfo(file_path=_url.file_path(),
                                                   data_path=_url.data_path())
                self.addSinogram(sinogram=structs.TxSinogram(name=name,
                                                             fileInfo=_fileInfo))
                index += 1
                sino_url = 'sino_url_' + str(index)

            iFile += 1
            section = 'sino_file_' + str(iFile)

    def __eq__(self, other):
        return _ItReconsConfig.__eq__(self, other) and \
               self.getSinogramsFileDict() == other.getSinogramsFileDict()

    def checkSinoType(self, sino):
        assert(isinstance(sino, structs.Sinogram))

    def getSinogramsFileDict(self):
        """
        return the sinograms as a dictionnary with key the file containing the
        sinograms and values the list of sinograms in this file

        :return: dict
        """
        dd = {}
        for sinogram in self.sinograms:
            assert isinstance(sinogram, structs.Sinogram)
            filePath = 'unknow'
            if sinogram.fileInfo and sinogram.fileInfo.file_path():
                filePath = sinogram.fileInfo.file_path()
            if filePath not in dd:
                dd[filePath] = []
            dd[filePath].append(sinogram)
        import collections
        sortedDict = collections.OrderedDict(sorted(dd.items()))
        return sortedDict

    def fillSinogramNames(self):
        # if no name define, define one for each sinogram
        if self.sinograms is not None:
            index = 0
            for sinogram in self.sinograms:
                if sinogram.name is None:
                    sinogram.name = 'sinogram_' + str(index)
                    index += 1


class TxConfig(_SimpleSinoConfig):
    """

    .. note:: Need to get a differentiation between TxConfig and this class
              because tomogui has also to deal with the FBP... and won't have the log
              option and maybe others
    """
    def __init__(self, sinograms=None, computeLog=True, *var, **kw):
        _SimpleSinoConfig.__init__(self, reconsType=self.TX_ID,
                                   sinograms=sinograms, *var, **kw)
        self.computeLog = computeLog

    def _setNormalizationFrmDict(self, dict):
        _SimpleSinoConfig._setNormalizationFrmDict(self, dict)
        assert('normalization' in dict)
        info = dict['normalization']
        assert('computeminuslog' in info)
        self.computeLog = info['computeminuslog']

    def _getNormalization(self):
        dic = _SimpleSinoConfig._getNormalization(self)
        dic['computeminuslog'] = self.computeLog
        return dic

    def __eq__(self, other):
        return _SimpleSinoConfig.__eq__(self, other) and \
               self.computeLog == other.computeLog


class FluoConfig(_SimpleSinoConfig):
    """
    configuration to build fluorescence or compton reconstruction algorithm
    """
    def __init__(self, outBeamCalMethod=0, sinoI0=None, absMat=None,
                 isAbsMatASinogram=False, detector=None, materials=None,
                 sinograms=None, e0=1, *var, **kw):
        _SimpleSinoConfig.__init__(self, reconsType=self.FLUO_ID, *var, **kw)
        assert(absMat is None or isinstance(absMat, structs.AbsMatrix))
        self.absMat = absMat
        if self.absMat is None:
            self.absMat = structs.AbsMatrix(fileInfo=None)

        # TODO: check: not sure I0 is used
        self.sinoI0 = sinoI0
        self.isAbsMatASinogram = isAbsMatASinogram

        assert(materials is None or isinstance(materials, structs.Materials))
        self.materials = materials
        if self.materials is None:
            self.materials = structs.Materials()
        self.detector = detector
        self.outBeamCalMethod = outBeamCalMethod
        self.E0 = e0

    def _defaultSinoType(self):
        return structs.FluoSino

    def _getDataSourceHeader(self):
        return 'data_source_fluo'

    def toDict(self):
        dic = _SimpleSinoConfig.toDict(self)
        dic['detector_setup'] = self._getDetector()
        return dic

    def _sinogramsToDict(self, dic):
        # deal with all fluorescence sinogram
        sinogramsDict = self.getSinogramsFileDict()
        for iSinoFile, sinoFile in enumerate(sinogramsDict):
            section = 'fluo_sino_file_' + str(iSinoFile)
            dic[section] = {}
            indexSino = 0
            for sino in sinogramsDict[sinoFile]:
                fluoSinoUrlID = 'fluo_sino_url_' + str(indexSino)
                dic[section][fluoSinoUrlID] = sino.fileInfo.path()

                dataNameID = 'data_name_' + str(indexSino)
                dic[section][dataNameID] = sino.name

                dataPhysElmtID = 'data_physical_element_' + str(indexSino)
                dic[section][dataPhysElmtID] = sino.physElmt

                EFID = 'ef_' + str(indexSino)
                dic[section][EFID] = sino.EF

                selfAbsMatID = 'self_absorption_file_' + str(indexSino)

                if sino.selfAbsMat is None:
                    dic[section][selfAbsMatID] = ''
                else:
                    assert(isinstance(sino.selfAbsMat, structs.AbsMatrix))
                    assert(sino.selfAbsMat.fileInfo is not None)
                    dic[section][selfAbsMatID] = sino.selfAbsMat.fileInfo.path()

                indexSino += 1

        return dic

    def _fromDict(self, dict):
        _SimpleSinoConfig._fromDict(self, dict)
        assert('detector_setup' in dict)
        info = dict['detector_setup']
        assert('det_width' in info)
        assert('det_pos_x' in info)
        assert('det_pos_y' in info)
        assert('det_pos_z' in info)

        self.detector = structs.Detector(x=info['det_pos_x'],
                                         y=info['det_pos_y'],
                                         z=info['det_pos_z'],
                                         width=info['det_width'])

        # deal with data_source_fluo
        assert('data_source_fluo' in dict)
        info = dict['data_source_fluo']
        self.isAbsMatASinogram = bool(info['absorption_file_is_a_sinogram'])
        absMat = info['absorption_file']
        info_file_abs_mat = _getMatrixFileInfo(absMat)

        if fileInfo.MatrixFileInfo._equalOrNone(info_file_abs_mat, None):
            self.absMat = structs.AbsMatrix()
        else:
            self.absMat = structs.AbsMatrix(fileInfo=info_file_abs_mat)

        materialCompoFile = info['samp_composition_file']
        info_file_comp = _getMatrixFileInfo(materialCompoFile)

        materialsFile = info['materials_file']
        info_file_mat_dic = _getDictFileInfo(materialsFile)

        self.materials = structs.Materials(
            materials=structs.MaterialsDic(fileInfo=info_file_mat_dic),
            matComposition=structs.MatComposition(fileInfo=info_file_comp))

        return self

    def _sinogramsFromDict(self, dict):
        """
        Create list(struct.FluoSino) from dictionnary containing the
        configuration

        :param dict: configuration dictionnary
        """
        iFile = 0
        section = 'fluo_sino_file_' + str(iFile)
        while section in dict:
            info = dict[section]
            indexSino = 0

            sinoUrlID = 'fluo_sino_url_' + str(indexSino)
            while sinoUrlID in info:
                dataNameID = 'data_name_' + str(indexSino)
                dataPhysElmtID = 'data_physical_element_' + str(indexSino)
                EFID = 'ef_' + str(indexSino)
                selfAbsMatID = 'self_absorption_file_' + str(indexSino)
                # deal with sinogram
                sinoFile = info[sinoUrlID]
                file_info = _getMatrixFileInfo(sinoFile)

                # deal with selfAbsMat
                selfAbsMatFile = info[selfAbsMatID] if selfAbsMatID in info else None
                absMatInfo = _getMatrixFileInfo(selfAbsMatFile)

                if fileInfo.MatrixFileInfo._equalOrNone(absMatInfo, None):
                    selfAbsMat = None
                else:
                    selfAbsMat = structs.SelfAbsMatrix(fileInfo=absMatInfo)
                    assert selfAbsMat.fileInfo.is_valid()

                name = info[dataNameID]
                if hasattr(name, 'astype'):
                    name = str(name.astype('U13'))
                physElmt = info[dataPhysElmtID]

                if hasattr(physElmt, 'astype'):
                    physElmt = str(physElmt.astype('U13'))
                # create the fluorescence sinogram
                fluoSino = structs.FluoSino(name=name, fileInfo=file_info,
                                            physElmt=physElmt, ef=info[EFID],
                                            selfAbsMat=selfAbsMat)
                try:
                    fluoSino.loadData()
                except:
                    pass
                self.addSinogram(fluoSino)
                indexSino += 1
                sinoUrlID = 'fluo_sino_url_' + str(indexSino)

            iFile += 1
            section = 'fluo_sino_file_' + str(iFile)

    def _getDataSourceInfo(self):
        assert(type(self.isAbsMatASinogram) is bool)
        compoFile = matFile = None
        if self.materials is not None:
            if(self.materials.matComposition is not None and
                       self.materials.matComposition.data is not None):
                if fileInfo.FreeARTFileInfo._equalOrNone(self.materials.matComposition.fileInfo, None) is False:
                    compoFile = self.materials.matComposition.fileInfo.path()
                    assert (isinstance(self.materials.matComposition, structs.MatComposition))

            if(self.materials.materials is not None and
                       self.materials.materials.data is not None and
                       len(self.materials.materials.data) > 0):
                if fileInfo.FreeARTFileInfo._equalOrNone(self.materials.materials.fileInfo, None) is False:
                    assert(isinstance(self.materials.materials, structs.MaterialsDic))
                    assert(isinstance(self.materials.materials.fileInfo, fileInfo.FreeARTFileInfo))
                    matFile = self.materials.materials.fileInfo.path()

        absMatFile = ''
        if(self.absMat is not None and
               fileInfo.FreeARTFileInfo._equalOrNone(self.absMat.fileInfo, None) is False):
            absMatFile = self.absMat.fileInfo.path()

        return {
            'absorption_file_is_a_sinogram': self.isAbsMatASinogram,
            'absorption_file': absMatFile,
            'samp_composition_file': compoFile or '',
            'materials_file': matFile or '',
        }

    def _getReconsProp(self):
        dic = _ItReconsConfig._getReconsProp(self)
        dic['outgoing_bean_calculation_method'] = self.outBeamCalMethod or 0
        dic['e0'] = self.E0
        return dic

    def _setReconsPropFrmDict(self, dict):
        _ItReconsConfig._setReconsPropFrmDict(self, dict)
        assert('outgoing_bean_calculation_method' in dict['reconstruction_properties'])
        self.outBeamCalMethod = dict['reconstruction_properties']['outgoing_bean_calculation_method']
        assert('e0' in dict['reconstruction_properties'])
        self.E0 = dict['reconstruction_properties']['e0']

    def _getDetector(self):
        if self.detector is None:
            return structs.Detector(x=None,
                                    y=None,
                                    z=None,
                                    width=None).toDict()
        else:
            return self.detector.toDict()

    def setFileInfoToH5File(self, refFile, save=False):
        """
        Change all the fileInfo to point ot the given h5 file

        :param refFile: the h5 file to store information
        :param save: if true once the file info updated, save the dataset
        """
        def dealWithSinograms():
            if self.sinograms:
                sinograms = []
                for sino in self.sinograms:
                    sino.loadData()
                    assert sino.data is not None
                    sino.fileInfo = fileInfo.MatrixFileInfo(file_path=refFile,
                                                            data_path=sino.h5defaultPath)
                    assert sino.data is not None

                    if save is True:
                        sino.save()
                        assert sino.data is not None

                    if(sino.selfAbsMat is not None and
                       fileInfo.FreeARTFileInfo._equalOrNone(sino.selfAbsMat.fileInfo, None) is False):
                        sino.selfAbsMat.loadData()
                        sino.selfAbsMat.fileInfo = fileInfo.MatrixFileInfo(file_path=refFile,
                                                                           data_path=sino.selfAbsMat.h5defaultPath)
                        if save is True:
                            sino.selfAbsMat.save()
                sinograms.append(sino)
                self.sinograms = sinograms

        def dealWithMaterials():
            if self.materials:
                if self.materials.materials:
                    if(fileInfo.FreeARTFileInfo._equalOrNone(self.materials.materials.fileInfo, None) is False):
                        if self.materials.materials.data is None:
                            try:
                                self.materials.materials.loadData()
                            except:
                                pass
                        self.materials.materials.fileInfo = fileInfo.MatrixFileInfo(file_path=refFile,
                                                                                    data_path=structs.MaterialsDic.MATERIALS_DICT)
                    if save is True:
                        self.materials.materials.save()
                if self.materials.matComposition is not None:
                    if(fileInfo.FreeARTFileInfo._equalOrNone(self.materials.matComposition.fileInfo, None) is False):
                        if self.materials.matComposition.data is None:
                            try:
                                self.materials.matComposition.loadData()
                            except:
                                pass
                        self.materials.matComposition.fileInfo = fileInfo.MatrixFileInfo(
                                file_path=refFile,
                                data_path=structs.MatComposition.MAT_COMP_DATASET)
                    if save is True:
                        self.materials.matComposition.save()

        def dealWithAbsMat():
            if self.absMat:
                if(fileInfo.FreeARTFileInfo._equalOrNone(self.absMat.fileInfo, None) is False):
                    if self.absMat.data is None:
                        try:
                            self.absMat.loadData()
                        except:
                            pass
                    self.absMat.fileInfo = fileInfo.MatrixFileInfo(file_path=refFile,
                                                                   data_path=self.absMat.h5defaultPath)
                if save is True:
                    self.absMat.save()


        _ItReconsConfig.setFileInfoToH5File(self, refFile, save)
        dealWithSinograms()
        dealWithMaterials()
        dealWithAbsMat()

    def __eq__(self, other):
        return _SimpleSinoConfig.__eq__(self, other) and \
               self.detector == other.detector and \
               self.absMat == other.absMat and \
               self.isAbsMatASinogram == other.isAbsMatASinogram

    def __str__(self):
        l = _ItReconsConfig.__str__(self)
        l += 'outgoing beam calculation meth = %s\n' % self.outBeamCalMethod
        l += str(self.materials)
        return l

    def checkSinoType(self, sino):
        assert(isinstance(sino, structs.FluoSino))


def retrieveInfoFile(file, index):
    """Simple function to get the adapted infoFile from a file and
    an index

    :param file: the file storing the data
    :param index: int or str location of the data in the file
    """
    assert type(file) is str
    if file == '' or file is None or ord(file[0]) == 0:
        return None
    assert(type(file) is str)
    info_file = None
    if file.lower().endswith('.h5') or file.lower().endswith('.hdf5'):
        fp = str(file) + '::' + str(index)
        info_file = fileInfo.MatrixFileInfo(file_path=fp)
    elif file.lower().endswith('.npy') or file.lower().endswith('.dict') or file.lower().endswith('.ini'):
        info_file = fileInfo.MatrixFileInfo(file_path=file)
    elif file.lower().endswith('.edf'):
        if index == '' or index is None:
            _index = 0
        else:
            _index = int(index)
        info_file = fileInfo.MatrixFileInfo(file_path=str(file), data_slice=int(_index))
    else:
        raise ValueError('extension not managed (%s)' % os.path.basename(file))
    return info_file


def _getMatrixFileInfo(_str):
    assert type(_str) in (type(None), str, numpy.ndarray)
    if hasattr(_str, 'tostring'):
        _str = str(_str.tostring().decode())
    if _str in (None, ''):
        return fileInfo.MatrixFileInfo()
    else:
        _url = url.DataUrl(path=_str)
        return fileInfo.MatrixFileInfo(file_path=_url.file_path(),
                                       data_path=_url.data_path())


def _getDictFileInfo(_str):
    assert type(_str) in (type(None), str, numpy.ndarray)
    if hasattr(_str, 'tostring'):
        _str = str(_str.tostring().decode())
    if _str in (None, ''):
        return fileInfo.DictInfo()
    else:
        _url = url.DataUrl(path=_str)
        return fileInfo.DictInfo(file_path=_url.file_path(),
                                 data_path=_url.data_path())
