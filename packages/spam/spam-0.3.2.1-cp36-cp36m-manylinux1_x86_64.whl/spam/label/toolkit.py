from __future__ import print_function

import numpy

import sys
import os

from . import labelToolkit

import scipy.ndimage

import scipy.spatial

import matplotlib

import spam.label
import math


# Define a random colourmap for showing labels
#   This is taken from https://gist.github.com/jgomezdans/402500
randomCmapVals = numpy.random.rand(256, 3)
randomCmapVals[0, :] = numpy.array([1.0, 1.0, 1.0])
randomCmapVals[-1, :] = numpy.array([0.0, 0.0, 0.0])
randomCmap = matplotlib.colors.ListedColormap(randomCmapVals)
del randomCmapVals


# If you change this, remember to change the typedef in tools/labelToolkit/labelToolkitC.hpp
labelType = '<u4'


def boundingBoxes(lab):
    """
    Returns bounding boxes for labelled objects using fast C-code which runs a single time through lab

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

    Returns
    -------
        boundingBoxes : lab.max()x6 array of ints
            This array contains, for each label, 6 integers:

            - Zmin, Zmax
            - Ymin, Ymax
            - Xmin, Xmax

    Note
    ----
        Bounding boxes `are not slices` and so to extract the correct bounding box from a numpy array you should use:
            lab[ Zmin:Zmax+1, Ymin:Ymax+1, Xmin:Xmax+1 ]
        Otherwise said, the bounding box of a single-voxel object at 1,1,1 will be:
            1,1,1,1,1,1

        Also note: for labelled images where some labels are missing, the bounding box returned for this case will be obviously wrong: `e.g.`, Zmin = (z dimension-1) and Zmax = 0

    """
    lab = lab.astype(labelType)

    boundingBoxes = numpy.zeros((lab.max()+1, 6), dtype='<u2')

    labelToolkit.boundingBoxes(lab, boundingBoxes)

    return boundingBoxes


def centresOfMass(lab, boundingBoxes=None, minVol=None):
    """
    Calculates (binary) centres of mass of each label in labelled image

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        minVol : int, optional
            The minimum volume in vx to be treated, any object below this threshold is returned as 0

    Returns
    -------
        centresOfMass : lab.max()x3 array of floats
            This array contains, for each label, 3 floats, describing the centre of mass of each label in Z, Y, X order
    """
    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)
    if minVol is None:
        minVol = 0

    lab = lab.astype(labelType)

    centresOfMass = numpy.zeros((lab.max()+1, 3), dtype='<f4')

    labelToolkit.centresOfMass(lab, boundingBoxes, centresOfMass, minVol)

    return centresOfMass


def volumes(lab, boundingBoxes=None):
    """
    Calculates (binary) volumes each label in labelled image, using potentially slow numpy.where

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

    Returns
    -------
        volumes : lab.max()x1 array of ints
            This array contains the volume in voxels of each label
    """
    #print "label.toolkit.volumes(): Warning this is a crappy python implementation"

    lab = lab.astype(labelType)

    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)

    volumes = numpy.zeros((lab.max()+1), dtype='<u4')

    labelToolkit.volumes(lab, boundingBoxes, volumes)

    return volumes


def equivalentRadii(lab, boundingBoxes=None, volumes=None):
    """
    Calculates (binary) equivalent sphere radii of each label in labelled image

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        volumes : lab.max()x1 array of ints
            Vector contining volumes, if this is passed, the others are ignored

    Returns
    -------
        equivRadii : lab.max()x1 array of floats
            This array contains the equivalent sphere radius in pixels of each label
    """
    def vol2rad(volumes): return ((3.0 * volumes) / (4.0 * numpy.pi))**(1.0/3.0)

    # If we have volumes, just go for it
    if volumes is not None:
        return vol2rad(volumes)

    # If we don't have bounding boxes, recalculate them
    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)

    return vol2rad(spam.label.volumes(lab, boundingBoxes=boundingBoxes))


def momentOfInertia(lab, boundingBoxes=None, minVol=None, centresOfMass=None):
    """
    Calculates (binary) moments of inertia of each label in labelled image

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        centresOfMass : lab.max()x3 array of floats, optional
            Centres of mass in format returned by ``centresOfMass``.
            If not defined (Default = None), it is recomputed by running ``centresOfMass``

        minVol : int, optional
            The minimum volume in vx to be treated, any object below this threshold is returned as 0

    Returns
    -------
        eigenValues : lab.max()x3 array of floats
            The values of the three eigenValues of the moment of inertia of each labelled shape

        eigenVectors : lab.max()x9 array of floats
            3 x Z,Y,X components of the three eigenValues in the order of the eigenValues
    """
    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)
    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(lab, boundingBoxes=boundingBoxes, minVol=minVol)

    lab = lab.astype(labelType)

    eigenValues = numpy.zeros((lab.max()+1, 3), dtype='<f4')
    eigenVectors = numpy.zeros((lab.max()+1, 9), dtype='<f4')

    labelToolkit.momentOfInertia(lab, boundingBoxes, centresOfMass, eigenValues, eigenVectors)

    return [eigenValues, eigenVectors]


def ellipseAxes(lab, volumes=None, MOIeigenValues=None, enforceVolume=True, twoD=False):
    """
    Calculates length of half-axes a,b,c of the ellipitic fit of the particle.
    These are half-axes and so are comparable to the radius -- and not the diameter -- of the particle.

    See appendix of for inital work:
        Ikeda, S., Nakano, T., & Nakashima, Y. (2000). Three-dimensional study on the interconnection and shape of crystals in a graphic granite by X-ray CT and image analysis.

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels
            Note: This is not strictly necessary if volumes and MOI is given

        volumes : 1D array of particle volumes (optional, default = None)
            Volumes of particles (length of array = lab.max())

        MOIeigenValues : lab.max()x3 array of floats, (optional, default = None)
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        enforceVolume = bool (default = True)
            Should a, b and c be scaled to enforce the fitted ellipse volume to be
            the same as the particle?
            This causes eigenValues are no longer completely consistent with fitted ellipse

        twoD : bool (default = False)
            Are these in fact 2D ellipses?
            Not implemented!!

    Returns
    -------
        eigenValues : lab.max()x3 array of floats
        a, b, c lengths of particle in pixels

    Note
    -----
        Our elliptic fit is not necessarily of the same volume as the original particle,
        although by default we scale all axes linearly with `enforceVolumes` to enforce this condition.

        Reminder: volume of an ellipse is (4/3)*pi*a*b*c

        Useful check from TM: Ia = (4/15)*pi*a*b*c*(b**2+c**2)
    """
    # Full ref:
    # @misc{ikeda2000three,
    #         title={Three-dimensional study on the interconnection and shape of crystals in a graphic granite by X-ray CT and image analysis},
    #         author={Ikeda, S and Nakano, T and Nakashima, Y},
    #         year={2000},
    #         publisher={De Gruyter}
    #      }

    if volumes is None:
        volumes = spam.label.volumes(lab)
    if MOIeigenValues is None:
        MOIeigenValues = spam.label.momentOfInertia(lab)[0]

    ABCaxes = numpy.zeros((volumes.shape[0], 3))

    Ia = MOIeigenValues[:, 0]
    Ib = MOIeigenValues[:, 1]
    Ic = MOIeigenValues[:, 2]

    # Initial derivation -- has quite a different volume from the original particle
    # Use the particle's V. This is a source of inconsistency,
    # since the condition V = (4/3) * pi * a * b * c is not necessarily respected
    ###ABCaxes[:,2] = numpy.sqrt( numpy.multiply((5.0/(2.0*volumes.ravel())),( Ib + Ia - Ic ) ) )
    ###ABCaxes[:,1] = numpy.sqrt( numpy.multiply((5.0/(2.0*volumes.ravel())),( Ia + Ic - Ib ) ) )
    ###ABCaxes[:,0] = numpy.sqrt( numpy.multiply((5.0/(2.0*volumes.ravel())),( Ic + Ib - Ia ) ) )

    mask = numpy.logical_and(Ia != 0, numpy.isfinite(Ia))
    # Calculate a, b and c: TM calculation 2018-03-30
    # 2018-04-30 EA and MW: swap A and C so that A is the biggest
    ABCaxes[mask, 2] = ((15.0/(8.0*numpy.pi)) * numpy.square((Ib[mask] + Ic[mask] - Ia[mask])) / numpy.sqrt(((Ia[mask] - Ib[mask] + Ic[mask])*(Ia[mask] + Ib[mask] - Ic[mask])))) ** (1.0/5.0)
    ABCaxes[mask, 1] = ((15.0/(8.0*numpy.pi)) * numpy.square((Ic[mask] + Ia[mask] - Ib[mask])) / numpy.sqrt(((Ib[mask] - Ic[mask] + Ia[mask])*(Ib[mask] + Ic[mask] - Ia[mask])))) ** (1.0/5.0)
    ABCaxes[mask, 0] = ((15.0/(8.0*numpy.pi)) * numpy.square((Ia[mask] + Ib[mask] - Ic[mask])) / numpy.sqrt(((Ic[mask] - Ia[mask] + Ib[mask])*(Ic[mask] + Ia[mask] - Ib[mask])))) ** (1.0/5.0)

    if enforceVolume:
        # Compute volume of ellipse:
        ellipseVol = (4.0/3.0)*numpy.pi*ABCaxes[:, 0]*ABCaxes[:, 1]*ABCaxes[:, 2]
        # filter zeros and infs
        #print volumes.shape
        #print ellipseVol.shape
        volRatio = (volumes[mask] / ellipseVol[mask])**(1.0/3.0)
        #print volRatio
        ABCaxes[mask, 0] = ABCaxes[mask, 0]*volRatio
        ABCaxes[mask, 1] = ABCaxes[mask, 1]*volRatio
        ABCaxes[mask, 2] = ABCaxes[mask, 2]*volRatio

    return ABCaxes


def convertLabelToFloat(lab, vector):
    """
    Replaces all values of a labelled array with a given value.
    Useful for visualising properties attached to labels, `e.g.`, sand grain displacements.

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        vector : a lab.max()x1 vector with values to replace each label with

    Returns
    -------
        relabelled : 3D array of converted floats
    """
    lab = lab.astype(labelType)

    relabelled = numpy.zeros_like(lab, dtype='<f4')

    vector = vector.ravel().astype('<f4')

    labelToolkit.labelToFloat(lab, vector, relabelled)

    return relabelled


def makeLabelsSequential(lab):
    """
    This function fills gaps in labelled images,
    by relabelling them to be sequential integers.

    Parameters
    -----------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background

    Returns
    --------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background
    """
    maxLabel = int(lab.max())
    lab = lab.astype(labelType)

    uniqueLabels = numpy.unique(lab)
    #print uniqueLabels

    relabelMap = numpy.zeros((maxLabel+1), dtype=labelType)
    relabelMap[uniqueLabels] = range(len(uniqueLabels))

    labelToolkit.relabel(lab, relabelMap)

    return lab


def _checkSlice(topOfSlice, botOfSlice, topLimit, botLimit):
    # Do we have any negative positions? Set all negative numbers to zero and see if there was any difference
    topOfSliceLimited = topOfSlice.copy()
    if topOfSliceLimited[0] < topLimit[0]:
        topOfSliceLimited[0] = topLimit[0]
    if topOfSliceLimited[1] < topLimit[1]:
        topOfSliceLimited[1] = topLimit[1]
    if topOfSliceLimited[2] < topLimit[2]:
        topOfSliceLimited[2] = topLimit[2]
    topOfSliceOffset = topOfSliceLimited - topOfSlice

    botOfSliceLimited = botOfSlice.copy()
    if botOfSliceLimited[0] > botLimit[0]:
        botOfSliceLimited[0] = botLimit[0]
    if botOfSliceLimited[1] > botLimit[1]:
        botOfSliceLimited[1] = botLimit[1]
    if botOfSliceLimited[2] > botLimit[2]:
        botOfSliceLimited[2] = botLimit[2]
    botOfSliceOffset = botOfSliceLimited - botOfSlice

    returnSliceLimited = (slice(int(topOfSliceLimited[0]), int(botOfSliceLimited[0])),
                          slice(int(topOfSliceLimited[1]), int(botOfSliceLimited[1])),
                          slice(int(topOfSliceLimited[2]), int(botOfSliceLimited[2])))

    returnSliceOffset = (slice(int(topOfSliceOffset[0]), int(topOfSliceOffset[0]+botOfSliceLimited[0]-topOfSliceLimited[0])),
                         slice(int(topOfSliceOffset[1]), int(topOfSliceOffset[1]+botOfSliceLimited[1]-topOfSliceLimited[1])),
                         slice(int(topOfSliceOffset[2]), int(topOfSliceOffset[2]+botOfSliceLimited[2]-topOfSliceLimited[2])))

    return returnSliceLimited, returnSliceOffset


def getLabel(labelledVolume, label,
             boundingBoxes=None, centresOfMass=None, margin=None,
             extractCube=False, extractCubeSize=None,
             maskOtherLabels=True,
             labelDilate=0):
    """
    Helper function to return well-formatted information about labels to
    help with iterations over labels

    Parameters
    ----------
        labelVolume : 3D array of ints
            3D Labelled volume

        label : int
            Label that we want information about

        boundingBoxes : nLabels*2 array of ints, optional
            Bounding boxes as returned by ``boundingBoxes``.
            Optional but highly recommended.
            If unset, bounding boxes are recalculated for every call.

        centresOfMass : nLabels*3 array of floats, optional
            Centres of mass as returned by ``centresOfMass``.
            Optional but highly recommended.
            If unset, centres of mass are recalculated for every call.

        extractCube : bool, optional
            Whether returned label subvolume should be in the middle of a cube or its bounding box.
            Should handle edges.
            Default = no

        extractCubeSize : int, optional
            half-size of cube to exctract.
            Default = calculate minimum cube

        margin : int, optional
            Extract a ``margin`` pixel margin around bounding box or cube.
            Default = 0

        maskOtherLabels : bool, optional
            In the returned subvolume, should other labels be masked?
            If true, the mask is directly returned.
            Default = True

        labelDilate : int, optional
            Number of times label should be dilated before returning it?
            This can be useful for catching the outside/edge of an image.
            ``margin`` should at least be equal to this value.
            Requires ``maskOtherLabels``.
            Default = 0

    Returns
    -------
        Dictionary containing:

            Keys:
                subvol : 3D array of ints
                    subvolume from labelled image

                slice : tuple of 3*slices
                    Slice used to extract subvol -- however edge management complicates this a bit, perhaps an offset should also be returned

                centreOfMassABS : 3*float
                    Centre of mass with respect to ``labelVolume``

                centreOfMassREL : 3*float
                    Centre of mass with respect to ``subvol``

                volume: int
                    Volume of label (before dilating)

    """
    if boundingBoxes is None:
        print("\tlabel.toolkit.returnLabel(): Bounding boxes not passed.")
        print("\tThey will be recalculated for each label, highly recommend calculating outside this function")
        boundingBoxes = spam.label.boundingBoxes(labelledVolume)

    if centresOfMass is None:
        print("\tlabel.toolkit.returnLabel(): Centres of mass not passed.")
        print("\tThey will be recalculated for each label, highly recommend calculating outside this function")
        centresOfMass = spam.label.centresOfMass(labelledVolume)

    # Check if there is a bounding box for this label:
    if label >= boundingBoxes.shape[0]:
        return
        raise "No bounding boxes for this grain"

    bbo = boundingBoxes[label]
    com = centresOfMass[label]
    comRound = numpy.floor(centresOfMass[label])

    # 1. Check if boundingBoxes are correct:
    if (bbo[0] == labelledVolume.shape[0]-1) and \
       (bbo[1] == 0) and \
       (bbo[2] == labelledVolume.shape[1]-1) and \
       (bbo[3] == 0) and \
       (bbo[4] == labelledVolume.shape[2]-1) and \
       (bbo[5] == 0):
        print("\tlabel.toolkit.getLabel(): Label {} does not exist".format(label))

    else:
        # We have a bounding box, let's extract it.
        if extractCube:
            # Calculate offsets between centre of mass and bounding box
            offsetTop = numpy.ceil(com-bbo[0::2])
            offsetBot = numpy.ceil(com-bbo[0::2])
            offset = numpy.max(numpy.hstack([offsetTop, offsetBot]))

            # If is none, assume closest fitting cube.
            if extractCubeSize is not None:
                if extractCubeSize < offset:
                    print ("\tlabel.toolkit.getLabel(): size of desired cube is smaller than minimum to contain label. Continuing anyway.")
                offset = int(extractCubeSize)

            # if a margin is set, add it to offset
            if margin is not None:
                offset += margin

            offset = int(offset)

            # we may go outside the volume. Let's check this
            labSubVol = numpy.zeros((3*[2*offset+1]))

            topOfSlice = numpy.array([int(comRound[0]-offset),
                                      int(comRound[1]-offset),
                                      int(comRound[2]-offset)])
            botOfSlice = numpy.array([int(comRound[0]+offset+1),
                                      int(comRound[1]+offset+1),
                                      int(comRound[2]+offset+1)])

            sliceLimited, sliceOffset = _checkSlice(topOfSlice, botOfSlice, [0, 0, 0], numpy.array(labelledVolume.shape)-1)

            labSubVol[sliceOffset] = labelledVolume[sliceLimited].copy()

        # We have a bounding box, let's extract it.
        else:
            if margin is None:
                margin = 0

            topOfSlice = numpy.array([int(bbo[0]-margin),
                                      int(bbo[2]-margin),
                                      int(bbo[4]-margin)])
            botOfSlice = numpy.array([int(bbo[1]+1+margin),
                                      int(bbo[3]+1+margin),
                                      int(bbo[5]+1+margin)])

            labSubVol = numpy.zeros((botOfSlice[0]-topOfSlice[0],
                                     botOfSlice[1]-topOfSlice[1],
                                     botOfSlice[2]-topOfSlice[2]))

            sliceLimited, sliceOffset = _checkSlice(topOfSlice, botOfSlice, [0, 0, 0], numpy.array(labelledVolume.shape)-1)

            labSubVol[sliceOffset] = labelledVolume[sliceLimited].copy()

        # Get mask for this label
        maskLab = labSubVol == label
        volume = numpy.sum(maskLab)

        # if we should mask, just return the mask.
        if maskOtherLabels:
            #labSubVol[ numpy.logical_not( maskLab ) ] = 0
            # Just overwrite "labSubVol"
            labSubVol = maskLab

            if labelDilate > 0:
                if labelDilate >= margin:
                    print("\tlabel.toolkit.getLabel(): labelDilate requested with a margin smaller than or equal to the number of times to dilate. I hope you know what you're doing!")
                labSubVol = scipy.ndimage.morphology.binary_dilation(labSubVol, iterations=labelDilate)
            if labelDilate < 0:
                labSubVol = scipy.ndimage.morphology.binary_erosion(labSubVol, iterations=-1*labelDilate)

        return {'subvol': labSubVol,
                'slice': sliceLimited,
                'centreOfMassABS': com,
                'centreOfMassREL': com-[sliceLimited[0].start-sliceOffset[0].start,
                                        sliceLimited[1].start-sliceOffset[1].start,
                                        sliceLimited[2].start-sliceOffset[2].start],
                'volume': volume}


def labelsOnEdges(lab):
    """
    Return labels on edges of volume

    Parameters
    ----------
        lab : 3D numpy array of ints
            Labelled volume

    Returns
    -------
        uniqueLabels : list of ints
            List of labels on edges
    """

    labelsVector = numpy.arange(lab.max()+1)

    uniqueLabels = []

    uniqueLabels.append(numpy.unique(lab[:, :, 0]))
    uniqueLabels.append(numpy.unique(lab[:, :, -1]))
    uniqueLabels.append(numpy.unique(lab[:, 0, :]))
    uniqueLabels.append(numpy.unique(lab[:, -1, :]))
    uniqueLabels.append(numpy.unique(lab[0, :, :]))
    uniqueLabels.append(numpy.unique(lab[-1, :, :]))

    # Flatten list of lists:
    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    uniqueLabels = [item for sublist in uniqueLabels for item in sublist]

    # There might well be labels that appears on multiple faces of the cube, remove them
    uniqueLabels = numpy.unique(numpy.array(uniqueLabels))

    return uniqueLabels.astype(labelType)


def removeLabels(lab, listOfLabelsToRemove):
    """
    Resets a list of labels to zero in a labelled volume.

    Parameters
    ----------
        lab : 3D numpy array of ints
            Labelled volume

        listOfLabelsToRemove : list-like of ints
            Labels to remove

    Returns
    -------
        lab : 3D numpy array of ints
            Labelled volume with desired labels blanked

    Note
    ----
        You might want to use `makeLabelsSequential` after using this function
    """
    lab = lab.astype(labelType)

    # define a vector with sequential ints
    arrayOfLabels = numpy.arange(lab.max()+1, dtype=labelType)

    # Remove the ones that have been asked for
    for l in listOfLabelsToRemove:
        arrayOfLabels[l] = 0

    labelToolkit.relabel(lab, arrayOfLabels)

    return lab


def setVoronoi(lab, poreEDT=None, maxPoreRadius=10):
    """
    This function computes an approximate set Voronoi for a given labelled image.
    This is a voronoi which does not have straight edges, and which necessarily
    passes through each contact point, so it is respectful of non-spherical grains.

    See:
    Schaller, F. M., Kapfer, S. C., Evans, M. E., Hoffmann, M. J., Aste, T., Saadatfar, M., ... & Schroder-Turk, G. E. (2013). Set Voronoi diagrams of 3D assemblies of aspherical particles. Philosophical Magazine, 93(31-33), 3993-4017.
    https://doi.org/10.1080/14786435.2013.834389

    and

    Weis, S., Schonhofer, P. W., Schaller, F. M., Schroter, M., & Schroder-Turk, G. E. (2017). Pomelo, a tool for computing Generic Set Voronoi Diagrams of Aspherical Particles of Arbitrary Shape. In EPJ Web of Conferences (Vol. 140, p. 06007). EDP Sciences.

    Parameters
    -----------
        lab: 3D numpy array of labelTypes
            Labelled image

        poreEDT: 3D numpy array of floats (optional, default = None)
            Euclidean distance map of the pores.
            If not given, it is computed by scipy.ndimage.morphology.distance_transform_edt

        maxPoreRadius: int (optional, default = 10)
            Maximum pore radius to be considered (this threshold is for speed optimisation)

    Returns
    --------
        lab: 3D numpy array of labelTypes
            Image labelled with set voronoi labels
    """
    if poreEDT is None:
        #print( "\tlabel.toolkit.setVoronoi(): Calculating the Euclidean Distance Transform of the pore with" )
        #print  "\t\tscipy.ndimage.morphology.distance_transform_edt, this takes a lot of memory"
        poreEDT = scipy.ndimage.morphology.distance_transform_edt(lab == 0).astype('<f4')

    lab = lab.astype(labelType)
    labOut = numpy.zeros_like(lab)
    maxPoreRadius = int(maxPoreRadius)

    # Prepare sorted distances in a cube to fit a maxPoreRadius.
    # This precomutation saves a lot of time
    # Local grid of values, centred at zero
    gridD = numpy.mgrid[-maxPoreRadius:maxPoreRadius+1,
                        -maxPoreRadius:maxPoreRadius+1,
                        -maxPoreRadius:maxPoreRadius+1]

    # Compute distances from centre
    Rarray = numpy.sqrt(numpy.square(gridD[0]) + numpy.square(gridD[1]) + numpy.square(gridD[2])).ravel()
    sortedIndices = numpy.argsort(Rarray)

    # Array to hold sorted coordinates
    coords = numpy.zeros((len(Rarray), 3), dtype='<i4')
    # Fill in with Z, Y, X coordinates in order of distance to centre
    coords[:, 0] = gridD[0].ravel()[sortedIndices]
    coords[:, 1] = gridD[1].ravel()[sortedIndices]
    coords[:, 2] = gridD[2].ravel()[sortedIndices]
    del gridD

    # Now define a simple array (by building a list) that gives the linear
    #   entry point into coords at the nearest integer values
    sortedDistances = Rarray[sortedIndices]
    indices = []
    n = 0
    i = 0
    while i <= maxPoreRadius+1:
        if sortedDistances[n] >= i:
            #indices.append( [ i, n ] )
            indices.append(n)
            i += 1
        n += 1
    indices = numpy.array(indices).astype('<i4')

    # Call C++ code
    labelToolkit.setVoronoi(lab, poreEDT.astype('<f4'), labOut, coords, indices)

    return labOut


def labelTetrahedra(dims, coordinates, connectivity):
    """
    Labels voxels corresponding to tetrahedra according to a connectivity matrix and node points

    Parameters
    ----------
        dims: tuple representing z,y,x dimensions of the desired labelled output

        coordinates: 3 x number of points array of floats
            List of points that define the vertices of the tetrahedra in Z,Y,X format.
            These points are referred to by line number in the connectivity array

        connectivity: 4 x number of tetrahedra array of integers
            Connectivity matrix between points that define tetrahedra.
            Each line defines a tetrahedron whose number is the line number + 1.
            Each line contains 4 integers that indicate the 4 points in the nodePos array.

    Returns
    -------
        3D array of ints, shape = dims
            Labelled 3D volume where voxels are numbered according to the tetrahedron number they fall inside of
    """

    dims = numpy.array(dims).astype('<u2')
    lab = numpy.zeros(tuple(dims), dtype=labelType)

    connectivity = connectivity.astype('<u4')
    coordinates = coordinates.astype('<f4')

    labelToolkit.tetPixelLabel(lab, connectivity, coordinates)

    return lab


def labelTetrahedraForScipyDelaunay(dims, delaunay):
    """
    Labels voxels corresponding to tetrahedra coming from scipy.spatial.Delaunay
    Apparently the cells are not well-numbered, which causes a number of zeros
    when using `labelledTetrahedra`

    Parameters
    ----------
        dims: tuple
            represents z,y,x dimensions of the desired labelled output

        delaunay: "delaunay" object
            Object returned by scipy.spatial.Delaunay( centres )
            Hint: If using label.toolkit.centresOfMass( ), do centres[1:] to remove
            the position of zero.

    Returns
    -------
        lab: 3D array of ints, shape = dims
            Labelled 3D volume where voxels are numbered according to the tetrahedron number they fall inside of
    """

    # Big matrix of points poisitions
    points = numpy.zeros((dims[0]*dims[1]*dims[2], 3))

    mgrid = numpy.mgrid[0:dims[0], 0:dims[1], 0:dims[2]]
    for i in [0, 1, 2]:
        points[:, i] = mgrid[i].ravel()

    del mgrid

    lab = numpy.zeros(tuple(dims), dtype=labelType)
    lab = delaunay.find_simplex(points).reshape(dims)

    return lab


def fabricTensor(orientations):
    """
    Calculation of a second order fabric tensor from orientations

    Parameters
    ----------
        orientations: Nx3 array of floats
            Z, Y and X components of direction vectors
            Non-unit vectors are normalised.

    Returns
    -------
        N: 3x3 array of floats
            normalised second order fabric tensor
            with N[0,0] corresponding to z-z, N[1,1] to y-y and N[2,2] x-x

        F: 3x3 array of floats
            fabric tensor of the third kind (deviatoric part)
            with F[0,0] corresponding to z-z, F[1,1] to y-y and F[2,2] x-x

        a: float
            scalar anisotropy factor based on the deviatoric part F

    Note
    ----
        see [Kanatani, 1984] for more information on the fabric tensor
        and [Gu et al, 2017] for the scalar anisotropy factor
    """
    # from http://stackoverflow.com/questions/2850743/numpy-how-to-quickly-normalize-many-vectors
    norms = numpy.apply_along_axis(numpy.linalg.norm, 1, orientations)
    orientations = orientations / norms.reshape(-1, 1)

    # create an empty array
    N = numpy.zeros((3, 3))
    size = len(orientations)

    for i in range(size):
        orientation = orientations[i]
        tensProd = numpy.outer(orientation, orientation)
        N[:, :] = N[:, :]+tensProd

    # fabric tensor of the first kind
    N = N/size
    # fabric tensor of third kind
    F = (N - (numpy.trace(N) * (1./3.)) * numpy.eye(3, 3)) * (15./2.)

    # scalar anisotropy factor
    a = math.sqrt(3./2. * numpy.tensordot(F, F, axes=2))

    return N, F, a

def filterIsolatedCells(array, struct, size):
    """ 
    Return array with completely isolated single cells removed

    Parameters
    ----------
        array: 3-D (labelled or binary) array 
            Array with completely isolated single cells

        struct: 3-D binary array
            Structure array for generating unique regions

        size: integer
            Size of the isolated cells to exclude
            (Number of Voxels)

    Returns
    -------
        filteredArray: 3-D (labelled or binary) array
            Array with minimum region size > size

    Notes
    -----
        function from: http://stackoverflow.com/questions/28274091/removing-completely-isolated-cells-from-python-array
    """

    filteredArray = ((array > 0)*1).astype('uint8')
    idRegions, numIDs = scipy.ndimage.label(filteredArray, structure=struct)
    idSizes = numpy.array(scipy.ndimage.sum(filteredArray, idRegions, range(numIDs + 1)))
    areaMask = (idSizes <= size)
    filteredArray[areaMask[idRegions]] = 0
    
    filteredArray = ((filteredArray > 0)*1).astype('uint8')
    array = filteredArray * array
    
    return array

