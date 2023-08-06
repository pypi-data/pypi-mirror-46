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
__date__ = "13/08/2018"

from freeart.utils import (reconstrutils, outgoingrayalgorithm, raypointsmethod)
import freeart
from freeart.unitsystem import metricsystem
import argparse
import sys
import logging
import numpy


def getinputinfo():
    return "freeart reconsfluosino sample.edf absmat.edf selfasbmat.edf [nangles]"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sinogramfile',
                        help='file containing the fluorescence sinogram')
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
    parser.add_argument('--nangles',
                        dest="nangles",
                        type=int,
                        default=None,
                        help='number of projections')
    parser.add_argument('--halfacq',
                        dest="halfacq",
                        action="store_true",
                        default=False,
                        help='Do we want to make a sinogram from 0 to 180 or from 0 to 360 degree')
    parser.add_argument('--niter',
                        dest="niter",
                        type=int,
                        default=4,
                        help='Number of iteration to process')
    parser.add_argument('--relaxation_factor',
                        dest="relaxation_factor",
                        default=None,
                        help='Relaxation factor to apply to the ART algorithm')
    parser.add_argument('--debug',
                        dest="debug",
                        action="store_true",
                        default=False,
                        help='Set logging system in debug mode')
    options = parser.parse_args(argv[1:])
    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    _halfacq = options.halfacq

    _output = options.output
    if _output and _output.endswith('.edf') is False:
        _output = _output + '.edf'

    sinogram_file = options.sinogramfile
    assert sinogram_file.lower().endswith('.edf')
    absmat_file = options.absmatfile
    assert absmat_file.lower().endswith('.edf')
    selfabsmat_file = options.selfabsmatfile
    assert selfabsmat_file.lower().endswith('.edf')

    sinogram_data = reconstrutils.LoadEdf_2D(sinogram_file)
    sinogram_data = reconstrutils.increaseMatSize(sinogram_data, True)

    absmat_data = reconstrutils.LoadEdf_2D(absmat_file)
    absmat_data = reconstrutils.increaseMatSize(absmat_data, False)

    selfabsmat_data = reconstrutils.LoadEdf_2D(selfabsmat_file)
    selfabsmat_data = reconstrutils.increaseMatSize(selfabsmat_data, False)

    relaxation_factor = options.relaxation_factor
    if relaxation_factor is None:
        relaxation_factor = 1.0 / float(sinogram_data.shape[1])
    else:
        relaxation_factor = float(relaxation_factor)

    detPos = (1000 * metricsystem.cm, 0, 0)  # 90 degree detector
    detectorRadius = 1 * metricsystem.cm
    detSetup = [(detPos, detectorRadius)]
    oversampling = 2
    maxAngle = numpy.pi * 2.0 if _halfacq is False else numpy.pi
    angles = numpy.linspace(0.0, maxAngle, sinogram_data.shape[1])

    print('----- configuration ---')
    print('sinogram file: ', sinogram_file)
    print('absorption matrix file: ', absmat_file)
    print('self absorption mattrix file: ', selfabsmat_file)
    print('half acq: ', _halfacq)
    print('oversampling: ', oversampling)
    print('I0: ', options.i0)
    print('relaxation factor: ', relaxation_factor)
    print('nb iteration: ', options.niter)
    print('angles, from: 0 to ', maxAngle, ' nb angles: ', str(sinogram_data.shape[1]))
    print('-----------------------')
    print('start reconstruction')

    # TODO: add possibility to define the voxel size in the command line

    # run the sinogram generation
    alRecons = freeart.FluoBckProjection(sinoDat=sinogram_data,
                                         sinoAngles=angles,
                                         expSetUp=detSetup,
                                         absorp=absmat_data,
                                         selfAbsorp=selfabsmat_data)

    alRecons.setOverSampling(oversampling)
    alRecons.setDampingFactor(relaxation_factor)
    # alRecons.setRandSeedToZero(True)
    alRecons.setVoxelSize(options.voxelsize)
    alRecons.turnOffSolidAngle(True)
    alRecons.setRayPointCalculationMethod(raypointsmethod.withInterpolation)
    alRecons.setOutgoingRayAlgorithm(outgoingrayalgorithm.rawApproximation)

    phantom = alRecons.iterate(options.niter)

    if _output is not None:
        reconstrutils.saveMatrix(data=phantom, fileName=_output, overwrite=True)
        # TODO: else plot it using silx
    print('end sinogram generation')


if __name__ == "__main__":
    """
    """
    main(sys.argv)
