#!/usr/bin/env python

# Name: get_myocean.py
# Purpose: download ocean model data from MyOcean
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
import inspect
import argparse
import datetime
import xml.etree.ElementTree as ET

from myocean_datasets import sources, username, password

# Find path to the motu-client bundled with this package
motu_client_name = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))) + \
    '/motu-client-python/motu-client.py'

# Get names of the (MyOcean) regions/oceans
regions = [source['name'] for source in sources]

# Only these relevant parameters are listed
relevantParameters = ['sea_water_salinity',
                      'sea_water_potential_temperature',
                      'eastward_sea_water_velocity',
                      'northward_sea_water_velocity',
                      'x_sea_water_velocity',
                      'y_sea_water_velocity',
                      'sea_water_x_velocity',
                      'sea_water_y_velocity',
                      'sea_surface_height_above_sea_level',
                      'sea_surface_elevation',
                      'sea_surface_height',
                      'sea_ice_area_fraction',
                      'sea_ice_thickness']

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Native arguments
    parser.add_argument('-region', dest='region',
                        default='global', help='The following regions '
                        'are available (see myocean_datasets.py): '
                        + str(regions))

    parser.add_argument('-reanalysis', action='store_true', default=False,
                        help='For reanalysis data, otherwise using '
                        'analysis/forecast')

    parser.add_argument('-f', dest='f', help='Output filename (netCDF)')

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
                        'The min longitude (float in the interval [-180;180])')

    parser.add_argument('-X', type=float, help=
                        'The max longitude (float in the interval [-180;180])')

    parser.add_argument('-z', type=str, default='Surface',
                        help='The min depth (float in the '
                        'interval [0 ; Inf] or string "Surface")')

    parser.add_argument('-Z', type=str, default='Surface',
                        help='The max depth (float in the '
                        'interval [0 ; Inf] or string "Surface")')

    parser.add_argument('-v', dest='v', help='The variable (list of strings)',
                        action='append')

    parser.add_argument('-user', dest='user', default=username,
                        help='MyOcean username')

    parser.add_argument('-pass', dest='pwd', default=password,
                        help='MyOcean password')

    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args, extraArgs = parser.parse_known_args()
    if args.user == '' or args.pwd == '' or args.pwd == 'my-passwd':
        sys.exit('Please provide Myocean username/passord' +
                 ' on commandline, or store in myocean_datasets.py')

    # Loop to obtain metadata for the requested region/source
    for source in sources:
        if source['name'] == args.region:
            if args.reanalysis is True:
                fs = source['reanalysis']
            else:
                fs = source['forecast']
    try:
        fs
    except:
        print 'No datasets for region ' + args.region
        print 'Available regions: ' + str(regions)
        sys.exit(1)
    region = args.region
    del args.region

    # Construct motu-arguments for selected dataset
    args.m = fs['motuClient']  # motu server
    args.s = fs['serviceID']  # service id
    args.d = fs['datasets'][0]  # dataset id
    if (
        region == 'baltic' or region == 'global' or (
            region == 'northwestshelf' and args.reanalysis is False) or (
            region == 'southwestshelf')
    ):
        xml2terminal = True
    else:
        xml2terminal = False

    motuCoreString = motu_client_name + ' -m %s -s %s -d %s -u %s -p %s ' % (
        args.m, args.s, args.d, args.user, args.pwd)

    # Download and display metadata if no output filename is given
    if args.f is None:
        xmlFile = 'metadata.txt'
        string = motuCoreString + ' -D '
        if xml2terminal:
            string = string + ' 1> ' + xmlFile
        else:
            string = string + ' -f ' + xmlFile
        # Download metadata to xml file
        os.system(string)
        # Read metadata xml file into string
        fp = open(xmlFile)
        xml = fp.read()
        fp.close()
        # Display metadata nicely formatted
        print '===================================================='
        if xml2terminal:
            xml = xml[xml.find('following:')+12:-3]
        root = ET.fromstring(xml)
        # Time
        times = root.find('timeCoverage')
        startTime = times.attrib['start'].split('.')[0].split('+')[0]
        endTime = times.attrib['end'].split('.')[0].split('+')[0]
        try:
            startTime = datetime.datetime.strptime(
                startTime, '%Y-%m-%dT%H:%M:%S')
            endTime = datetime.datetime.strptime(
                endTime, '%Y-%m-%dT%H:%M:%S')
        except:
            startTime = datetime.datetime.strptime(
                startTime, '%Y-%m-%d')
            endTime = datetime.datetime.strptime(
                endTime, '%Y-%m-%d')
        print 'Time start: ' + str(startTime)
        print 'Time end: ' + str(endTime)
        # Depths
        try:
            depths = root.find('availableDepths')
            print 'Depths:\n\t' + depths.text
            depths = depths.text.split(';')
        except:
            depths = ['Surface', 'Surface']
        # Axes
        axes = root.find('dataGeospatialCoverage')
        print 'Axes:'
        for axis in axes:
            desc = axis.attrib['name']
            if desc != 'time' and desc != 'depth':
                print '\t%s:\n\t\t%s (min)\n\t\t%s (max)' % (
                    desc, axis.attrib['lower'], axis.attrib['upper'])
            if desc == 'lat' or desc == 'latitude' or desc == 'nav_lat_v':
                latmin = axis.attrib['lower']
                latmax = axis.attrib['upper']
            if desc == 'lon' or desc == 'longitude' or desc == 'nav_lon_v':
                lonmin = axis.attrib['lower']
                lonmax = axis.attrib['upper']
        print 'Parameters (CF standard_name):'
        variables = root.find('variables')
        variableList = []
        for variable in variables:
            parameterName = variable.attrib['name']
            standardName = variable.attrib['standardName']
            print '\t' + parameterName + ' (' + standardName + ')'
            if standardName in relevantParameters:
                variableList.append(parameterName)
        templateCommand = '%s -region %s -t %s -T %s -z %s -Z %s ' \
                          ' -x %s -X %s -y %s -Y %s' % \
                          (sys.argv[0], region,
                           endTime - datetime.timedelta(days=1), endTime,
                           depths[0], depths[1],
                           lonmin, lonmax, latmin, latmax)
        if args.reanalysis:
            templateCommand = templateCommand + ' -reanalysis '
        for variable in variableList:
            templateCommand = templateCommand + ' -v ' + variable
        templateCommand = templateCommand + ' -f data.nc'
        print '---------------------------------------------------------'
        print 'Template command for data download (cut, paste and edit):'
        print templateCommand
        print '========================================================='
        sys.exit()

    # Download data, by passing appropriate arguments to the motu-client

    # Delete arguments specific for this script
    del args.reanalysis
    del args.m
    del args.s
    del args.d
    del args.user
    del args.pwd
    args.o = os.path.dirname(args.f)
    if args.o == '':
        args.o = '.'
    args.f = os.path.basename(args.f)
    print '='*40
    motuString = motuCoreString
    for parameter in args.__dict__:
        value = args.__dict__[parameter]
        if parameter == 'v':
            for val in value:
                motuString = motuString + ' -v ' + val
            continue
        if value is not None and value is not '':
            motuString = motuString + ' -' + parameter + ' ' + str(value)

    print motuString
    os.system(motuString)
