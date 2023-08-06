from __future__ import print_function
# 2017-05-05 Edward Ando and Emmanuel Roubin
import numpy
import scipy.ndimage

numpy.set_printoptions(precision=3, suppress=True)

# Point at which to consider no rotation
rotationAngleDegThreshold = 0.0001

###########################################################
# From components (translation, rotation, zoom, shear) compute Phi
###########################################################


def computePhi(transformation, PhiCentre=[0.0, 0.0, 0.0], PhiPoint=[0.0, 0.0, 0.0]):
    """
    Builds "Phi", a 4x4 deformation function from a dictionary of transformation parameters (translation, rotation, zoom, shear).
    Phi can be used to deform coordinates as follows:
    $$ Phi.x = x'$$

    Parameters
    ----------
        transformation : dictionary of 3x1 arrays
            Input to computeTransformationOperator is a "transformation" dictionary where all items are optional.

            Keys
                t = translation (z,y,x). Note: ( 0, 0, 0 ) does nothing
                r = rotation in "rotation vector" format. Note: ( 0, 0, 0 ) does nothing
                z = zoom. Note: ( 1, 1, 1 ) does nothing
                s = "shear". Note: ( 0, 0,0 ) does nothing

        PhiCentre : 3x1 array, optional
            Point where Phi is centered (centre of rotation)

        PhiPoint : 3x1 array, optional
           Point where Phi is going to be applied

    Returns
    -------
        Phi : 4x4 array of floats
            Phi, deformation function

    Note
    ----
        Useful reference: Chapter 2 -- Rigid Body Registration -- John Ashburner & Karl J. Friston, although we use a symmetric shear
    """
    Phi = numpy.eye(4, dtype='<f4')

    # Translation:
    if 't' in transformation:
        tmp = numpy.eye(4, dtype='<f4')
        tmp[0:3, 3] = transformation['t']
        Phi = numpy.dot(Phi, tmp)

    # Rotation
    if 'r' in transformation:
        # https://en.wikipedia.org/wiki/Rodrigues'_rotation_formula
        # its length is the rotation angle
        rotationAngleDeg = numpy.linalg.norm(transformation['r'])

        if rotationAngleDeg > rotationAngleDegThreshold:
            # its direction is the rotation axis.
            rotationAxis = transformation['r'] / rotationAngleDeg

            # positive angle is clockwise
            K = numpy.array([[0,       -rotationAxis[2],  rotationAxis[1]],
                             [rotationAxis[2],        0,         -rotationAxis[0]],
                             [-rotationAxis[1],  rotationAxis[0],          0]])

            # Note the numpy.dot is very important.
            R = numpy.eye(3) + (numpy.sin(numpy.deg2rad(rotationAngleDeg)) * K) + \
                ((1.0 - numpy.cos(numpy.deg2rad(rotationAngleDeg))) * numpy.dot(K, K))

            tmp = numpy.eye(4, dtype='<f4')
            tmp[0:3, 0:3] = R

            Phi = numpy.dot(Phi, tmp)

    # Zoom + Shear
    if 'z' in transformation or 's' in transformation:
        tmp = numpy.eye(4, dtype='<f4')

        if 'z' in transformation:
            # Zoom components
            tmp[0, 0] = 1.0/transformation['z'][0]
            tmp[1, 1] = 1.0/transformation['z'][1]
            tmp[2, 2] = 1.0/transformation['z'][2]

        if 's' in transformation:
            # Shear components
            tmp[0, 1] = transformation['s'][0]
            tmp[0, 2] = transformation['s'][1]
            tmp[1, 2] = transformation['s'][2]
            # Shear components
            tmp[1, 0] = transformation['s'][0]
            tmp[2, 0] = transformation['s'][1]
            tmp[2, 1] = transformation['s'][2]
        Phi = numpy.dot(Phi, tmp)

    # Apply Phi to the PhiPoint of the "image" and add this translation to Phi
    # Phi[0:3,3] += PhiPoint - numpy.dot( Phi[0:3,0:3], PhiPoint )

    # compute distance between point to apply Phi and the point where Phi is centered (centre of rotation)
    dist = numpy.array(PhiPoint) - numpy.array(PhiCentre)

    # apply Phi to the given point and calculate its displacement
    Phi[0:3, 3] -= dist - numpy.dot(Phi[0:3, 0:3], dist)

    # check that determinant of Phi is sound
    if numpy.linalg.det(Phi) < 0.00001:
        print("computeTransformationOperator(): Determinant of Phi is very small, this is probably bad, transforming volume into a point.")

    return Phi


###########################################################
# Polar Decomposition of a given Phi into human readable components
###########################################################
def decomposePhi(Phi, PhiCentre=[0.0, 0.0, 0.0], PhiPoint=[0.0, 0.0, 0.0]):
    """
        Get components out of a linear deformation function "Phi"

        Parameters
        ----------
        Phi : 4x4 array
            The deformation function operator "Phi"

        PhiCentre : 3x1 array, optional
            Point where Phi was calculated

        PhiPoint : 3x1 array, optional
           Point where Phi is going to be applied

        Returns
        -------
        transformation : dictionary of arrays

                - t = 3x1 array. Translation vector (z,y,x)
                - r = 3x1 array. Rotation in "rotation vector" format
                - U = 3x3 array. Right stretch tensor
                - G = 3x3 array. Eigen vectors * eigenvalues of strains, from which principal directions of strain can be obtained

    """
    # Check for singular Phi if yes quit
    try:
        numpy.linalg.inv(Phi)
    except numpy.linalg.linalg.LinAlgError:
        transformation = {'t': [numpy.nan]*3,
                          'r': [numpy.nan]*3,
                          'U': numpy.nan,
                          'G': numpy.nan
                          }
        return transformation

    # Check for NaNs if any quit
    if numpy.isnan(Phi).sum() > 0:
        transformation = {'t': [numpy.nan]*3,
                          'r': [numpy.nan]*3,
                          'U': numpy.nan,
                          'G': numpy.nan
                          }
        return transformation

    # Check for NaNs if any quit
    if numpy.isinf(Phi).sum() > 0:
        transformation = {'t': [numpy.nan]*3,
                          'r': [numpy.nan]*3,
                          'U': numpy.nan,
                          'G': numpy.nan
                          }
        return transformation

    ###########################################################
    # F, the inside 3x3 displacement gradient
    ###########################################################
    F = Phi[0:3, 0:3].copy()

    ###########################################################
    # Calculate transformation by undoing F on the PhiPoint
    ###########################################################
    tra = Phi[0:3, 3].copy()

    # compute distance between given point and the point where Phi was calculated
    dist = numpy.array(PhiPoint) - numpy.array(PhiCentre)

    # apply Phi to the given point and calculate its displacement
    tra -= dist - numpy.dot(Phi[0:3, 0:3], dist)

    ###########################################################
    # Polar decomposition of little 3x3 transformation matrix Phi[0:3, 0:3] = RU
    # U is the right stretch tensor
    # R is the rotation tensor
    ###########################################################

    # Compute the Right Cauchy tensor
    C = numpy.dot(F.T, F)

    # Solve eigen problem
    CeigVal, CeigVec = numpy.linalg.eig(C)

    # 2018-06-29 OS & ER check for negative eigenvalues
    # test "really" negative eigenvalues
    if CeigVal.any()/CeigVal.mean() < -1:
        print("deformationFunction.decomposePhi(): negative eigen value in transpose(Phi).Phi which is really wrong. Exiting")
        print("Eigenvalues are: {}".format(CeigenVal))
        exit()
    # for negative eigen values but close to 0 we set it to 0
    CeigVal[CeigVal < 0] = 0

    # Diagonalise C --> which is U**2
    diagUsqr = numpy.array([[CeigVal[0], 0, 0],
                            [0, CeigVal[1], 0],
                            [0, 0, CeigVal[2]]])

    diagU = numpy.sqrt(diagUsqr)

    # 2018-02-16 check for both issues with negative (Udiag)**2 values and inverse errors
    try:
        U = numpy.dot(numpy.dot(CeigVec, diagU), CeigVec.T)
        R = numpy.dot(F, numpy.linalg.inv(U))
    except numpy.linalg.LinAlgError:
        #print("Error while inverting U in order to create the rotation matrix. Might come from singular F.")
        #print("Little F =")
        #print(F)
        #print("returning null transformations.")
        transformation = {'t': [0, 0, 0],
                          'r': [0, 0, 0],
                          'U': numpy.eye(3),
                          'G': 3*[0, 0, 0]
                          }
        return transformation

    # print(CeigVal)
    # print(diagUsqr)
    # print(diagU)
    # print(U)
    # print(R)

    # normalisation of rotation matrix in order to respect basic properties
    # otherwise it gives errors like trace(R) > 3
    # this issue might come from numerical noise.
    # ReigVal, ReigVec = numpy.linalg.eig(R)

    for i in range(3):
        R[i, :] /= scipy.linalg.norm(R[i, :])
    # print("traceR - sumEig = {}".format(R.trace() - ReigVal.sum()))
    # print("u.v = {}".format(numpy.dot(R[:, 0], R[:, 1])))
    # print("detR = {}".format(numpy.linalg.det(R)))

    # Calculate rotation angle
    # Detect an identity -- zero rotation
    # if numpy.allclose(R, numpy.eye(3),  atol=1e-03):
    #     rotationAngleRad = 0.0
    #     rotationAngleDeg = 0.0

    # Detect trace(R) > 3 (should not append but appends)
    arccosArg = 0.5 * (R.trace() - 1.0)
    if arccosArg > 1.0:
        rotationAngleRad = 0.0
    else:
        # https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions#Rotation_matrix_.E2.86.94_Euler_axis.2Fangle
        rotationAngleRad = numpy.arccos(arccosArg)
    rotationAngleDeg = numpy.rad2deg(float(rotationAngleRad))

    # print("R")
    # print(R)
    # print("trace R = {}".format(R.trace()))
    # print("arccosArg = {}".format(arccosArg))
    # print("rotationAngleRad = {}".format(rotationAngleRad))
    # print("rotationAngleDeg = {}".format(rotationAngleDeg))

    if rotationAngleDeg > rotationAngleDegThreshold:
        rotationAxis = numpy.array([R[2, 1] - R[1, 2],
                                    R[0, 2] - R[2, 0],
                                    R[1, 0] - R[0, 1]])
        rotationAxis /= 2.0 * numpy.sin(rotationAngleRad)
        rot = rotationAngleDeg * rotationAxis
    else:
        rot = [0.0, 0.0, 0.0]
    ###########################################################

    # print "R is \n", R, "\n"
    # print "|R| is ", numpy.linalg.norm(R), "\n"
    # print "det(R) is ", numpy.linalg.det(R), "\n"
    # print "R.T - R-1 is \n", R.T - numpy.linalg.inv( R ), "\n\n"

    # print "U is \n", U, "\n"
    # print "U-1 is \n", numpy.linalg.inv( U ), "\n\n"

    # Also output eigenvectors * their eigenvalues as output:
    G = []

    for eigenvalue, eigenvector in zip(CeigVal, CeigVec):
        G.append(numpy.multiply(eigenvalue, eigenvector))

    transformation = {'t': [t for t in tra],
                      'r': [r for r in rot],
                      'U': U,
                      'G': G
                      }

    return transformation


###########################################################
# Taken an Phi and apply it (C++) to an image
###########################################################
def applyPhi(im, Phi=None, PhiPoint=None, interpolationOrder=1):
    """
        Deform a 3D image using a deformation function "Phi", applied using spam's C++ interpolator.
        Only interpolation order = 1 is implemented.

        Parameters
        ----------
        im : 3D numpy array
            3D numpy array of grey levels to be deformed

        Phi : 4x4 array, optional
            "Phi" deformation function.
            Highly recommended additional argument (why are you calling this function otherwise?)

        PhiPoint : 3x1 array of floats, optional
            Centre of application of Phi.
            Default = (numpy.array(im1.shape)-1)/2.0
            i.e., the centre of the image

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 1

        Returns
        -------
        imDef : 3D array
            Deformed greyscales by Phi
    """
    # import sys
    # import os
    from . import DICToolkit

    # Sort out Phi and calculate inverse
    if Phi is None:
        PhiInv = numpy.eye(4, dtype='<f4')
    else:
        try:
            PhiInv = numpy.linalg.inv(Phi).astype('<f4')
        except numpy.linalg.linalg.LinAlgError:
            # print( "\tapplyPhi(): Can't inverse Phi, setting it to identity matrix. Phi is:\n{}".format( Phi ) )
            PhiInv = numpy.eye(4, dtype='<f4')

    if PhiPoint is None:
        PhiPoint = (numpy.array(im.shape)-1)/2.0

    imDef = numpy.zeros_like(im, dtype='<f4')

    if interpolationOrder > 1:
        print("DIC.deformationFunction.applyPhi(): interpolation Order > 1 not implemented")
        return

    im = im.astype('<f4')
    PhiPoint = numpy.array(PhiPoint).astype('<f4')

    # We need to inverse Phi for question of direction
    DICToolkit.applyPhiC(im, imDef, PhiInv, PhiPoint, int(interpolationOrder))

    return imDef


###########################################################
# Taken an Phi and apply it to an image
###########################################################
def applyPhiPython(im, Phi=None, PhiPoint=None, interpolationOrder=3):
    """
        Deform a 3D image using a deformation function "Phi", applied using scipy.ndimage.map_coordinates
        Can have orders > 1 but is hungry in memory.

        Parameters
        ----------
        im : 3D numpy array
            3D numpy array of grey levels to be deformed

        Phi : 4x4 array, optional
            "Phi" linear deformation function.
            Highly recommended additional argument (why are you calling this function otherwise?)

        PhiPoint : 3x1 array of floats, optional
            Centre of application of Phi.
            Default = (numpy.array(im1.shape)-1)/2.0
            i.e., the centre of the image

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 3

        Returns
        -------
        imSub : 3D array
            Deformed greyscales by Phi
    """

    if Phi is None:
        PhiInv = numpy.eye(4, dtype='<f4')
    else:
        try:
            PhiInv = numpy.linalg.inv(Phi).astype('<f4')
        except numpy.linalg.linalg.LinAlgError:
            # print( "\tapplyPhiPython(): Can't inverse Phi, setting it to identity matrix. Phi is:\n{}".format( Phi ) )
            PhiInv = numpy.eye(4)

    if PhiPoint is None:
        PhiPoint = (numpy.array(im.shape)-1)/2.0

    imDef = numpy.zeros_like(im, dtype='<f4')

    coordinatesInitial = numpy.ones((4, im.shape[0] * im.shape[1] * im.shape[2]), dtype='<f4')

    coordinates_mgrid = numpy.mgrid[0:im.shape[0],
                                    0:im.shape[1],
                                    0:im.shape[2]]

    # Copy into coordinatesInitial
    coordinatesInitial[0, :] = coordinates_mgrid[0].ravel() - PhiPoint[0]
    coordinatesInitial[1, :] = coordinates_mgrid[1].ravel() - PhiPoint[1]
    coordinatesInitial[2, :] = coordinates_mgrid[2].ravel() - PhiPoint[2]

    # Apply Phi to coordinates
    coordinatesDef = numpy.dot(PhiInv, coordinatesInitial)

    coordinatesDef[0, :] += PhiPoint[0]
    coordinatesDef[1, :] += PhiPoint[1]
    coordinatesDef[2, :] += PhiPoint[2]

    imDef += scipy.ndimage.map_coordinates(im,
                                           coordinatesDef[0:3],
                                           order=interpolationOrder).reshape(imDef.shape).astype('<f4')
    return imDef

###############################################################
# Taken a field of Phi and apply it (quite slowly) to an image
###############################################################
def applyPhiField(im, fieldName=None, fieldCoords=None, fieldValues=None, fieldBinRatio=1.0, neighbours=8, interpolationOrder=3, verbose=False):
    """
        Deform a 3D image using a field of deformation functions "Phi" coming from a regularGrid,
        applied using scipy.ndimage.map_coordinates.

        Parameters
        ----------
        im : 3D array
            3D array of grey levels to be deformed

        fieldName : string, optional
            Name of the file containing the deformation functions field

        fieldCoords: 2D array, optional
            nx3 array of n points coordinates (ZYX)
            centre where each deformation function "Phi" has been calculated

        fieldValues: 3D array, optional
            nx4x4 array of n points deformation functions

        fieldBinRatio : int, optional
            If the input field refers to a binned version of the image
            `e.g.`, if ``fieldBinRatio = 2`` the ``fieldName`` values have been calculated
            for an image half the size of the input image ``im``
            Default = 1

        neighbours : int, optional
            Neighbours for field interpolation
            If == 1, the nearest neighbour is used, if >1 neighbours are weighted according to distance.
            Default = 8

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 1

        Returns
        -------
        imDef : 3D array
            deformed greylevels by a field of deformation functions "Phi"
    """

    # Create the grid of the input image
    imSize = im.shape
    coordinates_mgrid = numpy.mgrid[0:imSize[0],
                                    0:imSize[1],
                                    0:imSize[2]]

    coordIn = numpy.ones((imSize[0] * imSize[1] * imSize[2], 4))

    coordIn[:, 0] = coordinates_mgrid[0].ravel()
    coordIn[:, 1] = coordinates_mgrid[1].ravel()
    coordIn[:, 2] = coordinates_mgrid[2].ravel()

    numberofPoints = imSize[0] * imSize[1] * imSize[2]

    # Copy initial coordinates to the deformed coordinates
    coordDef = coordIn.copy()

    # Read input PhiField, usually the result of a regularGrid correlation
    if fieldName:
        import spam.helpers.tsvio
        PhiFromFile = spam.helpers.tsvio.readTSV(fieldName, fieldBinRatio=fieldBinRatio)
        fieldCoords = PhiFromFile["fieldCoords"]
        fieldValues = PhiFromFile["PhiField"]
    else:
        fieldCoords = fieldCoords
        fieldValues = fieldValues

    # Create the k-d tree of the coordinates of the input Phi field
    from scipy.spatial import KDTree
    tree = KDTree(fieldCoords)

    # Loop over each point of the grid of the input image
    for point in range(coordIn.shape[0]):
        if verbose:
            print("\rWorking on point {} {}%".format(point, (point/float(numberofPoints))*100), end='')

        # Calculate the distance of the current point to the points of the input Phi field
        distance, indices = tree.query(coordIn[point][0:3], k=neighbours)

        # Check if we've hit the same point
        if numpy.any(distance == 0):

            # Deform the coordinates of the current point
            # by subtracting the translation part of the deformation function Phi
            coordDef[point][:3] -= fieldValues[indices][numpy.where(distance == 0)][0][0:3, -1].copy()

        # Check if we have asked only for the closest neighbour
        elif neighbours == 1:

            # Deform the coordinates of the current point
            # by subtracting the translation part of the deformation function Phi
            # applied on the current point
            coordDef[point][:3] -= decomposePhi(fieldValues[indices].copy(),
                                                     PhiCentre=fieldCoords[indices],
                                                     PhiPoint=coordIn[point][:3])["t"]

        # Consider the k closest neighbours
        else:
            # Compute the `Inverse Distance Weighting` since the closest points should have the major influence
            weightSumInv = sum(1/distance)

            # Loop over each neighbour
            for neighbour in range(neighbours):
                # Calculate its weight
                weightInv = (1/distance[neighbour])/float(weightSumInv)

            # Deform the coordinates of the current point
            # by subtracting the translation part of the deformation function Phi
            # applied on the current point
            # multiplied by the weight of each neighbour
                coordDef[point][:3] -= numpy.dot(decomposePhi(fieldValues[indices][neighbour].copy(),
                                                                   PhiCentre=fieldCoords[indices][neighbour],
                                                                   PhiPoint=coordIn[point][:3])["t"],
                                                 weightInv)

    # Deform the image
    imDef = numpy.zeros_like(im)

    imDef += scipy.ndimage.map_coordinates(im,
                                           coordDef[:, 0:3].T,
                                           mode="constant",
                                           order=interpolationOrder).reshape(imDef.shape).astype('<f4')

    return imDef


def correctPhiField(fileName=None,
                    fieldCoords=None, fieldValues=None, fieldRS=None, fieldDPhi=None, fieldPSCC=None, fieldIT=None,
                    fieldBinRatio=1.0,
                    ignoreBadPoints=False, ignoreBackGround=False,
                    correctBadPoints=False,
                    deltaPhiNormMin=0.001, pixelSearchCCmin=0.98,
                    neighbours=12,
                    filterPoints=False, filterPointsRadius=3,
                    verbose=False,
                    saveFile=False, saveFileName=None):
    """
    This function corrects a field of deformation functions **Phi** calculated at a number of points.
    This is typically the output of the DICdiscrete and DICregularGrid clients.
    The correction is done based on the `SubPixelReturnStatus` and `SubPixelDeltaPhiNorm` of the correlated points.
    It takes as an input either a tsv file containing the result of the correlation or
    6 separate arrays:

      1 the coordinates of the points

      2 the PhiField

      3 the `SubPixelReturnStatus` 

      4 the `SubPixelDeltaPhiNorm` 

      5 the `PSCC` 

      6 the `SubPixelIterations` 


    Parameters
    ----------
        fileName : string, optional
            name of the file

        fieldCoords : 2D array, optional
            nx3 array of n points coordinates (ZYX)
            centre where each deformation function **Phi** has been calculated

        fieldValues : 3D array, optional
            nx4x4 array of n points deformation functions

        fieldRS : 1D array, optional
            nx1 array of n points `SubPixelReturnStatus` from the correlation

        fieldDf : 1D array, optional
            nx1 array of n points `SubPixelDeltaPhiNorm` from the correlation

        fieldIT : 1D array, optional
            nx1 array of n points `SubPixelIterations` from the correlation

        fieldPSCC : 1D array, optional
            nx1 array of n points `PixelSearchCorrelationCoefficient` from the correlation

        fieldBinRatio : int, optional
            if the input field is referred to a binned version of the image
            *e.g.*, if `fieldBinRatio = 2` the fileName values have been calculated for an image half the size of what the returned PhiField is referring to.
            Default = 1.0

        ignoreBadPoints : bool, optional
            if True it will replace the **Phi** matrices of the badly correlated points with nans.
            Bad points are set according to `SubPixelReturnStatus` and `SubPixelDeltaPhiNorm` or `PSCC` of the correlation.
            Default = False

         ignoreBackGround : bool, optional
            if True it will replace the **Phi** matrices of the back ground points with nans.
            Back ground points are set according to `SubPixelReturnStatus` (<-4) of the correlation.
            Default = False

        correctBadPoints : bool, optional
            if True it will replace the **Phi** matrices of the badly correlated points with the weighted function of the k nearest good points.
            Bad points are set according to `SubPixelReturnStatus` and `SubPixelDeltaPhiNorm` or `PSCC` of the correlation
            The number of the nearest good neighbours can be defined (see `neighbours` below).
            Default = False

        deltaPhiNormMin: float, optional
            minimum value of subpixel change in Phi to consider a point with `SubPixelReturnStatus` = 1 as good or bad.
            Default = 0.001

        picelSearchCCmin: float, optional
            minimum value of pixel search correlation coefficient to consider a point as good or bad.
            Default = 0.98

        neighbours : int, optional
            if `correctBadPoints` is activated, it specifies the number of the nearest neighbours to consider.
            If == 1, the nearest neighbour is used, if >1 neighbours are weighted according to distance.
            Default = 12

        filterPoints : bool, optional
            if True: a median filter will be applied on the **Phi** of each point.
            Default = False

        filterPointsRadius : int, optional
            Radius of median filter.
            Size of cubic structuring element is 2*filterPointsRadius+1.
            Default = 3

        verbose : bool, optional
            follow the progress of the function.
            Default = False

        saveFile : bool, optional
            save the corrected file into a tsv
            Default = False

        saveFileName : string, optional
            The file name for output.
            Default = 'spam'

    Returns
    -------
        PhiField : nx4x4 array
            n points deformation functions **Phi** after the correction

    """
    import os
    # read the input arguments
    if fileName:
        if not os.path.isfile(fileName):
            print("\n\tdeformationFunction.correctPhiField():{} is not a file. Exiting.".format(fileName))
            return
        else:
            import spam.helpers.tsvio
            fi = spam.helpers.tsvio.readTSV(fileName, fieldBinRatio=fieldBinRatio, readDisplacements=True, readFs=False, readConvergence=True, readPixelSearchCC=True)
            PhiField = fi["PhiField"]
            fieldCoords = fi["fieldCoords"]
            fieldDims = fi["fieldDims"]
            RS = fi["SubPixReturnStat"]
            deltaPhiNorm = fi["SubPixDeltaPhiNorm"]
            iterations = fi["SubPixIterations"]
            PSCC = fi["PixelSearchCC"]
    elif fieldCoords is not None and fieldValues is not None and fieldRS is not None and fieldDPhi is not None and fieldPSCC is not None and fieldIT is not None:
        fieldCoords = fieldCoords
        fieldDims = numpy.array([len(numpy.unique(fieldCoords[:, 0])), len(numpy.unique(fieldCoords[:, 1])), len(numpy.unique(fieldCoords[:, 2]))])
        PhiField = fieldValues
        RS = fieldRS
        deltaPhiNorm = fieldDPhi
        PSCC = fieldPSCC
        iterations = fieldIT
    else:
        print("\tdeformationFunction.correctPhiField(): Not enough arguments given. Exiting.")
        return

    # check if it is a subPixel field or a pixel search field
    if numpy.nansum(PSCC)>0 and iterations.sum()==0:
        pixelSearch = True
        subPixel = False
    else:
        pixelSearch = False
        subPixel = True

    # define good and bad correlation points according to `SubPixelReturnStatus` and `SubPixelDeltaPhiNorm` or `PSCC`conditions
    if ignoreBackGround is False:
        if subPixel:
            goodPoints = numpy.where(numpy.logical_or(RS == 2, numpy.logical_and(RS == 1, deltaPhiNorm <= deltaPhiNormMin)))
            badPoints  = numpy.where(numpy.logical_or(RS <= 0, numpy.logical_and(RS == 1, deltaPhiNorm > deltaPhiNormMin)))
        if pixelSearch:
            goodPoints = numpy.where(PSCC >= pixelSearchCCmin)
            badPoints  = numpy.where(PSCC < pixelSearchCCmin)
    else:
        if subPixel:
            goodPoints = numpy.where(numpy.logical_or(RS == 2, numpy.logical_and(RS == 1, deltaPhiNorm <= deltaPhiNormMin)))
            badPoints  = numpy.where(numpy.logical_or(numpy.logical_and(RS <= 0, RS >= -4), numpy.logical_and(RS == 1, deltaPhiNorm > deltaPhiNormMin)))
            backGroundPoints = numpy.where(RS < -4)
        if pixelSearch:
            goodPoints = numpy.where(numpy.logical_and(RS >= -4, PSCC >= pixelSearchCCmin))
            badPoints  = numpy.where(numpy.logical_and(RS >= -4, PSCC < pixelSearchCCmin))
        backGroundPoints = numpy.where(RS < -4)
        PhiField[backGroundPoints] = numpy.nan

    # if asked, ignore the bad correlation points by setting their Phi to identity matrix
    if ignoreBadPoints:
        PhiField[badPoints] = numpy.eye(4)*numpy.nan

    # if asked, replace the bad correlation points with the weighted influence of the k nearest good neighbours
    if correctBadPoints:
        # create the k-d tree of the coordinates of good points, we need this to search for the k nearest neighbours easily
        #   for details see: https://en.wikipedia.org/wiki/K-d_tree &
        #   https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.query.html

        from scipy.spatial import KDTree
        treeCoord = KDTree(fieldCoords[goodPoints])

        # extract the Phi matrices of the bad points
        fieldBad = numpy.zeros_like(PhiField[badPoints])
        fieldBad[:, -1, :] = numpy.array([0, 0, 0, 1])

        # check if we have asked only for the closest neighbour
        if neighbours == 1:

            # loop over each bad point
            for badPoint in range(badPoints[0].shape[0]):
                if verbose:
                    print("\rWorking on bad point: {} of {}".format(badPoint+1, badPoints[0].shape[0]), end='')
                # call tree.query to calculate:
                #   {ind}: the index of the nearest neighbour (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to the nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=neighbours)

                # replace bad point's Phi with the Phi of the nearest good point
                fieldBad[badPoint][:-1] = PhiField[goodPoints][ind][:-1].copy()

            # replace the corrected Phi field
            PhiField[badPoints] = fieldBad

        # if we have asked for more neighbours
        else:

            # loop over each bad point
            for badPoint in range(badPoints[0].shape[0]):
                if verbose:
                    print("\rWorking on bad point: {} of {}".format(badPoint+1, badPoints[0].shape[0]), end='')
                # call tree.query to calculate:
                #   {ind}: k nearest neighbours (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to each of the ith nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=neighbours)

                # compute the "Inverse Distance Weighting" since the nearest points should have the major influence
                weightSumInv = sum(1/distance)

                # loop over each good neighbour point:
                for neighbour in range(neighbours):
                    # calculate its weight
                    weightInv = (1/distance[neighbour])/float(weightSumInv)

                    # replace the Phi components of the bad point with the weighted Phi components of the ith nearest good neighbour
                    fieldBad[badPoint][:-1] += PhiField[goodPoints][ind[neighbour]][:-1]*weightInv

            # replace the corrected Phi field
            PhiField[badPoints] = fieldBad
        # overwrite RS to the corrected
        RS[badPoints] = 2

    # if asked, apply a median filter of a specific size in the Phi field
    if filterPoints:
        if verbose: print("\nFiltering...")
        import scipy.ndimage
        filterPointsRadius = int(filterPointsRadius)

        PhiField[:, 0, 0] = scipy.ndimage.generic_filter(PhiField[:, 0, 0].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 1, 0] = scipy.ndimage.generic_filter(PhiField[:, 1, 0].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 2, 0] = scipy.ndimage.generic_filter(PhiField[:, 2, 0].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        PhiField[:, 0, 1] = scipy.ndimage.generic_filter(PhiField[:, 0, 1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 1, 1] = scipy.ndimage.generic_filter(PhiField[:, 1, 1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 2, 1] = scipy.ndimage.generic_filter(PhiField[:, 2, 1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        PhiField[:, 0, 2] = scipy.ndimage.generic_filter(PhiField[:, 0, 2].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 1, 2] = scipy.ndimage.generic_filter(PhiField[:, 1, 2].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 2, 2] = scipy.ndimage.generic_filter(PhiField[:, 2, 2].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        PhiField[:, 0, -1] = scipy.ndimage.generic_filter(PhiField[:, 0, -1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 1, -1] = scipy.ndimage.generic_filter(PhiField[:, 1, -1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()
        PhiField[:, 2, -1] = scipy.ndimage.generic_filter(PhiField[:, 2, -1].reshape(fieldDims), numpy.nanmedian, size=(2*filterPointsRadius+1)).ravel()

        if ignoreBackGround:
            PhiField[backGroundPoints] = numpy.nan

    if saveFile:
        # if asked, write the corrected PhiField into a TSV
        if saveFileName:
            outDir = os.path.dirname(saveFileName)
            prefix = os.path.splitext(os.path.basename(saveFileName))[0]
        elif fileName:
            outDir = os.path.dirname(fileName)
            prefix = os.path.splitext(os.path.basename(fileName))[0]
        elif saveFileName is None and fileName is None:
            outDir = "."
            prefix = "spam"

        TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tF11\tF12\tF13\tZdisp\tF21\tF22\tF23\tYdisp\tF31\tF32\tF33\tXdisp\tSubPixReturnStat\tSubPixDeltaPhiNorm\tSubPixIterations\tPSCC"
        outMatrix = numpy.array([numpy.array(range(PhiField.shape[0])),
                                 fieldCoords[:, 0], fieldCoords[:, 1], fieldCoords[:, 2],
                                 PhiField[:, 0, 0],    PhiField[:, 0, 1],    PhiField[:, 0, 2],    PhiField[:, 0, 3],
                                 PhiField[:, 1, 0],    PhiField[:, 1, 1],    PhiField[:, 1, 2],    PhiField[:, 1, 3],
                                 PhiField[:, 2, 0],    PhiField[:, 2, 1],    PhiField[:, 2, 2],    PhiField[:, 2, 3],
                                 RS, deltaPhiNorm, iterations, PSCC]).T

        if filterPoints:
            title = "{}/{}-corrected-N{}-filteredRad{}.tsv".format(outDir, prefix, neighbours, filterPointsRadius)
        else:
            title = "{}/{}-corrected-N{}.tsv".format(outDir, prefix, neighbours)
        numpy.savetxt(title,
                      outMatrix,
                      fmt='%.7f',
                      delimiter='\t',
                      newline='\n',
                      comments='',
                      header=TSVheader)

    return PhiField


def interpolateField(fieldCoords, fieldValues, interpCoords, fieldInterpBinRatio=1):
    """
    Interpolate a field of deformation functions (Phi).

    Parameters
    ----------
    fieldCoords : nPointsField x 3 array
        Z Y X coordinates of points where ``fieldValues`` are defined

    fieldValues : nPointsField x 4 x 4 array
        Phi defined at ``fieldCoords``

    interpCoords : nPointsInterpolate x 3
        Z Y X coordinates of points to interpolate Phi for

    fieldInterpBinRatio : int, optional
        If the ``fieldCoords`` and ``fieldValues`` matrices refer to a binned version of the new coordintes.
        `e.g.`, if ``fieldInterpBinRatio = 2`` then ``fieldCoords`` and ``fieldValues`` have been calculated on an
        image half the size of what ``interpCoords`` are referring to.

    Returns
    -------
    interpValues : nPointsInterpolate x 4 x 4 array of Phis
    """

    # This version of the function will use scipy.ndimage.interpolation.map_coordinates().
    # It takes in a field, which means that our fieldValues Phi field MUST be regularly spaced.
    # Furthermore it takes points at integer values (voxels), so we have to convert from
    # positions in the Phi field, and the "real" voxel coordinates.
    # e.g., Our first measurement point is 12,12,12 and the node spacing is 20 pixels.
    # map_coordinates will access this first Phi 12,12,12 at a position [0,0,0] in the matrix of Phi values in space
    # The next Phi 32,12,12 at a position [1,0,0]
    # Define the output array
    output = numpy.zeros((interpCoords.shape[0], 4, 4))

    # 1. calculate node spacing and position of first point
    # Measure node spacing in all three directions:
    zUnique = numpy.unique(fieldCoords[:, 0])
    yUnique = numpy.unique(fieldCoords[:, 1])
    xUnique = numpy.unique(fieldCoords[:, 2])

    zSpacing = zUnique[1] - zUnique[0]
    ySpacing = yUnique[1] - yUnique[0]
    xSpacing = xUnique[1] - xUnique[0]

    if zSpacing == ySpacing and zSpacing == xSpacing:
        nodeSpacing = zSpacing

        # TopPoint -- Ask ER -- Elizabeth Regina -- Honni soit qui mal y pense
        taupPoihunt = [zUnique[0], yUnique[0], xUnique[0]]
        # print "Top point:", taupPoihunt

        nNodes = [int(1 + (zUnique[-1]-zUnique[0]) / zSpacing),
                  int(1 + (yUnique[-1]-yUnique[0]) / ySpacing),
                  int(1 + (xUnique[-1]-xUnique[0]) / xSpacing)]
    else:
        print("Not all node spacings are the same, help! {} {} {} ".format(
            zSpacing, ySpacing, xSpacing))
        return "moinsUn"

    # 2. reshape fieldValues into an Z*Y*X*Phiy*Phix array for map_coordinates
    fieldValues = fieldValues.reshape([nNodes[0], nNodes[1], nNodes[2], 4, 4])

    # 3. Convert interpCoords into positions in reshaped Phi array
    # If we have a non-zero bin, scale coordinates
    interpCoords /= fieldInterpBinRatio

    # Remove top corner coords...
    interpCoords -= taupPoihunt
    # And divide by node spacing, now coords are in 0->1 format
    interpCoords /= float(nodeSpacing)

    # 4. Call map_coordinates and return
    # Loop over each component of Phi, so they are not interpolated together.
    for Fy in range(4):
        for Fx in range(4):
            output[:, Fy, Fx] = scipy.ndimage.interpolation.map_coordinates(
                fieldValues[:, :, :, Fy, Fx], interpCoords.T, order=1)

    # 5. Scale transformation by binning value
    output[:, 0:3, 3] *= fieldInterpBinRatio
    return output

def mergeRegularGridAndDiscrete(
                fileNameRegularGrid=None,
                fileNameDiscreteA=None,
                labelledA=None,
                binningLabelledA=1,
                fileNameDiscreteB=None,
                labelledB=None,
                binningLabelledB=1,
                alwaysLabel=True,
                saveFileName=None):
    """
    This function merges displacement fields from the DICregularGrid script and 
    the DICdiscrete script.
    This can be useful where there are large flat zones in the image that cannot
    be correlated with small correlation windows, but can be identified and 
    tracked with a DICdiscrete computation.

    Parameters
    -----------
        fileNameRegularGrid : string
            File name of TSV from DICregularGrid client.
            Default = None

        fileNameDiscrete : string
            File name of TSV from DICdiscrete client
            Default = None

        labelled : 3D numpy array of ints
            Labelled volume used for discrete computation
            Default = None

        alwaysLabel : bool
            If regularGrid point falls inside the label, should we use the
            label displacement automatically?
            Otherwise if the reggularGrid point has converged should we use that?
            Default = True (always use Label displacement)

        saveFileName : string
            Output filename
            Default = None

    Returns
    --------
        Output matrix, with number of rows equal to DICregularGrid with columns:
            "NodeNumber", "Zpos", "Ypos", "Xpos", "Zdisp", "Ydisp", "Xdisp", "SubPixDeltaPhiNorm", "SubPixReturnStat", "SubPixIterations"
    """
    import spam.helpers

    regGrid  = spam.helpers.readTSV(fileNameRegularGrid)
    discreteA = spam.helpers.readTSV(fileNameDiscreteA)
    discreteB = spam.helpers.readTSV(fileNameDiscreteB)

    output = numpy.zeros([regGrid['fieldCoords'].shape[0], 10])

    from progressbar import ProgressBar
    pbar = ProgressBar()

    # For each point on the regular grid...
    for n, gridPoint in pbar(enumerate(regGrid['fieldCoords'].astype(int))):
        # Find labels corresponding to this grid position for the laeblled images
        labelA = labelledA[gridPoint[0]/binningLabelledA, gridPoint[1]/binningLabelledA, gridPoint[2]/binningLabelledA] 
        labelB = labelledB[gridPoint[0]/binningLabelledB, gridPoint[1]/binningLabelledB, gridPoint[2]/binningLabelledB] 

        # First column is point number
        output[n,0] = n 

        # Next three columns are the position of the regular grid point
        output[n,1:4] = gridPoint 

        # Is the point inside a discrete label?
        if ( labelA == 0 and labelB == 0 ) or ( not alwaysLabel and regGrid['SubPixReturnStat'][n] == 2):
            # If we're not in a label, copy the results from DICregularGrid
            output[n,4:7] = regGrid['PhiField'][n][0:3,-1] 
            output[n,7] = regGrid['SubPixDeltaPhiNorm'][n]
            output[n,8] = regGrid['SubPixReturnStat'][n]
            output[n,9] = regGrid['SubPixIterations'][n]
        else:
            # Give precedence to A field, conflicts not handled
            if labelA != 0:
                phi = discreteA['PhiField'][labelA].copy()
                phi[0:3,-1] *= float(binningLabelledA)
                output[n,4:7] = spam.DIC.decomposePhi( phi, PhiCentre=discreteA['fieldCoords'][labelA]*float(binningLabelledA), PhiPoint=gridPoint )['t'] 
                output[n,7] = discreteA['SubPixDeltaPhiNorm'][labelA]
                output[n,8] = discreteA['SubPixReturnStat'][labelA]
                output[n,9] = discreteA['SubPixIterations'][labelA]
            elif labelB != 0:
                phi = discreteB['PhiField'][labelB].copy()
                phi[0:3,-1] *= float(binningLabelledB)
                output[n,4:7] = spam.DIC.decomposePhi( phi, PhiCentre=discreteB['fieldCoords'][labelB]*float(binningLabelledB), PhiPoint=gridPoint )['t'] 
                output[n,7] = discreteB['SubPixDeltaPhiNorm'][labelB]
                output[n,8] = discreteB['SubPixReturnStat'][labelB]
                output[n,9] = discreteB['SubPixIterations'][labelB]

    #displacements = output[:,4:7].reshape([regGrid['fieldDims'][0],
                                           #regGrid['fieldDims'][1],
                                           #regGrid['fieldDims'][2],
                                           #3])

    #plt.imshow( displacements[:,24,:,0], vmin=0, vmax=3, cmap='plasma'); plt.show()

    if saveFileName is not None:
        numpy.savetxt( saveFileName,
                       output,
                       header="NodeNumber\tZpos\tYpos\tXpos\tZdisp\tYdisp\tXdisp\tSubPixDeltaPhiNorm\tSubPixReturnStat\tSubPixIterations",
                       delimiter="\t" )

    return output, regGrid['fieldDims']

def binning( im,
             binning,
             returnCropAndCentre=False ):
    """
    This function downscales images by averaging NxNxN voxels together in 3D and NxN pixels in 2D.
    This is useful for reducing data volumes, and denoising data (due to averaging procedure).

    Parameters
    ----------
        im : 2D/3D numpy array
            Input measurement field

        binning : int
            The number of pixels/voxels to average together

        returnCropAndCentre: bool (optional)
            Return the position of the centre of the binned image
            in the coordinates of the original image, and the crop
            Default = False

    Returns
    -------
        imBin : 2/3D numpy array
            `binning`-binned array

        (otherwise if returnCropAndCentre): list containing:
            imBin,
            topCrop, bottomCrop
            centre of imBin in im coordinates (useful for re-stitching)
    Notes
    -----
        Here we will only bin pixels/voxels if they is a sufficient number of
        neighbours to perform the binning. This means that the number of pixels that
        will be rejected is the dimensions of the image, modulo the binning amount. 

        The returned volume is computed with only fully binned voxels, meaning that some voxels on the edges
        may be excluded.
        This means that the output volume size is the input volume size / binning or less (in fact the crop
        in the input volume is the input volume size % binning
    """
    twoD = False
    import DICToolkit

    if im.dtype == 'f8': im = im.astype('<f4')

    binning = int(binning)
    #print("binning = ", binning)

    dimsOrig = numpy.array(im.shape)
    #print("dimsOrig = ", dimsOrig)

    # Note: // is a floor-divide
    imBin = numpy.zeros(dimsOrig//binning, dtype=im.dtype)
    #print("imBin.shape = ", imBin.shape)

    # Calculate number of pixels to throw away
    offset = dimsOrig % binning
    #print("offset = ", offset)

    # Take less off the top corner than the bottom corner
    topCrop = offset // 2
    #print("topCrop = ", topCrop)
    topCrop = topCrop.astype('<i2')

    if len(im.shape) == 2:
        # pad them
        im = im[numpy.newaxis, ...]
        imBin = imBin[numpy.newaxis, ...]
        topCrop = numpy.array([ 0, topCrop[0], topCrop[1] ]).astype('<i2')
        offset  = numpy.array([ 0, offset[0],  offset[1]  ]).astype('<i2')
        twoD = True

    # Call C++
    if im.dtype == 'f4':
        print("Float binning")
        DICToolkit.binningFloat(im, imBin, topCrop, binning)
    elif im.dtype == 'u2':
        print("Uint 2 binning")
        DICToolkit.binningUInt(im, imBin, topCrop, binning)
    elif im.dtype == 'u1':
        print("Char binning")
        DICToolkit.binningChar(im, imBin, topCrop, binning)

    if returnCropAndCentre:
        centreBinned = (numpy.array(imBin.shape)-1)/2.0
        relCentOrig = offset+binning*centreBinned
        return [imBin, [topCrop, offset-topCrop],  relCentOrig]
    else:
        return imBin
