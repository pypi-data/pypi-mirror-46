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

# -*- coding: utf-8 -*-

""""
 =========================================
 ============== TomoWarp II ==============
 =========================================
 ------------------------------------------
 ---- Part A - Prior Field Calculation ----
 ------------------------------------------

 ... Regular Nodes position calculator ...

 Date copied from porosity_2.py: 2013-08-20

 Authors: Edward Andò, Erika Tudisco, Stephen Hall

 This function is responsible for laying out REGULARLY SPACED calculation nodes
   within an image.

 INPUTs:
  1. Integer that defined mesh "division"
  2. 2xThree-component list of top and bottom of image
  3. Optional size of cubic window

 OUTPUTS:
  1. Prior including: 1x(Node Number), 3x(Absolute position of nodes), 2x3x(Bounding boxes))
"""
from __future__ import print_function

import numpy
#from defaults import *


def layout_nodes(div, corners, correlationHalfWindow=None):

    # 2017-01-24 EA and CC -- removed the +1 to help coax the 2D mode, Cyrille's fault!
    # Calculate positions of nodes in H
    #nodes_h = range(corners[0][0]+int(corners[1][0]%node_spacing[0])/2,corners[1][0],node_spacing[0])
    # Calculate positions of nodes in W
    #nodes_w = range(corners[0][1]+int(corners[1][1]%node_spacing[1])/2,corners[1][1],node_spacing[1])
    # Calculate positions of nodes in D
    #nodes_d = range(corners[0][2]+int(corners[1][2]%node_spacing[2])/2,corners[1][2],node_spacing[2])

    shape = numpy.array(corners[1]) - numpy.array(corners[0]) + 1
    minDim = min(shape)
    spacing = int(numpy.floor(minDim / (2**div)))
    topPadding = shape % spacing/2

    # print "corners[0]   ", corners[0]
    # print "corners[1]   ", corners[1]
    # print "shape        ", shape
    # print "minDim       ", minDim
    # print "spacing      ", spacing
    # print "shape%spacing", shape%spacing
    # print "topPadding   ", topPadding

    bins_z = numpy.array(
        range(topPadding[0]+corners[0][0], corners[1][0]+2, spacing))
    bins_y = numpy.array(
        range(topPadding[1]+corners[0][1], corners[1][1]+2, spacing))
    bins_x = numpy.array(
        range(topPadding[2]+corners[0][2], corners[1][2]+2, spacing))
    # print "bins z      ", bins_z
    # print "bins y      ", bins_y
    # print "bins x      ", bins_x

    nodes_z = (bins_z[:-1] + bins_z[1:]) / 2
    nodes_y = (bins_y[:-1] + bins_y[1:]) / 2
    nodes_x = (bins_x[:-1] + bins_x[1:]) / 2
    # print "nodes z      ", nodes_z
    # print "nodes y      ", nodes_y
    # print "nodes x      ", nodes_x

    # With our x,y,z displacement iterate and build the matrix.
    #prior = numpy.zeros((len(nodes_z) * len(nodes_y) * len(nodes_x), 10  ), dtype='<f4')
    # Add node number in first column of prior

    #nodes_rel = numpy.zeros((len(nodes_h) * len(nodes_w) * len(nodes_d), 3 ))
    nodesPositions = []
    #count = 0
    for z in range(len(nodes_z)):
        for y in range(len(nodes_y)):
            for x in range(len(nodes_x)):
                #prior[count,0] = count
                nodesPositions.append([[nodes_z[z],
                                        nodes_y[y],
                                        nodes_x[x]],
                                       [slice(nodes_z[z] - spacing/2+1, nodes_z[z] + spacing/2-1),
                                        slice(nodes_y[y] - spacing/2+1,
                                              nodes_y[y] + spacing/2-1),
                                        slice(nodes_x[x] - spacing/2+1, nodes_x[x] + spacing/2-1)]])
                #prior[count,1:3+1] = ( nodes_z[z], nodes_y[y], nodes_x[x] )
                #count += 1

    return nodesPositions
