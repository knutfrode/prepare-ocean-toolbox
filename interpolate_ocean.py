#!/usr/bin/env python

# Name: interpolate_ocean.py
# Purpose: interpolate netCDF file to another map projection
# Author: Knut-Frode Dagestad (knutfd@met.no)
# Created: Dec 2014
# Copyright: (c) MET Norway 2014
# Licence:
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# http://www.gnu.org/licenses/gpl-3.0.html
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import os
import sys
import argparse
import datetime
import subprocess

# Check if NCO is available
try:
    subprocess.check_output('which fimex', shell=True)
except:
    sys.exit('ERROR: Fimex not available\n'
             'Please install from https://wiki.met.no/fimex/start')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', dest='inputFilename',
                        help='Input filename', required=True)
    parser.add_argument('-o', dest='outputFilename',
                        help='Output filename', required=True)
    parser.add_argument('-proj4', help='proj4 string describing a spatial '
                        'reference system onto which the data will be '
                        'projected. See http://trac.osgeo.org/proj/wiki/FAQ '
                        'for reference', required=True)
    parser.add_argument('-r', dest='resolution', default=10000,
                        help='Spatial resolution of destination grid [m]')
    parser.add_argument('-v', dest='rotatevectors', default='latlon',
                        choices=('latlon', 'grid'),
                        help='Axis directions for vector components')

    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if not os.path.exists(args.inputFilename):
        sys.exit('Input file does not exist: ' + args.inputFilename)

    fimexString = ("/vol/fou/emep/People/heikok/fimexTrunk/bin/fimex "
                   " --input.file %s --output.file %s " %
                   (args.inputFilename, args.outputFilename))
    fimexString += " --interpolate.projString \'" + args.proj4 + "\'"
    fimexString += " --interpolate.xAxisUnit m --interpolate.yAxisUnit m "
    resolutionString = '0,%s,...,x;relativeStart=0\'' % (args.resolution)
    fimexString += " --interpolate.xAxisValues='" + resolutionString
    fimexString += " --interpolate.yAxisValues='" + resolutionString
    fimexString += " --process.rotateVector.direction=" + args.rotatevectors
    fimexString += " --process.rotateVector.all"

    print fimexString
    os.system(fimexString)
