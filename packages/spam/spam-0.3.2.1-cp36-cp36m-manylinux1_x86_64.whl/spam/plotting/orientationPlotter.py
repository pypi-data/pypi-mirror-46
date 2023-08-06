#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Edward Ando 17/11/2011
#
# Attempt at programming rose plots myself.

# Assuming that the contacts are kind of flat, and so the normal vector pointing up from them is correct
# which means using Visilog's Orientation 2 vectors.

# Modified in order to allow vector components to be taken as input directly

# 2012.08.27 - adding ability to output projected components, in order to allow plotting
#   with gnuplot

# Completely new version with objective of:
#   - reading in different formats (3D coordinates (x,y,z,), Spherical Coordinates, Cylindrical)
#   - outputting any other format
#   - Different projections onto the plane (Lambert, Stereo, direct, etc...)
#   - Possibility to colour the negative part of the projected sphere in a different colour
#   - Projection point-by-point or binned with Hugues Talbot and Clara's code, which
#       gives the very convenient cutting of the circle into in equal area parts:
#         Jaquet, C., Andò, E., Viggiani, G., & Talbot, H. (2013).
#         Estimation of separating planes between touching 3D objects using power watershed.
#         In Mathematical Morphology and Its Applications to Signal and Image Processing (pp. 452-463).
#         Springer Berlin Heidelberg.

# Internal data format will be x,y,z sphere, with x-y defining the plane of projection.

# 2015-07-24 -- EA and MW -- checking everything, there were many bugs -- the points were only plotted to an extent of 1 and not radiusMax
#               created plotting function, which allows radius labels to be updated.

# 2016-11-08 -- MW -- binning was still erroneous. an angularBin (lines 348ff) was usually put to the next higher bin, so not rounded correctly
#               rounding now with numpy.rint and if the orientation doesn't belong to the last bin, it has to be put in the first one
#                 as the first bin extends to both sides of 0 Degrees. -> check validation example in lines 227ff

# 2017-06-01 -- MW -- updating for the current numpy version 1.12.1 and upgrading matplotlib to 2.0.2

# 2017-06-26 -- MW -- there still was a small bug in the binning: for the angular bin numpy.rint was used -- replaced it with numpy.floor (line 375)
#                     benchmarking points are in lines 217ff.

# 2018-02-19 -- EA -- changes in the new matplot version revealed a problem. Eddy solved it for the spam client, MW modified this one here.

# 2018-04-20 -- MW -- adding relative bin counts -- to normalise the bincounts by the average overall bin count.
#                     enables to plot many states with the same legend!

from __future__ import print_function

import os
import sys
import numpy
import random
import math
import matplotlib
import matplotlib.pyplot

VERBOSE = False

# ask numpy to print 0.000 without scientific notation
numpy.set_printoptions(suppress=True)
numpy.set_printoptions(precision=3)


def SaffAndKuijlaarsSpiral( N ):
    """
        There is no analytical solution for putting equally-spaced points on a sphere.
        This spiral gets close.

        Parameters
        ----------

        N : integer
            Number of points to generate

        Returns
        -------
        orientations : Nx3 numpy array
            Z,Y,X unit vectors of orientations for each point on sphere

        Note
        ----------
        For references, see
        http://www.cgafaq.info/wiki/Evenly_distributed_points_on_sphere

        Which in turn was based on
        http://sitemason.vanderbilt.edu/page/hmbADS

        From
        Rakhmanov, Saff and Zhou: **Minimal Discrete Energy on the Sphere**, Mathematical Research Letters, Vol. 1 (1994), pp. 647-662:
        https://www.math.vanderbilt.edu/~esaff/texts/155.pdf

        Also see discussion here
        http://groups.google.com/group/sci.math/browse_thread/thread/983105fb1ced42c/e803d9e3e9ba3d23#e803d9e3e9ba3d23%22%22
    """
    M = int(N)*2
    
    s         = 3.6 / math.sqrt(M)
    
    delta_z   = 2 / float(M)
    z         = 1 - delta_z/2
    
    longitude = 0
    
    points = numpy.zeros( (N,3) )
    
    for k in range( N ):
        r           = math.sqrt( 1 - z*z )
        points[k,2] = math.cos( longitude ) * r
        points[k,1] = math.sin( longitude ) * r 
        points[k,0] = z
        z           = z - delta_z
        longitude   = longitude + s/r
    return points



def _projectOrientations( projection, coordSystem, vector ):
    #           1. type of projection
    #                        2. coordinate system (XYZ, or spherical)
    #                                    3. input 3-unit vector, or array:
    #                                       for x-y-z that order is maintained
    #                                       for spherical: r, theta (inclination), phi (azimuth)
    
    # Returns: projection_xy, projection_theta_r
    
    projection_xy_local      = numpy.zeros( (2) )
    projection_theta_r_local = numpy.zeros( (2) )
    
    if coordSystem == "spherical":
        # unpack vector 
        r, theta, phi = vector
        
        x = r * math.sin( theta ) * math.cos( phi )
        y = r * math.sin( theta ) * math.sin( phi )
        z = r * math.cos( theta )
        
    else:
        # unpack vector 
        x, y, z = vector
        # we're in cartesian coordinates, (x-y-z mode) Calculate spherical coordinates
        # passing to 3d spherical coordinates too...
        # From: https://en.wikipedia.org/wiki/Spherical_coordinate_system
        #  Several different conventions exist for representing the three coordinates, and for the order in which they should be written.
        #  The use of (r, θ, φ) to denote radial distance, inclination (or elevation), and azimuth, respectively, is common practice in physics, 
        #   and is specified by ISO standard 80000-2 :2009, and earlier in ISO 31-11 (1992).
        r     = numpy.sqrt( x**2 + y**2 + z**2 )
        theta = math.acos( z / r )   # inclination
        phi   = math.atan2( y, x )   # azimuth
      
    if projection == "lambert":          #                            dividing by sqrt(2) so that we're projecting onto a unit circle
        projection_xy_local[0] = x*( math.sqrt(2/(1+z)) )
        projection_xy_local[1] = y*( math.sqrt(2/(1+z)) )
        
        # sperhical coordinates -- CAREFUL as per this wikipedia page: https://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection
        #   the symbols for inclination and azimuth ARE INVERTED WITH RESPEST TO THE SPHERICAL COORDS!!!
        projection_theta_r_local[0] = phi
        #                                                  HACK: doing math.pi - angle in order for the +z to be projected to 0,0
        projection_theta_r_local[1] = 2 * math.cos( ( math.pi - theta ) / 2 )
        
        # cylindrical coordinates
        #projection_theta_r_local[0] = phi
        #projection_theta_r_local[1] = math.sqrt( 2.0 * ( 1 + z ) )
        

        
    if projection == "stereo":
        projection_xy_local[0] = x / ( 1 - z )
        projection_xy_local[1] = y / ( 1 - z )
        
        # https://en.wikipedia.org/wiki/Stereographic_projection uses a different standard from the page on spherical coord Spherical_coordinate_system
        projection_theta_r_local[0] = phi
        #                                        HACK: doing math.pi - angle in order for the +z to be projected to 0,0
        #                                                                             HACK: doing math.pi - angle in order for the +z to be projected to 0,0
        projection_theta_r_local[1] = numpy.sin( math.pi - theta ) / ( 1 - numpy.cos( math.pi - theta ) )
        
    if projection == "equidistant":
        # https://en.wikipedia.org/wiki/Azimuthal_equidistant_projection
        # TODO: To be checked, but this looks like it should -- a straight down projection.
        projection_xy_local[0] = math.sin( phi )
        projection_xy_local[1] = math.cos( phi )
        
        projection_theta_r_local[0] = phi
        projection_theta_r_local[1] = numpy.cos( theta - math.pi/2 )
    
    return projection_xy_local, projection_theta_r_local


def plotOrientations( orientations_zyx,
                    projection="lambert",
                    plot="both",
                    binValues={"min":None, "max":None},
                    binNormalisation = False,
                    numberOfRings = 9,
                    # the size of the dots in the points plot (5 OK for many points, 25 good for few points/debugging)
                    pointMarkerSize = 8,
                    cmap = matplotlib.pyplot.cm.RdBu_r,
                    title = "",
                    subtitle = {"points":"",
                                "bins":""},
                    saveFigPath = None ):
    """
        Main function for plotting 3D orientations.
        This function plots orientations (described by unit-direction vectors) from a sphere onto a plane.

        One useful trick for evaluating these orientations is to project them with a "Lambert equal area projection", which means that an isotropic distribution of angles is projected as equally filling the projected space.

        Parameters
        ----------
        orientations : Nx3 numpy array of floats
            Z, Y and X components of direction vectors.
            Non-unit vectors are normalised.

        projection : string, optional
            Selects different projection modes:
                **lambert** : Equal-area projection, default and highly reccommended. See https://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection

                **equidistant** : equidistant projection

        plot : string, optional
            Selects which plots to show:
                **points** : shows projected points individually
                **bins** : shows binned orientations with counts inside each bin as colour
                **both** : shows both representations side-by-side, default

        title : string, optional
            Plot main title. Default = ""

        subtitle : dictionary, optional
            Sub-plot titles:
                **points** : Title for points plot. Default = ""
                **bins** : Title for bins plot. Default = ""

        binValues : dictionary, optional
            Dictionary defining the colour-bar limits for bin view:
                **min** : Mininun value to be shown, default = None (`i.e.`, auto-set)
                **max** : Maximum value to be shown, default = None (`i.e.`, auto-set)

        binNormalisation : bool, optional
            In binning mode, should bin counts be normalised by mean counts on all bins
            or absoulte counts?

        cmap : matplotlib colour map, optional
            Colourmap for number of counts in each bin in the bin view.
            Default = ``matplotlib.pyplot.cm.RdBu_r``

        numberOfRings : int, optional
            Number of rings (`i.e.`, radial bins) for the bin view.
            The other bins are set automatically to have uniform sized bins using an algorithm from Jacquet and Tabot.
            Default = 9 (quite small bins)

        pointMarkerSize : int, optional
            Size of points in point view.
            Default = 8 (quite big points)

        saveFigPath : string, optional
            Path to save figure to -- stops the graphical plotting.
            Default = None

        Returns
        -------
        None -- A matplotlib graph is created and show()n

        Note
        ----
        Authors: Edward Andò, Hugues Talbot, Clara Jacquet and Max Wiebicke
    """
    import matplotlib.pyplot
    # ========================================================================
    # ==== Reading in data, and formatting to x,y,z sphere                 ===
    # ========================================================================
    numberOfPoints = orientations_zyx.shape[0]

    # ========================================================================
    # ==== Check that all the vectors are unit vectors                     ===
    # ========================================================================
    if VERBOSE: print( "\t-> Normalising all vectors in x-y-z representation..." ),

    # from http://stackoverflow.com/questions/2850743/numpy-how-to-quickly-normalize-many-vectors
    norms = numpy.apply_along_axis( numpy.linalg.norm, 1, orientations_zyx )
    orientations_zyx = orientations_zyx / norms.reshape( -1, 1 )

    if VERBOSE: print( "done." )

    # ========================================================================
    # ==== At this point we should have clean x,y,z data in memory         ===
    # ========================================================================
    if VERBOSE: print( "\t-> We have %i orientations in memory."%( numberOfPoints ) )

    # Since this is the final number of vectors, at this point we can set up the 
    #   matrices for the projection.
    projection_xy       = numpy.zeros( (numberOfPoints, 2) )

    # TODO: Check if there are any values less than zero or more that 2*pi
    projection_theta_r  = numpy.zeros( (numberOfPoints, 2) )

    # ========================================================================
    # ==== Projecting from x,y,z sphere to the desired projection          ===
    # ========================================================================
    # TODO: Vectorise this...
    for vectorN in range( numberOfPoints ):
        # unpack 3D x,y,z
        z,y,x = orientations_zyx[ vectorN ]
        #print "\t\txyz = ", x, y, z

        # fold over the negative half of the sphere
        #     flip every component of the vector over
        if z < 0: z = -z; y = -y; x = -x

        projection_xy[ vectorN ], projection_theta_r[ vectorN ] = _projectOrientations( projection, "xyz", [x,y,z] )

    # get radiusMax based on projection
    #                                    This is only limited to sqrt(2) because we're flipping over the negative side of the sphere
    if projection == "lambert":         radiusMax = numpy.sqrt(2)
    elif projection == "stereo":        radiusMax = 1.0
    elif projection == "equidistant":   radiusMax = 1.0

    if VERBOSE: print( "\t-> Biggest projected radius (r,t) = {}".format( numpy.abs( projection_theta_r[:,1] ).max() ) )

    #print "projection_xy\n", projection_xy
    #print "\n\nprojection_theta_r\n", projection_theta_r


    if plot == "points" or plot == "both":
        fig = matplotlib.pyplot.figure()
        fig.suptitle( title )
        if plot == "both":
          ax  = fig.add_subplot( 121, polar=True )
        else:
          ax  = fig.add_subplot( 111, polar=True)

        ax.set_title( subtitle['points']+"\n" )

        # set the line along which the numbers are plotted to 0°
        #ax.set_rlabel_position(0)
        matplotlib.pyplot.axis( ( 0, math.pi*2, 0, radiusMax ) )

        # set radius grids to 15, 30, etc, which means 6 numbers (r=0 not included)
        radiusGridAngles = numpy.arange( 15, 91, 15 )
        radiusGridValues = []
        for angle in radiusGridAngles:
            #                        - project the 15, 30, 45 as spherical coords, and select the r part of theta r-
            #               - append to list of radii -
            radiusGridValues.append( _projectOrientations( projection, "spherical", [ 1, angle*math.pi/180.0, 0 ] )[1][1] )
        #                                       --- list comprehension to print 15°, 30°, 45° ----------
        ax.set_rgrids( radiusGridValues, labels=[ "%02i$^\circ$"%(x) for x in numpy.arange(  15,91,15) ], angle=None, fmt=None )
        ax.plot( projection_theta_r[:,0], projection_theta_r[:,1] , '.', markersize=pointMarkerSize )

        if plot == "points":
          matplotlib.pyplot.show()


    if plot == "bins" or plot == "both":
        # ========================================================================
        # ==== Binning the data -- this could be optional...                   ===
        # ========================================================================
        # This code inspired from Hugues Talbot and Clara Jaquet's developments.
        # As published in:
        #   Identifying and following particle-to-particle contacts in real granular media: an experimental challenge
        #   Gioacchino Viggiani, Edward Andò, Clara Jaquet and Hugues Talbot
        #   Keynote Lecture
        #   Particles and Grains 2013 Sydney
        #
        # ...The number of radial bins (numberOfRings)
        # defines the radial binning, and for each radial bin starting from the centre, 
        # the number of angular bins is  4(2n + 1)
        # 
        import matplotlib.patches
        #from matplotlib.colors import Normalize
        import matplotlib.colorbar
        import matplotlib.collections

        if plot == "both":
            ax  = fig.add_subplot( 122, polar=True )
        if plot == "bins":
            fig = matplotlib.pyplot.figure()
            ax  = fig.add_subplot( 111, polar=True)

        if VERBOSE: print( "\t-> Starting Data binning..." )

        # This must be an integer -- could well be a parameter if this becomes a function.
        if VERBOSE: print( "\t-> Number of Rings (radial bins) = ", numberOfRings )


        # As per the publication, the maximum number of bins for each ring, coming from the inside out is 4(2n + 1):
        numberOfAngularBinsPerRing = numpy.arange( 1, numberOfRings+1, 1 )
        numberOfAngularBinsPerRing = 4 * ( 2 * numberOfAngularBinsPerRing - 1 )

        if VERBOSE: print( "\t-> Number of angular bins per ring = ", numberOfAngularBinsPerRing )

        # defining an array with dimensions numberOfRings x numberOfAngularBinsPerRing
        binCounts = numpy.zeros( ( numberOfRings, numberOfAngularBinsPerRing[-1] ) )

        # ========================================================================
        # ==== Start counting the vectors into bins                            ===
        # ========================================================================
        for vectorN in range( numberOfPoints ):
            # unpack projected angle and radius for this point
            angle, radius = projection_theta_r[ vectorN, : ]

            # Flip over negative angles
            if angle < 0:             angle += 2*math.pi
            if angle > 2 * math.pi:   angle -= 2*math.pi

            # Calculate right ring number
            ringNumber = int(numpy.floor( radius / ( radiusMax / float(numberOfRings) ) ) )

            # Check for overflow
            if ringNumber > numberOfRings - 1:
                if VERBOSE: print( "\t-> Point with projected radius = %f is a problem (radiusMax = %f), putting in furthest  bin"%( radius, radiusMax ) )
                ringNumber = numberOfRings - 1

            # Calculate the angular bin
            angularBin = int( numpy.floor( ( angle ) / ( 2 * math.pi / float( numberOfAngularBinsPerRing[ ringNumber ] ) ) ) ) + 1

            #print "numberOfAngularBinsPerRing", numberOfAngularBinsPerRing[ringNumber] - 1
            # Check for overflow
            #  in case it doesn't belong in the last angularBin, it has to be put in the first one!
            if angularBin > numberOfAngularBinsPerRing[ringNumber] - 1:
                if VERBOSE: print( "\t-> Point with projected angle = %f does not belong to the last bin, putting in first bin"%( angle ) )
                angularBin = 0

            # now that we know what ring, and angular bin you're in add one count!
            binCounts[ ringNumber, angularBin ] += 1

        # ========================================================================
        # === Plotting binned data                                             ===
        # ========================================================================

        plottingRadii = numpy.linspace( radiusMax/float(numberOfRings), radiusMax, numberOfRings )
        #print "Plotting radii:", plottingRadii

        #ax  = fig.add_subplot(122, polar=True)
        #matplotlib.pyplot.axis(  )
        #ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        bars = []

        # add two fake, small circles at the beginning so that they are overwritten
        #   they will be coloured with the min and max colour
        #              theta   radius    width
        bars.append( [   0,   radiusMax,    2*math.pi ] )
        bars.append( [   0,   radiusMax,    2*math.pi ] )
        #bars.append( ax.bar( 0,   radiusMax,    2*math.pi, bottom=0.0 ) )
        #bars.append( ax.bar( 0,   radiusMax,    2*math.pi, bottom=0.0 ) )

        # --- flatifiying binned data for colouring wedges                    ===
        flatBinCounts = numpy.zeros( numpy.sum( numberOfAngularBinsPerRing ) + 2 )

        # Bin number as we go through the bins to add the counts in order to the flatBinCounts
        # This is two in order to skip the first to fake bins which set the colour bar.
        binNumber = 2

        # --- Plotting binned data, from the outside, inwards.                 ===
        if binNormalisation:
            avg_binCount = float(numberOfPoints)/numpy.sum( numberOfAngularBinsPerRing )
            #print "\t-> Number of points = ", numberOfPoints
            #print "\t-> Number of bins   = ", numpy.sum( numberOfAngularBinsPerRing )
            if VERBOSE: print( "\t-> Average binCount = ", avg_binCount )

        for ringNumber in range( numberOfRings )[::-1]:
            deltaTheta    = 360 / float( numberOfAngularBinsPerRing[ringNumber] )
            deltaThetaRad = 2 * math.pi / float( numberOfAngularBinsPerRing[ringNumber] )

            # --- Angular bins                                                 ---
            for angularBin in range( numberOfAngularBinsPerRing[ringNumber] ):
                # ...or add bars
                #                           theta                             radius                  width
                bars.append( [ angularBin*deltaThetaRad - deltaThetaRad/2.0, plottingRadii[ ringNumber ], deltaThetaRad ] )
                #bars.append( ax.bar( angularBin*deltaThetaRad - deltaThetaRad/2.0, plottingRadii[ ringNumber ], deltaThetaRad, bottom=0.0 ) )

                # Add the number of vectors counted for this bin
                if binNormalisation:
                    flatBinCounts[ binNumber ] = binCounts[ ringNumber, angularBin ]/avg_binCount
                else:
                    flatBinCounts[ binNumber ] = binCounts[ ringNumber, angularBin ]

                # Add one to bin number
                binNumber += 1

        del binNumber

        # figure out auto values if they're requested.
        if binValues['min'] is None: binValues['min'] = flatBinCounts[2::].min()
        if binValues['max'] is None: binValues['max'] = flatBinCounts[2::].max()

        # Add two flat values for the initial wedges.
        flatBinCounts[0] = binValues['min']
        flatBinCounts[1] = binValues['max']

        ##                           theta                   radius                          width
        barsPlot = ax.bar( numpy.array( bars )[:,0], numpy.array( bars )[:,1], width=numpy.array( bars )[:,2], bottom=0.0)

        for binCount,bar in zip(  flatBinCounts, barsPlot ):
            bar.set_facecolor( cmap(  ( binCount - binValues['min']) / float( binValues['max'] - binValues['min'] ) ) )

        #matplotlib.pyplot.axis( [ 0, radiusMax, 0, radiusMax ] )
        matplotlib.pyplot.axis( [ 0, numpy.deg2rad(360), 0, radiusMax ] )

        #colorbar = matplotlib.pyplot.colorbar( barsPlot, norm=matplotlib.colors.Normalize( vmin=minBinValue, vmax=maxBinValue ) )
        # Set the colormap and norm to correspond to the data for which
        # the colorbar will be used.

        norm = matplotlib.colors.Normalize( vmin=binValues['min'], vmax=binValues['max'] )

        # ColorbarBase derives from ScalarMappable and puts a colorbar
        # in a specified axes, so it has everything needed for a
        # standalone colorbar.  There are many more kwargs, but the
        # following gives a basic continuous colorbar with ticks
        # and labels.
        ax3 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
        cb1 = matplotlib.colorbar.ColorbarBase( ax3, cmap=cmap, norm=norm )

        # set the line along which the numbers are plotted to 0°
        #ax.set_rlabel_position(0)

        # set radius grids to 15, 30, etc, which means 6 numbers (r=0 not included)
        radiusGridAngles = numpy.arange( 15, 91, 15 )
        radiusGridValues = []
        for angle in radiusGridAngles:
            #                        - project the 15, 30, 45 as spherical coords, and select the r part of theta r-
            #               - append to list of radii -
            radiusGridValues.append( _projectOrientations( projection, "spherical", [ 1, angle*math.pi/180.0, 0 ] )[1][1] )
        #                                       --- list comprehension to print 15°, 30°, 45° ----------
        ax.set_rgrids( radiusGridValues, labels=[ "%02i$^\circ$"%(x) for x in numpy.arange(  15,91,15) ], angle=None, fmt=None )

        fig.subplots_adjust(left=0.05,right=0.85)
        #cb1.set_label('Some Units')

        if saveFigPath is not None:
          matplotlib.pyplot.savefig( saveFigPath )
        else:
          matplotlib.pyplot.show()


if __name__ == "__main__":
    #reference       = numpy.loadtxt( orientationsFile, usecols=(2,3,4))
    SPHERE_TEST = False

    if SPHERE_TEST:
        print ("\t-> Working with \"equally\" spaced points of a sphere")
        # This overrides the length of the file, and can simply be set to the number of 
        #   points desired
        numberOfPoints = 4000
        orientations_zyx = SaffAndKuijlaarsSpiral( numberOfPoints )

    else:
        # Max's benchmarking points for the binning
        orientations_zyx = numpy.array( [ 
                                  [ 1, 0, 0 ],    \
                                  [ -1, 0, 0 ],   \
                                  [ 0.2, 1, 1 ],  \
                                  [ 0.2,-1,-1],   \
                                  [ 0,1,1],       \
                                  [ 1,1,1],       \
                                  [ 0,1,-0.0],       \
                                  [ 0,1,0.01],      \
                                  [ 1,-1,1 ],     \
                                  [ 1.8,0.1,1 ]  ] 
                                )
    plotOrientations( orientations_zyx,
                    projection="lambert",
                    plot="both",
                    binValues={ "min": None, "max": None},
                    numberOfRings=7,
                    pointMarkerSize=8,
                    title = "Demonstration of orientation plotting",
                    subtitle = { "points":"Points",
                                 "bins":"Bins"}
                    )
                    
    #plotProjection( orientations_zyx,
                    ##projection="lambert",
                    ##plot="both",
                    ##binValues={ "min": None, "max": None},
                    ##numberOfRings=9,
                    ##pointMarkerSize=8,
                    ##title = "Demonstration of orientation plotting",
                    ##subtitle = { "points":"Points",
                                 ##"bins":"Bins"}
                    #)

