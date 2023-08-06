  #!/usr/bin/env python
# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
# ############################################################################*/
"""
Simple application doing data.max() - data
"""

__authors__ = ["H> Payno"]
__license__ = "MIT"
__date__ = "08/08/2018"


from freeart.utils import (reconstrutils, outgoingrayalgorithm, raypointsmethod)
from freeart.unitsystem import metricsystem
import argparse
import sys
import logging
import numpy


def getinputinfo():
    return "freeart createfluosino sample.edf absmat.edf selfasbmat.edf [nangles]"



def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phantomfile',
                        help='edf file containing the sample density to generate the fluorescence sinogram')
    parser.add_argument('absmatfile',
                        help='definition of the sample absorption (in g.cm-2)')
    parser.add_argument('selfabsmatfile',
                        help='definition of the sample self attenuation (in g.cm-2)')
    parser.add_argument('--output', '-o',
                        dest="output",
                        default=None,
                        help='outputfile')
    parser.add_argument('--I0', '--i0',
                        dest="i0",
                        type=float,
                        default=1.0)
    parser.add_argument('--voxelsize',
                        dest="voxelsize",
                        type=float,
                        default=1.0*metricsystem.centimeter)
    parser.add_argument('--nangle',
                        dest="nangle",
                        type=int,
                        default=None,
                        help='number of projections')
    parser.add_argument('--center',
                        dest="center",
                        type=int,
                        default=None,
                        help='change the center once the sinogram has been created. Can only be an integer for now')
    parser.add_argument('--halfacq',
                        dest="halfacq",
                        action="store_true",
                        default=False,
                        help='Do we want to make a sinogram from 0 to 180 or from 0 to 360 degree')
    parser.add_argument('--debug',
                        dest="debug",
                        action="store_true",
                        default=False,
                        help='Set logging system in debug mode')
    options = parser.parse_args(argv[1:])

    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    _halfacq = options.halfacq
    _nangle = options.nangle
    if _nangle is None:
        _nangle = 180 if _halfacq is True else 360

    _output = options.output
    if _output and _output.endswith('.edf') is False:
        _output = _output + '.edf'

    phantom_file = options.phantomfile
    assert phantom_file.lower().endswith('.edf')
    absmat_file = options.absmatfile
    assert absmat_file.lower().endswith('.edf')
    selfabsmat_file = options.selfabsmatfile
    assert selfabsmat_file.lower().endswith('.edf')

    phantom_data = reconstrutils.LoadEdf_2D(phantom_file)
    phantom_data = reconstrutils.increaseMatSize(phantom_data, False)

    absmat_data = reconstrutils.LoadEdf_2D(absmat_file)
    absmat_data = reconstrutils.increaseMatSize(absmat_data, False)

    selfabsmat_data = reconstrutils.LoadEdf_2D(selfabsmat_file)
    selfabsmat_data = reconstrutils.increaseMatSize(selfabsmat_data, False)

    detPos = (1000*metricsystem.cm, 0, 0) # 90 degree detector
    detectorRadius = 1*metricsystem.cm
    detSetup = [(detPos, detectorRadius)]
    oversampling = 2
    
    print('----- configuration ---')
    print('phantom file: ', phantom_file)
    print('absorption matrix file: ', absmat_file)
    print('self absorption mattrix file: ', selfabsmat_file)
    print('half acq: ', _halfacq)
    print('oversampling: ', oversampling)
    print('I0: ', options.i0)
    if options.center is not None:
        print('center: ', int(options.center))
    print('-----------------------')
    print('start sinogram generation')

    # TODO: add possibility to define the voxel size in the command line

    # run the sinogram generation
    sinogram, angles = reconstrutils.makeFreeARTFluoSinogram(phantom=phantom_data,
                                                             absMat=absmat_data,
                                                             selfAbsMat=selfabsmat_data,
                                                             numAngle=_nangle,
                                                             minAngle=0.0,
                                                             maxAngle=numpy.pi if _halfacq else numpy.pi * 2.0,
                                                             turnOffSolidAngle=True,
                                                             oversampling=oversampling,
                                                             beamCalcMeth=raypointsmethod.withInterpolation,
                                                             outRayPtCalcMeth=outgoingrayalgorithm.rawApproximation,
                                                             voxelSize=options.voxelsize,
                                                             detSetup=detSetup,
                                                             I0=options.i0)
    sinogram = reconstrutils.decreaseMatSize(sinogram)
    if options.center:
        center = int(options.center)
        res = numpy.zeros((sinogram.shape[0], center * 2))
        if center * 2.0 > sinogram.shape[1]:
            res[:, center * 2 - sinogram.shape[1]:] = sinogram
        else:
            res = sinogram[:, sinogram.shape[1] / 2 - center]
        sinogram = res

    if _output is not None:
        reconstrutils.saveMatrix(data=sinogram, fileName=_output, overwrite=True)
        # TODO: else plot it using silx
    print('end sinogram generation')

if __name__ == "__main__":
    """
    """
    main(sys.argv)
