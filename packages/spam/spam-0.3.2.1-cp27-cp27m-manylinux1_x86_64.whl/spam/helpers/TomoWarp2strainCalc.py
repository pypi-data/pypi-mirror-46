#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016, Erika Tudisco, Edward Andò, Stephen Hall, Rémi Cailletaud

# This file is part of TomoWarp2.
#
# TomoWarp2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TomoWarp2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TomoWarp2.  If not, see <http://www.gnu.org/licenses/>.

# ===================================================================
# ===========================  TomoWarp2  ===========================
# ===================================================================

# Authors: Erika Tudisco, Edward Andò, Stephen Hall, Rémi Cailletaud

from __future__ import print_function

import os
import sys
import getopt
import numpy


class Bunch(dict):
    def __init__(self, kw):
        dict.__init__(self, kw)
        self.__dict__ = self

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self


def help_process_results():
    print('Use: tomowarp_process_results [options] <inputfile>')
    print('  -o  --output_name   output file prefix (Default: "DIC")')
    print('  -p  --prefix        output file prefix (Default: "DIC")')
    print('  -d  --dir-out       output diretcory (Default: directory of the input file)')
    print('  -T  --saveTIFF      save outputs as TIFF files (Default = False)')
    print('  -R  --saveRAW       save outputs as RAW  files (Default = False)')
    print('  -V  --saveVTK       save outputs as VTK  files (Default = False)')
    print('  -c  --cc-threshold  threshold for the correlation coefficient')
    print('                      can be a number, "auto" (Default: none)')
    print('      --no-strain     if specified strains are not calculated')
    print('      --kinematics_median_filter')
    print('                      kinematics are median filtered, with their nearest neighbours.')
    print('                      Smoothed fields are output, and strain is calculated on smoothed fields.')
    print('                      (can improve strain results a lot).')
    print('                      Default = 0, good option = 3 (means one neighbour in each direction).')
    print('      --correct_pixel_size')
    print('                      correction for pixel size changing as:')
    print(
        '                      [pixel_size_ratio, image_centre_z, image_centre_y, image_centre_x]')
    print('      --strain_mode')
    print('                      Whether strains should be calculated in the "largeStrains" or "smallStrains"')
    print('                      or "largeStrainsCentred". "largeStrains" is recommended, and is default')
    print('      --nomask')
    print('                      Don\'t mask the data with return status.')

# 2017-03-09 EA and JD: Process results in current form takes a data object which needs to be created,
#   So we're importing "Bunch" and trying to create it on the fly.


# Make sure prints come out straight away
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


if __name__ == "__main__":
    sys.path.append(os.path.join(
        os.path.dirname(__file__), "./TomoWarp2-libs"))
    from process_results import process_results

    argv = sys.argv[1:]
    if len(argv) == 0:
        help_process_results()
        sys.exit(2)
    try:
        opts, args = getopt.gnu_getopt(argv, "hp:o:d:c:RTV", ["prefix=", "output_name=" "dir-out=", "cc-threshold=",
                                                              "no-strain", "kinematics_median_filter=", "correct_pixel_size=",
                                                              "strain_mode=", "saveRAW", "saveTIFF", "saveVTK", "nomask", "oldTSV"])
    except getopt.GetoptError as e:
        print(str(e))
        help_process_results()
        sys.exit(2)

    file_kinematics = args[0]

    data = {}
    data['output_name'] = os.path.basename(file_kinematics[0:-4])
    data['cc_threshold'] = None
    data['calculate_strain'] = True
    data['saveTIFF'] = False
    data['saveRAW'] = False
    data['saveVTK'] = False
    data['kinematics_median_filter'] = 0
    data['remove_outliers_filter_size'] = 0
    data['remove_outliers_threshold'] = 2
    data['remove_outliers_absolut_threshold'] = False
    data['remove_outliers_filter_high'] = True
    data['strain_mode'] = "largeStrains"

    # 2015-04-23 EA: adding defaults for kinematics output
    data['saveDispl'] = True
    data['saveRot'] = False
    data['saveRotFromStrain'] = False
    data['saveError'] = False
    data['saveCC'] = False
    data['saveMask'] = False
    data['saveStrain'] = [True, True, True, True, True, True, True, True]
    data['images_2D'] = False
    data['mask'] = True
    #data['oldTSV'] = False

    if len(args) != 1:
        help_process_results()
        sys.exit(2)

    data['DIR_out'] = os.path.dirname(file_kinematics)
    if not data['DIR_out']:
        data['DIR_out'] = "."

    for opt, arg in opts:
        if opt == '-h':
            help_process_results()
            sys.exit()
        elif opt in ("-p", "--prefix", "-o", "--output_name"):
            data['output_name'] = arg
        elif opt in ("-T", "--saveTIFF"):
            data['saveTIFF'] = True
        elif opt in ("-R", "--saveRAW"):
            data['saveRAW'] = True
        elif opt in ("-V", "--saveVTK"):
            data['saveVTK'] = True
        elif opt in ("-d", "--dir-out"):
            data['DIR_out'] = arg
        elif opt in ("-c", "--cc-threshold"):
            data['cc_threshold'] = arg
        elif opt in ("--nomask"):
            data['mask'] = False
        #elif opt in ("--oldTSV"):
        #    data['oldTSV'] = True
        elif opt in ("--no-strain"):
            data['calculate_strain'] = False
        elif opt in ("--kinematics_median_filter"):
            data['kinematics_median_filter'] = int(float(arg))
        elif opt in ("--strain_mode"):
            if arg == "smallStrains" or arg == "largeStrains" or arg == 'tetrahedralStrains' or arg == 'largeStrainsCentred':
                data['strain_mode'] = arg
                print("tomowarp_process_results(): Strain mode {} selected".format(
                    data['strain_mode']))

    #print("  -> Reading a kinematics field...")
    #if not data['oldTSV']:
    #    kinematics = numpy.genfromtxt(file_kinematics, names=True, delimiter="\t")[
    #        ["NodeNumber", "Zpos", "Ypos", "Xpos", "F14", "F24", "F34", "SubPixDeltaFnorm", "SubPixReturnStat"]]
    #else:
    #    kinematics = numpy.genfromtxt(file_kinematics, names=True, delimiter="\t")[
    #        ["NodeNumber", "Zpos", "Ypos", "Xpos", "Zdisp", "Ydisp", "Xdisp", "SubPixError", "SubPixReturnStat"]]
    #    # rename titles
    #    kinematics.dtype.names = ("NodeNumber", "Zpos", "Ypos", "Xpos",
    #                              "F14", "F24", "F34", "SubPixDeltaFnorm", "SubPixReturnStat")

    print("  -> Reading a kinematics field...")
    try:
        kinematics = numpy.genfromtxt(file_kinematics, names=True, delimiter="\t")[
            ["NodeNumber", "Zpos", "Ypos", "Xpos", "Zdisp", "Ydisp", "Xdisp", "SubPixDeltaFnorm", "SubPixReturnStat"]]
    except ValueError:
        kinematics = numpy.genfromtxt(file_kinematics, names=True, delimiter="\t")[
            ["NodeNumber", "Zpos", "Ypos", "Xpos", "F14", "F24", "F34", "SubPixDeltaFnorm", "SubPixReturnStat"]]
        # rename titles
        kinematics.dtype.names = ("NodeNumber", "Zpos", "Ypos", "Xpos", "Zdisp", "Ydisp", "Xdisp", "SubPixDeltaFnorm", "SubPixReturnStat")


    # Create data object
    data = Bunch(data)

    process_results(kinematics, data)
