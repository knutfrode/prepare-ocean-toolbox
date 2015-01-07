#!/usr/bin/env python

# Name: get_opendap.py
# Purpose: retrieve ocean model data from an OPeNDAP server
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


import sys
import argparse
import subprocess
import datetime
import bisect

import numpy as np
from netCDF4 import Dataset, date2num, num2date

from opendap_datasets import sources

sourceNames = sources.keys()

# Check if NCO is available
try:
    subprocess.check_output('which ncks', shell=True)
except:
    sys.exit('ERROR: NCO (netCDF Operator) not available\n'
             'Please install from http://nco.sourceforge.net/')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Native arguments
    parser.add_argument('-source', dest='source',
                        default='usn-ncom', help='OPeNDAP URL to dataset '
                        'containing ocean data, or one of keyword '
                        'identifiers from file opendap_datasets.py: '
                        + str(sourceNames))

    parser.add_argument('-f', help='Output filename (netCDF)')

    # Arguments passed directly to motu-client
    parser.add_argument('-t', help='The min date with optional hour '
                        'resolution (string following format '
                        'YYYY-MM-DD [HH:MM:SS])')

    parser.add_argument('-T', help='The max date with optional hour '
                        'resolution (string following format '
                        'YYYY-MM-DD [HH:MM:SS])')

    parser.add_argument('-y', type=float, help=
                        'The min latitude (float in the interval [-90;90])')

    parser.add_argument('-Y', type=float, help=
                        'The max latitude (float in the interval [-90;90])')

    parser.add_argument('-x', type=float, help=
                        'The min longitude')

    parser.add_argument('-X', type=float, help=
                        'The max longitude')

    parser.add_argument('-z', type=str, default=0.0,
                        help='The min depth (float in the '
                        'interval [0 ; Inf])')

    parser.add_argument('-Z', type=str, default=0.0,
                        help='The max depth (float in the '
                        'interval [0 ; Inf])')

    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    try:
        url = sources[args.source]
    except:
        url = args.source
    source = args.source

    # Parse time
    if args.t is not None:
        try:  # Date and time is given
            startTime = datetime.datetime.strptime(
                args.t, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.datetime.strptime(
                args.T, '%Y-%m-%d %H:%M:%S')
        except:  # Only date is given
            try:
                startTime = datetime.datetime.strptime(
                    args.t, '%Y-%m-%d')
                endTime = datetime.datetime.strptime(
                    args.T, '%Y-%m-%d')
            except:
                print('Could not parse time: ' + str(args.t))

    # Get metadata from URL
    d = Dataset(url, 'r')
    if args.f is None:
        print '=================================================='
        print d
    print '=================================================='

    # Get dimensions and their vectors
    for dimName in d.dimensions:
        print dimName
        dimvals = d.variables[dimName][:]
        if dimName == 'time':
            dimvals = num2date(dimvals, units=d.variables[dimName].units)
            if args.t is None:  # Return first time steps, if time not given
                startTime = dimvals[-2]
                endTime = dimvals[-1]
            if startTime > dimvals[-1] or endTime < dimvals[0]:
                sys.exit('Requested time span (%s - %s) not covered '
                         'by dataset (%s - %s)' %
                         (startTime, endTime, dimvals[0], dimvals[-1]))
            timeIndexStart = bisect.bisect_left(dimvals, startTime)
            timeIndexEnd = bisect.bisect_right(dimvals, endTime)
            timeIndexStart = np.maximum(timeIndexStart, 0)
            timeIndexEnd = np.minimum(timeIndexEnd, len(dimvals)-1)
        if dimName == 'depth':
            print str(dimvals)
            hasDepth = True
        else:
            print '\t' + str(dimvals[0]) + ' (min)'
            print '\t' + str(dimvals[-1]) + ' (max)'
        if dimName == 'lon':
            if args.x is None:
                args.x = dimvals[0]
                args.X = dimvals[1]
        if dimName == 'lat':
            if args.y is None:
                args.y = dimvals[0]
                args.Y = dimvals[1]

    # Print available parameters
    print '\nParameters (CF standard name):'
    for varName in d.variables:
        try:
            standard_name = d.variables[varName].standard_name
            print '\t' + varName + ' (' + standard_name + ')'
        except:
            print '\t' + varName

    d.close()

    # Suggest command, if filename is not given
    if args.f is not None:
        # Subsetting in time and space
        subset = ' -d lon,%.2f,%.2f -d lat,%.2f,%.2f -d time,%i,%i' % \
            (args.x, args.X, args.y, args.Y, timeIndexStart, timeIndexEnd)
        if 'hasDepth' in locals():
            args.z = np.float(args.z)
            args.Z = np.float(args.Z)
            subset = subset + ' -d depth,%.2f,%.2f ' % (args.z, args.Z)
        out = ' -o out.nc '
        ncoCommand = 'ncks ' + subset + out + url + ' --overwrite'
        ncoCommand = ncoCommand + ' -o ' + args.f
        print ncoCommand
        subprocess.call(ncoCommand, shell=True)
        #subprocess.call('ncdump out.nc -v lon|tail -3', shell=True)
        #subprocess.call('ncdump out.nc -v lat|tail -3', shell=True)
    else:
        templateCommand = '%s -source %s -t \'%s\' -T \'%s\' ' \
                          ' -x %s -X %s -y %s -Y %s -f %s' % \
                          (sys.argv[0], source, startTime, endTime,
                           args.x, args.X, args.y, args.Y, 'out.nc')
        if 'hasDepth' in locals():
            templateCommand = templateCommand + \
                ' -z %s -Z %s ' % (args.z, args.Z)
        print '---------------------------------------------------------'
        print 'Template command for data download (cut, paste and edit):'
        print templateCommand
        print '========================================================='
