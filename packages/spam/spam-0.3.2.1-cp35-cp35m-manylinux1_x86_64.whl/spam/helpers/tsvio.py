"""
This module offers a set functions in order to manipulate TSV files.
It writes, reads, cleans and visualises TSV files used in DIC clients.
"""

from __future__ import print_function
import numpy
import os


def writeRegistrationTSV(fileName, regCentre, regReturns):
    '''
    This function writes a correctly formatted TSV file from the result of a single lucasKanade call, allowing it to be used as an initial registration.

    Parameters
    ----------
        fileName : string
            The file name for output, suggestion: it should probably end with ".tsv"

        regCentre : 3-component list
            A list containing the point at which `PhiCentre` has been measured.
            This is typically the middle of the image, and can be obtained as follows:
            (numpy.array( im.shape )-1)/2.0
            The conversion to a numpy array is necessary, since tuples cannot be divided by a number directly.

        regReturns : dictionary
            This should be the return dictionary from `lucasKanade`.
            From this dictionary will be extracted: 'PhiCentre', 'error', 'iterationNumber', 'returnStatus', 'deltaPhiNorm'

    '''
    regPhi = regReturns['PhiCentre']

    # catch 2D images
    if len(regCentre) == 2:
        regCentre = [1, regCentre[0], regCentre[1]]

    # Make one big array for writing:
    #   First the node number,
    #   3 node positions,
    #   Phi[0:3,0:2]
    #   Pixel-search CC
    #   SubPixError, SubPixIterations, SubPixelReturnStatus
    TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tF11\tF12\tF13\tZdisp\tF21\tF22\tF23\tYdisp\tF31\tF32\tF33\tXdisp\tSubPixError\tSubPixIterations\tSubPixReturnStat\tSubPixDeltaPhiNorm"
    outMatrix = numpy.array([[1],
                             [regCentre[0]],
                             [regCentre[1]],
                             [regCentre[2]],
                             [regPhi[0, 0]],
                             [regPhi[0, 1]],
                             [regPhi[0, 2]],
                             [regPhi[0, 3]],
                             [regPhi[1, 0]],
                             [regPhi[1, 1]],
                             [regPhi[1, 2]],
                             [regPhi[1, 3]],
                             [regPhi[2, 0]],
                             [regPhi[2, 1]],
                             [regPhi[2, 2]],
                             [regPhi[2, 3]],
                             [regReturns['error']],
                             [regReturns['iterationNumber']],
                             [regReturns['returnStatus']],
                             [regReturns['deltaPhiNorm']]])

    numpy.savetxt(fileName,
                  outMatrix.T,
                  fmt='%.7f',
                  delimiter='\t',
                  newline='\n',
                  comments='',
                  header=TSVheader)

def readTSV(fileName, fieldBinRatio=1.0, readDisplacements=False, readFs=False, readConvergence=False, readPixelSearchCC=False, readEverything=True, returnFs=True):
    """
    This function reads a TSV file containing a field of transformation operators **Phi** at a number of points.
    This is typically the output of the DICdiscrete and DICregularGrid clients

    Parameters
    ----------
        fileName : string
            Name of the file

        fieldBinRatio : int, optional
            if the input field is refer to a binned version of the image
            `e.g.`, if ``fieldBinRatio = 2`` the field_name values have been calculated
            for an image half the size of what the returned PhiField is referring to
            Default = 1.0

        readDisplacements : bool, optional
            Read "zDisp", "yDisp", "xDisp", displacements from the TSV file, and not the rest of the Phi matrix?
            Default = False

        readFs : bool, optional
            Read full Phi matrices from the TSV file?
            Same as displacements with also "F11" to "F33" columns
            Default = False

        readConvergence : bool, optional
            Read "SubPixReturnStat", "SubPixDeltaPhiNorm", "SubPixIterations" from file
            Default = False

        readPixelSearchCC : bool, optional
            Read "PSCC" from file
            Default = False

        readEverything : bool, optional
            Activates "readFs", "readConvergence", "readPixelSearchCC"
            Default = True

        returnFs : bool, optional
            Even with only displacements, return a full F?
            Default = True


    Returns
    -------
        Dictionary containing:
            fieldDims: 1x3 array of the field dimensions (ZYX) (for a regular grid DIC result)

            numberOfLabels: number of labels (for a discrete DIC result)

            fieldCoords: nx3 array of n points coordinates (ZYX)

            PhiField: nx4x4 array of n points transformation operators

            SubPixReturnStat: nx1 array of n points SubPixelReturnStatus from the correlation

            SubPixDeltaPhiNorm: nx1 array of n points SubPixelDeltaFnorm from the correlation

            SubPixIterations: nx1 array of n points SubPixelIterations from the correlation

            PSCC: nx1 array of n points PixelSearchCC from the correlation
    """
    if not os.path.isfile(fileName):
        print("\n\tspam.tsvio.readTSV(): {} is not a file. Exiting.".format(fileName))
        return

    if readDisplacements:
        readFs = False
        readEverything = False

    if readDisplacements:
        readFs = False
        readEverything = False

    if readEverything:
        readFs = True
        readConvergence = True
        returnFs = True
        readPixelSearchCC = True


    f = numpy.genfromtxt(fileName, delimiter="\t", names=True)
    #RS = []
    #deltaPhiNorm = []
    #PSCC = []

    # If this is a one-line TSV file (an initial registration for example)
    if f.size == 1:
        print("\tspam.tsvio.readTSV(): {} seems only to have one line.".format(fileName))
        nPoints = 1
        numberOfLabels = 1
        fieldDims = [1, 1, 1]

        # Sort out the field coordinates
        fieldCoords = numpy.zeros((nPoints, 3))
        fieldCoords[:, 0] = f['Zpos']*fieldBinRatio
        fieldCoords[:, 1] = f['Ypos']*fieldBinRatio
        fieldCoords[:, 2] = f['Xpos']*fieldBinRatio

        # Sort out the components of Phi
        PhiField = numpy.zeros((nPoints, 4, 4))
        PhiField[0] = numpy.eye(4)

        # Fill in displacements
        try:
            PhiField[0, 0, 3] = f['Zdisp']*fieldBinRatio
            PhiField[0, 1, 3] = f['Ydisp']*fieldBinRatio
            PhiField[0, 2, 3] = f['Xdisp']*fieldBinRatio
        except ValueError:
            PhiField[0, 0, 3] = f['F14']*fieldBinRatio
            PhiField[0, 1, 3] = f['F24']*fieldBinRatio
            PhiField[0, 2, 3] = f['F34']*fieldBinRatio

        if readFs:
            # Get non-displacement components
            PhiField[0, 0, 0] = f['F11']
            PhiField[0, 0, 1] = f['F12']
            PhiField[0, 0, 2] = f['F13']
            PhiField[0, 1, 0] = f['F21']
            PhiField[0, 1, 1] = f['F22']
            PhiField[0, 1, 2] = f['F23']
            PhiField[0, 2, 0] = f['F31']
            PhiField[0, 2, 1] = f['F32']
            PhiField[0, 2, 2] = f['F33']

        if readConvergence:
            # Return ReturnStatus, SubPixelDeltaFnorm, SubPixelIterations
            RS = f['SubPixReturnStat']
            deltaPhiNorm = f['SubPixDeltaPhiNorm']
            iterations = f['SubPixIterations']

        PSCC = 0

    # there is more than one line in the TSV file -- a field -- typical case
    else:
        nPoints = f.size

         # check if it is a DICdiscrete or DICregularGrid result
        try:
            f["NodeNumber"]
            # it's a local DIC result with grid points regularly spaced
            DICgrid = True
            DICdiscrete = False
        except ValueError:
            # it's a discrete DIC result with values in each label's centre of mass
            DICdiscrete = True
            DICgrid = False


        # Sort out the field coordinates
        fieldCoords = numpy.zeros((nPoints, 3))
        fieldCoords[:, 0] = f['Zpos']*fieldBinRatio
        fieldCoords[:, 1] = f['Ypos']*fieldBinRatio
        fieldCoords[:, 2] = f['Xpos']*fieldBinRatio

        if DICgrid:
            fieldDims = numpy.array([len(numpy.unique(f['Zpos'])), len(numpy.unique(f['Ypos'])), len(numpy.unique(f['Xpos']))])
            numberOfLabels = 0
            print("\tspam.tsvio.readTSV(): Field Dimensions: {}".format(fieldDims))
        elif DICdiscrete:
            numberOfLabels = len(f["Label"])
            fieldDims = [0, 0, 0]
            print("\tspam.tsvio.readTSV(): Number of labels: {}".format(numberOfLabels))

        # create ReturnStatus and deltaPhiNorm matrices if asked
        if readConvergence:
            RS = numpy.zeros(nPoints)
            RS[:] = f[:]['SubPixReturnStat']
            deltaPhiNorm = numpy.zeros(nPoints)
            deltaPhiNorm = f[:]['SubPixDeltaPhiNorm']
            iterations = numpy.zeros(nPoints)
            iterations = f[:]['SubPixIterations']

        # Return pixelSearchCC
        if readPixelSearchCC:
            PSCC = numpy.zeros(nPoints)
            try:
                PSCC = f[:]['PSCC']
            except ValueError:
                pass

        # Sort out the components of Phi
        PhiField = numpy.zeros((nPoints, 4, 4))
        for n in range(nPoints):
            # Initialise with Identity matrix
            PhiField[n] = numpy.eye(4)

            # Fill in displacements
            try:
                PhiField[n, 0, 3] = f[n]['Zdisp']*fieldBinRatio
                PhiField[n, 1, 3] = f[n]['Ydisp']*fieldBinRatio
                PhiField[n, 2, 3] = f[n]['Xdisp']*fieldBinRatio
            except ValueError:
                PhiField[n, 0, 3] = f[n]['F14']*fieldBinRatio
                PhiField[n, 1, 3] = f[n]['F24']*fieldBinRatio
                PhiField[n, 2, 3] = f[n]['F34']*fieldBinRatio

            if readFs:
                # Get non-displacement components
                PhiField[n, 0, 0] = f[n]['F11']
                PhiField[n, 0, 1] = f[n]['F12']
                PhiField[n, 0, 2] = f[n]['F13']
                PhiField[n, 1, 0] = f[n]['F21']
                PhiField[n, 1, 1] = f[n]['F22']
                PhiField[n, 1, 2] = f[n]['F23']
                PhiField[n, 2, 0] = f[n]['F31']
                PhiField[n, 2, 1] = f[n]['F32']
                PhiField[n, 2, 2] = f[n]['F33']

    output = {"fieldDims": fieldDims,
              "numberOfLabels": numberOfLabels,
              "fieldCoords": fieldCoords}
    if readConvergence:
        output.update({"SubPixReturnStat": RS,
                       "SubPixDeltaPhiNorm": deltaPhiNorm,
                       "SubPixIterations": iterations })
    if readPixelSearchCC:
        output.update({"PixelSearchCC": PSCC})

    if readDisplacements and not returnFs:
        output.update({"Displacements": PhiField[:,0:3,-1]})
    else:
        output.update({"PhiField": PhiField})

    return output

def TSVtoTIFF(fileName, fieldBinRatio=1.0, lab=None, returnRS=False, outDir=None, prefix=None):
    '''
    This function converts a TSV file (typically the output of the DICdiscrete and DICregularGrid clients)
    to a tiff file for visualising the Phi field.

    Parameters
    ----------
        fileName : string
            Name of the file

        fieldBinRatio : int, optional
            if the input field is refer to a binned version of the image
            `e.g.`, if ``fieldBinRatio = 2`` the field_name values have been calculated
            for an image half the size of what the returned PhiField is referring to
            Default = 1.0

        lab : 3D numpy array, optional
            The labelled image of the reference state. Highly recommended argument in case of a discrete correlation result.
            Default = None

        returnRS : bool, optional
            if True: will return the SubPixelReturnStatus of the correlation as a tiff file
            Default = False

        outDir : string, optional
            Output directory
            Default is the dirname of the input file

        prefix : string, optional
            Prefix for output files
            Default is the basename of the input file (without extension)
    '''

    import tifffile
    # use the helper function to read the TSV file
    fi = readTSV(fileName, fieldBinRatio=fieldBinRatio, readDisplacements=True, readConvergence=returnRS)
    PhiField = fi["PhiField"]
    PhiComponents = [['Zdisp', 0, 3],
                     ['Ydisp', 1, 3],
                     ['Xdisp', 2, 3]]

    # output file directory
    if outDir is None:
        outDir = os.path.dirname(fileName)

    # output file name prefix
    if prefix is None:
        prefix = os.path.splitext(os.path.basename(fileName))[0]

    # check if it is a DICdiscrete result
    if fi["numberOfLabels"] != 0:
        if lab:
            labelled = tifffile.imread(lab)
            import spam.label.toolkit as ltk

            for component in PhiComponents:
                tifffile.imsave("{}/{}-{}.tif".format(outDir, prefix, component[0]),
                                ltk.convertLabelToFloat(labelled, PhiField[:, component[1], component[2]]).astype('<f4'))
            if returnRS:
                tifffile.imsave("{}/{}-RS.tif".format(outDir, prefix),
                                ltk.convertLabelToFloat(labelled, fi["SubPixReturnStat"]).astype('<f4'))
        else:
            print ("\tspam.tsvio.TSVtoTIFF(): The labelled image of the reference state is needed as input. Exiting.")
            return

    # if not, is a DICregularGrid result
    else:
        dims = fi["fieldDims"]

        for component in PhiComponents:
            tifffile.imsave("{}/{}-{}.tif".format(outDir, prefix, component[0]),
                            PhiField[:, component[1], component[2]].reshape(dims).astype('<f4'))

        if returnRS:
            tifffile.imsave("{}/{}-RS.tif".format(outDir, prefix),
                            fi["SubPixReturnStat"].reshape(dims).astype('<f4'))

def TSVtoVTK(fileName, fieldBinRatio=1.0, pixelSize=1.0, returnRS=False, outDir=None, prefix=None):
    '''
    This function converts a TSV file (typically the output of the DICdiscrete and DICregularGrid clients)
    to a vtk file for visualising the F field.

    Parameters
    ----------
        fileName : string
            Name of the file

        fieldBinRatio : int, optional
            if the input field is refer to a binned version of the image
            `e.g.`, if ``fieldBinRatio = 2`` the field values have been calculated
            for an image half the size of what the returned PhiField is referring to
            Default = 1.0

        pixelSize: float
            physical size of a pixel (i.e. 1mm/px)
            Default = 1.0

        returnRS : bool, optional
            if True: will return the SubPixelReturnStatus of the correlation
            Default = False

        outDir : string
            Output directory
            Default is the dirname of input file

        prefix : string
            Prefix for output files
            Default is the basename of input file (without extension)
    '''
    import spam.helpers
    # use the helper function to read the TSV file
    fi = readTSV(fileName, fieldBinRatio=fieldBinRatio)
    PhiField = fi["PhiField"]

    # output file directory
    if outDir is None:
        outDir = os.path.dirname(fileName)

    # output file name prefix
    if prefix is None:
        prefix = os.path.splitext(os.path.basename(fileName))[0]

    # check if it is a DICdiscrete result
    if fi["numberOfLabels"] != 0:
        coords = fi["fieldCoords"][1:] * pixelSize
        if not returnRS:
            pointData = {"XYZdisp":  PhiField[1:, :-1, 3] * pixelSize}

        else:
            pointData = {"XYZdisp":  PhiField[1:, :-1, 3] * pixelSize,
                         "RS": fi["SubPixReturnStat"][1:]}

        spam.helpers.writeGlyphsVTK(coords, pointData, fileName="{}/{}.vtk".format(outDir, prefix))

    # if not, is a DICregularGrid result
    else:
        dims = fi["fieldDims"]
        coords = fi["fieldCoords"] * pixelSize
        aspectRatio = numpy.array([numpy.unique(coords[:, 0])[1]-numpy.unique(coords[:, 0])[0], numpy.unique(coords[:, 1])[1]-numpy.unique(coords[:, 1])[0], numpy.unique(coords[:, 2])[1]-numpy.unique(coords[:, 2])[0]])

        if not returnRS:
            cellData = {"XYZdisp":  (PhiField[:, :-1, 3] * pixelSize).reshape((dims[0], dims[1], dims[2], 3))}

        else:
            cellData = {"XYZdisp":  (PhiField[:, :-1, 3] * pixelSize).reshape((dims[0], dims[1], dims[2], 3)),
                        "RS": fi["SubPixReturnStat"].reshape(dims[0], dims[1], dims[2])}

        spam.helpers.writeStructuredVTK(aspectRatio=aspectRatio, cellData=cellData, fileName="{}/{}.vtk".format(outDir, prefix))
