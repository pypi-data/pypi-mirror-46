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
Contains the fileInfo classes. They allow the definition of information
to retrieve data from .h5 and .edf files
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "26/10/2017"


from silx.io import url, utils
from silx.io import dictdump
import numpy
import logging

logger = logging.getLogger(__name__)


class FreeARTFileInfo(url.DataUrl):
    """
    class defining potential information for a file sinogram contained in
    a file. And a load function to retrieve the data associated with this
    information

    Now based on the silx.io.url.DataUrl
    """
    def __init__(self, file_path=None, data_path=None, data_slice=None):
        if file_path:
            if len(file_path) == 1 and ord(file_path) == 0:
                file_path = ''
            extension = file_path.split('.')[-1].lower()
        else:
            extension = None

        if extension == 'edf':
            scheme = 'fabio'
        elif extension in ('h5', 'hdf5', 'nx', 'nxs'):
            scheme = 'silx'
        else:
            scheme = None
        _data_slice = data_slice
        if isinstance(_data_slice, (int, float)):
            _data_slice = (_data_slice, )
        url.DataUrl.__init__(self, path=None, file_path=file_path,
                             data_path=data_path, data_slice=_data_slice,
                             scheme=scheme)

    @staticmethod
    def _equalOrNone(mfi1, mfi2):
        """This is not a strict comparison between self and other but this is
        needed, especially for unit test in the case an empty filePath is equal
        to a MatrixFileInfo set to None.
        :warning: Direct inheritance from url.DataUrl.__str__ is not possible
        because enter in conflict with the url.DataUrl source code.
        """
        if mfi1 is not None and mfi2 is None:
            return mfi1.file_path() in (None, '')
        elif mfi2 is not None and mfi1 is None:
            return mfi2.file_path() in (None, '')
        else:
            return mfi1 == mfi2

    def load(self):
        raise NotImplementedError()


class MatrixFileInfo(FreeARTFileInfo):
    def load(self):
        """
        load the data. First from the file set. If None register in infoFile
        then it will use the reffile.

        :return: the data contained
        """
        if self.is_valid() is False:
            err = '%s is not a valid url, cannot load data associated' % self.path
            raise ValueError(err)
        elif self.path() is None or self.file_path() in ("", None):
            return None
        else:
            if self.file_path().lower().endswith('.npy'):
                return numpy.load(self.file_path())
            else:
                try:
                    return utils.get_data(self.path())
                except ValueError as e:
                    # TODO: set it back
                    # logger.error(e)
                    return None


class DictInfo(FreeARTFileInfo):
    def load(self):
        """
        load the data. First from the file set. If None register in infoFile
        then it will use the reffile.

        :return: the data contained
        """
        if self.is_valid() is False:
            err = '%s is not a valid url, cannot load data associated' % self.path
            raise ValueError(err)
        elif self.path() is None or self.file_path() in ("", None):
            return None
        else:
            extension = self.file_path().lower().split('.')[-1]
            if extension in ('h5', 'hdf5', 'hdf', 'nx', 'nxs'):
                return dictdump.h5todict(h5file=self.file_path(),
                                         path=self.data_path())
            elif extension in ('cfg', 'ini'):
                return dictdump.load(self.file_path())
            else:
                logger.error('Extension type %s is not managed by freeart' % extension)
                return None
