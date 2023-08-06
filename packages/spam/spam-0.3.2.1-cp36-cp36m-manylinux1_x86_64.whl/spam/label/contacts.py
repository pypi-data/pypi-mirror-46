
from __future__ import print_function

from . import labelToolkit
import numpy

from collections import deque
import scipy.ndimage #for the contact detection
from skimage.feature import peak_local_max #for the maxima of the EDM
import time
import multiprocessing #for contact detection and orientation of assemblies
import spam.label

contactType = '<u4'


def contactingLabels(lab, labels, areas=False, boundingBoxes=None, centresOfMass=None):
    """
    This function returns contacting labels for a given label or list of labels,
    and optionally the number of voxels involved in the contact.
    This is designed for an interpixel watershed where there are no watershed lines,
    and so contact detection is done by dilating the particle in question once and
    seeing what other labels in comes in contact with.

    Parameters
    -----------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background

        labels : int or a list of labels
            Labels for which we should compute neighbours

        areas : bool, optional (default = False)
            Compute contact "areas"? *i.e.*, number of voxels
            Careful, this is not a physically correct quantity, and
            is measured only as the overlap from ``label`` to its
            neightbours. See ``c    ontactPoint`` for something
            more meaningful

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        centresOfMass : lab.max()x3 array of floats, optional
            Centres of mass in format returned by ``centresOfMass``.
            If not defined (Default = None), it is recomputed by running ``centresOfMass``

    Returns
    --------
        For a single "labels", a list of contacting labels.
        if areas == True, then a list of "areas" is also returned.

        For multiple labels, as above but a lsit of lists in the order of the labels

    Note
    -----
        Because of dilation, this function is not very safe at the edges,
        and will throw an exception
    """
    # Default state for single
    single = False

    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)
    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(lab, boundingBoxes=boundingBoxes)

    # I guess there's only one label
    if type(labels) != list:
        labels = [labels]
        single = True

    contactingLabels = []
    contactingAreas  = []

    for label in labels:
        # catch zero and return it in order to keep arrays aligned
        if label == 0:
            contactingLabels.append([0])
        else:
            p1 = spam.label.getLabel(lab, label,
                            boundingBoxes=boundingBoxes,
                            centresOfMass=centresOfMass,
                            margin=2)
            p2 = spam.label.getLabel(lab, label,
                            boundingBoxes=boundingBoxes,
                            centresOfMass=centresOfMass,
                            margin=2,
                            labelDilate=1)

            dilOnly = numpy.logical_xor(p2['subvol'], p1['subvol'])

            labSlice = lab[ p1['slice'][0].start:p1['slice'][0].stop,
                            p1['slice'][1].start:p1['slice'][1].stop,
                            p1['slice'][2].start:p1['slice'][2].stop]

            if (dilOnly.shape == labSlice.shape):
                intersection = dilOnly * labSlice

                counts = numpy.unique(intersection, return_counts=True)

                # Print counts starting from the 1th column since we'll always have a ton of zeros
                # print "\tLabels:\n\t",counts[0][1:]
                # print "\tCounts:\n\t",counts[1][1:]

                contactingLabels.append(counts[0][1:])
                if areas:
                    contactingAreas.append(counts[1][1:])

            else:
                raise Exception('\tdilOnly and labSlice are not the same size... getLabel probably did some safe cutting around the edges')

    # Flatten if it's a list with only one object
    if single:
        contactingLabels = contactingLabels[0]
        if areas:
            contactingAreas = contactingAreas[0]
    # Now return things
    if areas:
        return [contactingLabels, contactingAreas]
    else:
        return contactingLabels


def detectAndFixOversegmentation(lab, nVoxThreshold=25):
    """
    This function runs on a labelled image, detects very large contacts
    and assumes they are oversegmentation, so labels the grains with the
    same (lowest) label.
    This is recursive, so a label that is merged is re-treated as a larger
    grain, which is checked again.

    Parameters
    ----------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background

        nVoxThreshold : int, optional (default=25)
            Number of voxels to consider a big contact.
            This should be a function of the volume, someone please implement it.

    Returns
    --------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background.
            If any labels have merged, the labels will be discontinuous integers,
            running spam.label.toolkit.makeLabelsSequential is recommended.
    """
    lab = lab.astype(spam.label.labelType)
    bb = spam.label.boundingBoxes(lab)
    com = spam.label.centresOfMass(lab)
    numberOfLabels = lab.max()

    stack = deque()

    for label in range(1, numberOfLabels+1):
        stack.append(label)
    stack.reverse()

    # Define a label mapping
    relabelMap = numpy.arange(0, numberOfLabels+1, 1, dtype=spam.label.labelType)

    while len(stack) > 0:
        # for label in [163]:
        label = stack.pop()
        print("\rcontacts.detectOversegmentation(): Label {}/{}".format(label, numberOfLabels), end=''),

        # The contactingLabels is not safe on the edges,
        #   so catch the exception that it throws
        try:
            contactLabels, contactAreas = contactingLabels( lab, label, areas=True, centresOfMass=com, boundingBoxes=bb)
            # print contactLabels, contactAreas
        except:
            #print("\nlabel close to the edge, skipping")
            continue

        # See if any contact areas are bigger than the threhold.
        # TODO: Make this a function of the volume
        bigContactsMask = contactAreas > nVoxThreshold

        # If any contact areas are bigger than the threhsold...
        if bigContactsMask.sum() != 0:
            # print "\n\tFound big contacts! Replacing that Grain, and starting again"

            # For all bigger-than areas...
            for pos in numpy.where(bigContactsMask == True)[0]:
                # print pos
                # print contactLabels
                relabelMap[contactLabels[pos]] = label
                labelToolkit.relabel(lab, relabelMap)
                #lab[ lab == contactLabels[pos] ] = label

            stack.append(label)

    print("\n")

    return lab


def getContactPoints( lab, contactPairs, returnContactZones=False, boundingBoxes=None, centresOfMass=None ):  print("spam.label.getContactPoints(): This function has been renamed to contactPoints, please update your code"); return
def contactPoints( lab, contactPairs, returnContactZones=False, boundingBoxes=None, centresOfMass=None ):
    """
    Get the point, or area of contact between contacting particles.
    This is done by looking at the overlap of a 1-dilation of particle1 onto particle 2
    and vice versa.

    Parameters
    -----------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background

        contactPairs : list (or list of list) of labels
            Pairs of labels for which we should compute neighbours

        returnContactZones : bool, optional (default = False)
            Output a labelled volume where contact zones are labelled according to the order
            of contact pairs?
            If False, the centres of mass of the contacts are returned

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        centresOfMass : lab.max()x3 array of floats, optional
            Centres of mass in format returned by ``centresOfMass``.
            If not defined (Default = None), it is recomputed by running ``centresOfMass``

    Returns
    --------
        if returnContactZones:
            lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
        else:
            Z Y X Centres of mass of contacts
    """
    # detect list of lists with code from: https://stackoverflow.com/questions/5251663/determine-if-a-list-contains-other-lists
    #if not any(isinstance(el, list) for el in contactPairs ):
        #contactPairs = [ contactPairs ]
    # different approach:
    contactPairs = numpy.array(contactPairs)
    # Pad with extra dim if only one contact pair
    if len(contactPairs.shape) == 1:
        contactPairs = contactPairs[numpy.newaxis, ...]

    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)
    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(lab, boundingBoxes=boundingBoxes)

    # To this volume will be added each contact "area", labelled
    # with the contact pair number (+1)
    analysisVolume = numpy.zeros_like(lab)

    for n, contactPair in enumerate( contactPairs ):
        # Do both orders in contacts
        if len(contactPair) != 2:
            print("spam.label.contacts.contactPoints(): contact pair does not have 2 elements")
        for label1, label2 in [ contactPair, contactPair[::-1] ]:
            #print( "Label1: {} Label2: {}".format( label1, label2 ) )
            p1 = spam.label.getLabel(lab, label1,
                            boundingBoxes=boundingBoxes,
                            centresOfMass=centresOfMass,
                            margin=2)
            p2 = spam.label.getLabel(lab, label1,
                            boundingBoxes=boundingBoxes,
                            centresOfMass=centresOfMass,
                            margin=2,
                            labelDilate=1)

            dilOnly = numpy.logical_xor(p2['subvol'], p1['subvol'])

            labSlice  = [slice(p1['slice'][0].start,p1['slice'][0].stop),
                         slice(p1['slice'][1].start,p1['slice'][1].stop),
                         slice(p1['slice'][2].start,p1['slice'][2].stop)]

            labSubvol = lab[ labSlice ]

            if (dilOnly.shape == labSubvol.shape):
                intersection = dilOnly * labSubvol

                analysisVolume[ labSlice ][ intersection==label2 ] = n+1

            else:
                raise Exception(
                    '\tdilOnly and labSlice are not the same size... getLabel probably did some safe cutting around the edges')

    if returnContactZones:
        return analysisVolume
    else:
        return spam.label.centresOfMass( analysisVolume )


def _labelledContacts( lab, maximumCoordinationNumber=20 ):
    """
    Uniquely names contacts based on grains.

    Parameters
    -----------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background

        maximumCoordinationNumber : int (optional, default = 20)
            Maximum number of neighbours to consider per grain

    Returns
    --------
        contactList : array of ints
            2D Array of lab.max()+1 by  2*maximumCoordinationNumber
            containing, per grain: touching grain label, contact number
    """
    #print( "\tlabel.contacts.labelledContacts(): Creating big contact-labels list of lists of lists", end='' )
    contactStruct = []
    for i in range( lab.max()+1 ):
        contactStruct.append(  []  )
    #print( "...done" )

    # Initialise counter
    currentContactNumber = 1

    arrayOut = numpy.zeros( ( lab.max()+1, 2 * maximumCoordinationNumber ), dtype='<u4' )
    contactsPerParticle = numpy.zeros( ( lab.max()+1 ), dtype='<u1' )

    for label in range( 1, lab.max()+1 ):
        print( "\r\tlabel.contacts.labelledContacts() progress: {}".format( label ), end='' )
        contactingLabels = spam.label.contactingLabels( lab, label )

        # Keep only ones smaller than the current label
        smallerContactingLabels = contactingLabels[ contactingLabels < label ]

        for smallerContactingLabel in smallerContactingLabels:
            #contactStruct[ smallerContactingLabel ].append( [ label, currentContactNumber  ] )
            # plus add corresponding label in larger labelled grain
            #contactStruct[ label ].append( [ smallerContactingLabel, currentContactNumber  ] )
            if contactsPerParticle[label] < maximumCoordinationNumber and  contactsPerParticle[smallerContactingLabel] < maximumCoordinationNumber :
                arrayOut[ smallerContactingLabel, 2*contactsPerParticle[smallerContactingLabel]+0 ] = label
                arrayOut[ smallerContactingLabel, 2*contactsPerParticle[smallerContactingLabel]+1 ] = currentContactNumber
                contactsPerParticle[smallerContactingLabel] += 1
                # plus add corresponding label in larger labelled grain
                arrayOut[ label, 2*contactsPerParticle[label]+0 ] = smallerContactingLabel
                arrayOut[ label, 2*contactsPerParticle[label]+1 ] = currentContactNumber
                contactsPerParticle[label] += 1
                currentContactNumber += 1
    print()
    #print( "\n",contactStruct )

    #print "\n\n=== contact_voxel_labels Summary ==="
    #print "Unwrapping list of list of lists..."

    #TSVLabels = []
    #for i in range( maximumCoordinationNumber ):
        #TSVLabels.append("ContactingLabel_%i"%i)
        #TSVLabels.append("ContactLabel_%i"%i)

    #for i in range( lab.max()+1 ):
        ## The current grain label
        ##arrayOut[ i ][ 0 ] = i
        ## Check if there are contacts in the structure
        #if len( contactStruct[i] ) > 0:
            #for j in range( min( len( contactStruct[i] ), maximumCoordinationNumber ) ):
                #arrayOut[ i ][ (j*2)+0 ] = contactStruct[i][j][0]
                #arrayOut[ i ][ (j*2)+1 ] = contactStruct[i][j][1]

    return arrayOut


def labelledContacts( lab, maximumCoordinationNumber=20 ):
    """
    Uniquely names contacts based on grains.

    Parameters
    -----------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background

        maximumCoordinationNumber : int (optional, default = 20)
            Maximum number of neighbours to consider per grain

    Returns
    --------
        An array, containing:
            contactVolume : array of ints
                3D array where contact zones are uniquely labelled

            Z : array of ints
                Vector of length lab.max()+1 contaning the coordination number
                (number of touching labels for each label)

            contactTable : array of ints
                2D array of lab.max()+1 by  2*maximumCoordinationNumber
                containing, per grain: touching grain label, contact number

            contactingLabels : array of ints
                2D array of numberOfContacts by 2
                containing, per contact: touching grain label 1, touching grain label 2
    """
    contacts        = numpy.zeros_like( lab, dtype=contactType )
    Z               = numpy.zeros( ( lab.max()+1 ), dtype='<u1' )
    contactTable    = numpy.zeros( ( lab.max()+1,  maximumCoordinationNumber*2 ), dtype=contactType )
    contactingLabels= numpy.zeros( ( (lab.max()+1)*maximumCoordinationNumber, 2 ), dtype=spam.label.labelType )

    labelToolkit.labelContacts( lab, contacts, Z, contactTable, contactingLabels )

    # removed the first row of contactingLabels, as it is 0, 0
    return [ contacts, Z, contactTable, contactingLabels[1:contacts.max()+1,:] ]


def fetchTwoGrains(volLab,volGrey,labels,boundingBoxes=None,padding=0,size_exclude=5):
    """
    fetches the sub-volume of two grains from a labelled image

    Parameters
    ----------
        volLab : 3D array of integers
            Labelled volume, with lab.max() labels

        volGrey : 3D array
            Grey-scale volume

        labels : 1x2 array of integers
            the two labels that should be contained in the subvolume

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        padding : integer
            padding of the subvolume
            for some purpose it might be benefitial to have a subvolume
            with a boundary of zeros

    Returns
    -------
        subVolLab : 3D array of integers
            labelled sub-volume containing the two input labels

        subVolBin : 3D array of integers
            binary subvolume

        subVolGrey : 3D array
            grey-scale subvolume
    """

    # check if bounding boxes are given
    if boundingBoxes is None:
        #print "bounding boxes are not given. calculating ...."
        boundingBoxes = spam.label.boundingBoxes(volLab)
    #else:
        #print "bounding boxes are given"
    lab1, lab2 = labels
    # get coordinates of the big bounding box
    startZ = min( boundingBoxes[lab1,0], boundingBoxes[lab2,0] ) - padding
    stopZ  = max( boundingBoxes[lab1,1], boundingBoxes[lab2,1] ) + padding
    startY = min( boundingBoxes[lab1,2], boundingBoxes[lab2,2] ) - padding
    stopY  = max( boundingBoxes[lab1,3], boundingBoxes[lab2,3] ) + padding
    startX = min( boundingBoxes[lab1,4], boundingBoxes[lab2,4] ) - padding
    stopX  = max( boundingBoxes[lab1,5], boundingBoxes[lab2,5] ) + padding

    subVolLab = volLab[startZ:stopZ+1, startY:stopY+1, startX:stopX+1]

    subVolLab_A = numpy.where( subVolLab == lab1, lab1, 0 )
    subVolLab_B = numpy.where( subVolLab == lab2, lab2, 0 )
    subVolLab = subVolLab_A + subVolLab_B
    
    struc = numpy.zeros((3,3,3))
    struc[1,1:2,:]=1
    struc[1,:,1:2]=1
    struc[0,1,1]=1
    struc[2,1,1]=1
    subVolLab = spam.label.filterIsolatedCells(subVolLab, struc, size_exclude)

    subVolBin = numpy.where( subVolLab != 0, 1, 0 )

    subVolGrey = volGrey[startZ:stopZ+1, startY:stopY+1, startX:stopX+1]
    subVolGrey = subVolGrey * subVolBin

    return subVolLab, subVolBin, subVolGrey


def localDetection(subVolGrey,localThreshold,radiusThresh=None):
    """
    local contact refinement
    checks whether two particles are in contact with a local threshold,
    that is higher than the global one used for binarisation

    Parameters
    ----------
        subVolGrey : 3D array
            Grey-scale volume

        localThreshold : integer or float, same type as the 3D array
            threshold for binarisation of the subvolume

        radiusThresh : integer, optional
            radius for excluding patches that might not be relevant,
            e.g. noise can lead to patches that are not connected with the grains in contact
            the patches are calculated with ``equivalentRadii()``
            Default is None and such patches are not excluded from the subvolume

    Returns
    -------
        CONTACT : boolean
            if True, that particles appear in contact for the local threshold

    Note
    ----
        see https://doi.org/10.1088/1361-6501/aa8dbf for further information
    """

    CONTACT = False
    subVolBin = ((subVolGrey > localThreshold)*1).astype('uint8')
    if radiusThresh is not None:
        # clean the image of isolated voxels or pairs of voxels
        # due to higher threshold they could exist
        subVolLab, numObjects = scipy.ndimage.measurements.label(subVolBin)
        if numObjects > 1:
            radii = spam.label.equivalentRadii( subVolLab )
            labelsToRemove = numpy.where( radii < radiusThresh )
            if len(labelsToRemove[0]) > 1:
                subVolLab = spam.label.removeLabels( subVolLab, labelsToRemove)
        subVolBin = ((subVolLab > 0)*1).astype('uint8')

    # fill holes
    subVolBin = scipy.ndimage.morphology.binary_fill_holes(subVolBin).astype('uint8')
    labeledArray, numObjects = scipy.ndimage.measurements.label(subVolBin, structure=None, output=None)
    if numObjects == 1:
        CONTACT = True

    return CONTACT


def contactOrientations(volBin,volLab,watershed="ITK",markerShrink=True):
    """
    determines contact normal orientation between two particles
    uses the random walker implementation from skimage

    Parameters
    ----------
        volBin : 3D array
            binary volume containing two particles in contact

        volLab : 3D array of integers
            labelled volume containing two particles in contact

        watershed : string
            sets the basis for the determination of the orientation
            options are "ITK" for the labelled image from the input,
            "RW" for a further segmentation by the random walker
            default is "ITK"

        markerShrink : boolean
            shrinks the markers to contain only one voxel (Default = True)
            for large markers, the segmentation might yield strange results depending on the shape

    Returns
    -------
        contactNormal : 1x3 array
            contact normal orientation in z,y,x coordinates
            the vector is flipped such that the z coordinate is positive

        len(coordIntervox) : integer
            the number of points for the principal component analysis
            indicates the quality of the fit

        notTreatedContact : boolean
            if False that contact is not determined
            if the contact consisted of too few voxels a fit is not possible or feasible
    """
    notTreatedContact = False
    from skimage.segmentation import random_walker

    if watershed == "ITK":
        # ------------------------------
        # ITK watershed for orientations
        # ------------------------------
        # need to relabel, because the _contactPairs functions looks for 1 and 2
        labels = numpy.unique(volLab)
        volLab[ volLab==labels[1] ] = 1
        volLab[ volLab==labels[2] ] = 2

        contactITK = _contactPairs(volLab)

        if len(contactITK) <=2:
            #print('WARNING: not enough contacting voxels (beucher)... aborting this calculation')
            notTreatedContact = True
            return numpy.zeros((3)), 0, notTreatedContact

        coordIntervox = contactITK[:,0:3]
        # Determining the contact orientation! using PCA
        contactNormal = _contactNormals(coordIntervox)

    if watershed == "RW":
        # random walker for orientations
        distanceMap = scipy.ndimage.morphology.distance_transform_edt(volBin)
        localMaxi = peak_local_max(distanceMap, min_distance=5, indices=False, exclude_border=True, labels=volBin, num_peaks=2)

        # Set markers for the watershed algorithm (= local maxima of the EDM)
        #   define structure for the labelling algorithm in order to find connected voxels
        #   sometimes local maxima are flat and touch only diagonal of slices
        struc = numpy.ones((3,3,3))
        markers, numMarkers = scipy.ndimage.measurements.label(localMaxi,structure=struc)

        if numMarkers != 2:
            markers = _markerCorrection(markers,numMarkers,distanceMap,volBin)
            #print("sum of markers",markers.sum(), numpy.unique(markers))
            # check if we finally have only two markers -- 1 and 2
            # unique == 3 because it counts 0
            if numpy.unique(markers).size != 3:
                notTreatedContact = True
                return numpy.zeros((3)), 0, notTreatedContact

        if markerShrink:
            centerOfMass = scipy.ndimage.measurements.center_of_mass(markers,labels=markers,index=[1,2])

            newMarkers = numpy.zeros(numpy.shape(markers))
            newMarkers[int(centerOfMass[0][0]),int(centerOfMass[0][1]),int(centerOfMass[0][2])] = 1
            newMarkers[int(centerOfMass[1][0]),int(centerOfMass[1][1]),int(centerOfMass[1][2])] = 2
            markers = newMarkers

        volRWbin = volBin.astype(float)

        # set the void phase of the binary image to -1, excludes this phase from calculation of the random walker (saves time)
        markers[~volRWbin.astype(bool)] = -1

        probMaps = random_walker(volRWbin, markers, beta=80, mode='cg_mg', return_full_prob=True)

        # reset probability of voxels in the void region to 0! (-1 right now, as they were not taken into account!)
        probMaps[:,~volRWbin.astype(bool)] = 0

        # create a map of the probabilities of belonging to either label 1 oder label 2 (which is just the inverse map)
        labRW1 = probMaps[0].astype(numpy.float32)

        # label the image depending on the probabilty of each voxel belonging to marker = 1, save one power watershed
        labRW = numpy.array(labRW1)
        labRW[labRW > 0.5] = 1
        labRW[(labRW < 0.5) & (labRW > 0)] = 2
        # seed of the second marker has to be labelled by 2 as well
        labRW[markers == 2] = 2

        contactVox = _contactPairs(labRW)
        if len(contactVox) <=2:
            #print 'WARNING: not enough contacting voxels (rw).... aborting this calculation'
            notTreatedContact = True
            return numpy.zeros((3)), 0, notTreatedContact

        # get subvoxel precision - using the probability values at the contacting voxels!
        coordIntervox = _contactPositions(contactVox,labRW1)
        # Determining the contact orientation! using PCA
        contactNormal = _contactNormals(coordIntervox)

    return contactNormal[0], len(coordIntervox), notTreatedContact


def _contactPairs(lab):
    """
    finds the voxels involved in the contact
    i.e. the voxels of one label in direct contact with another label

    Parameters
    ----------
        lab : 3D array of integers
            labelled volume containing two particles in contact
            labels of the considered particles are 1 and 2

    Returns
    -------
        contact : (len(contactVoxels))x4 array
            z,y,x positions and the label of the voxel
    """
    dimensions = numpy.shape(lab)
    dimZ, dimY, dimX = dimensions[0], dimensions[1], dimensions[2]

    # position of the voxels labelled by 1 ... row 1 = coord index 1, row 2 = coord 2, ...
    positionLabel = numpy.array(numpy.where(lab==1))
    # initialize the array for the contact positions and labels!
    contact=numpy.array([[],[],[],[]]).transpose()

    # loop over all voxels labeled with 1
    for x in range (0,len(positionLabel.transpose())):
        pix=numpy.array([positionLabel[0][x],positionLabel[1][x],positionLabel[2][x],1])
        # pix ... positions (axis 0,1,2) of the first voxel containing 1
        ## x axis neighbor
        if positionLabel[0][x]<dimZ-1: # if the voxel is still in the image!
        #if neighbor in pos. x-direction is 2 then save the actual voxel and the neighbor!!
            if lab[positionLabel[0][x]+1,positionLabel[1][x],positionLabel[2][x]]==2:
                vx1=numpy.array([positionLabel[0][x]+1,positionLabel[1][x],positionLabel[2][x],2])
                # stacks the data, adds a row to the data, so you get (contact, pix, vx2)
                contact=numpy.vstack((contact,pix))
                contact=numpy.vstack((contact,vx1))
        # this condition prevents from getting stuck at the border of the image, where the x-value cannot be reduced!
        if positionLabel[0][x]!=0:
            #if neighbor in neg. x-direction is 2 then save the actual voxel and the neighbor!!
            if lab[positionLabel[0][x]-1,positionLabel[1][x],positionLabel[2][x]]==2:
                vx2=numpy.array([positionLabel[0][x]-1,positionLabel[1][x],positionLabel[2][x],2])
                contact=numpy.vstack((contact,pix))
                contact=numpy.vstack((contact,vx2))
        ## y axis neighbor
        if positionLabel[1][x]<dimY-1:
            if lab[positionLabel[0][x],positionLabel[1][x]+1,positionLabel[2][x]]==2:
                vy1=numpy.array([positionLabel[0][x],positionLabel[1][x]+1,positionLabel[2][x],2])
                contact=numpy.vstack((contact,pix))
                contact=numpy.vstack((contact,vy1))
        if positionLabel[1][x]!=0:
            if lab[positionLabel[0][x],positionLabel[1][x]-1,positionLabel[2][x]]==2:
                vy2=numpy.array([positionLabel[0][x],positionLabel[1][x]-1,positionLabel[2][x],2])
                contact=numpy.vstack((contact,pix))
                contact=numpy.vstack((contact,vy2))
        ## z axis neighbor
        if positionLabel[2][x]<dimX-1:
            if lab[positionLabel[0][x],positionLabel[1][x],positionLabel[2][x]+1]==2:
                vz1=numpy.array([positionLabel[0][x],positionLabel[1][x],positionLabel[2][x]+1,2])
                contact=numpy.vstack((contact,pix))
                contact=numpy.vstack((contact,vz1))
        if positionLabel[2][x]!=0:
            if lab[positionLabel[0][x],positionLabel[1][x],positionLabel[2][x]-1]==2:
                vz2=numpy.array([positionLabel[0][x],positionLabel[1][x],positionLabel[2][x]-1,2])
                contact=numpy.vstack((contact,pix))
                contact=numpy.vstack((contact,vz2))

    return contact


def _contactPositions(contact,probMap):
    """
    determines the position of the points that define the contact area
    for the random walker probability map
    the 50 percent probability plane is considered as the area of contact
    linear interpolation is used to determine the 50 percent probability area

    Parameters
    ----------
        contact : (len(contactVoxels))x4 array
            z,y,x positions and the label of the voxel
            as returned by the function contactPairs()

        probMap : 3D array of floats
            probability map of one of the labels
            as determined by the random walker

    Returns
    -------
        coordIntervox : (len(coordIntervox))x3 array
            z,y,x positions of the 50 percent probability area
    """
    coordIntervox = numpy.array([[],[],[]]).transpose()
    for x in range (0,len(contact),2): #call only contact pairs (increment 2)
        prob1 = probMap[int(contact[x][0]),int(contact[x][1]),int(contact[x][2])]
        #pick the probability value of the concerning contact voxel!
        prob2 = probMap[int(contact[x+1][0]),int(contact[x+1][1]),int(contact[x+1][2])]
        if prob2-prob1 != 0:
            add = float((0.5-prob1)/(prob2-prob1))
        else:
            add=0.5 #if both voxels have the same probability (0.5), the center is just in between them!
        #  check whether the next contact voxel is x-axis (0) neighbor or not
        ## x axis neighbor
        if contact[x][0]!=contact[x+1][0]:
            ## 2 possibilities: a coordinates > or < b coordinates
            if contact[x][0]<contact[x+1][0]: # find the contact point in subvoxel resolution!
                midX=numpy.array([contact[x][0]+add,contact[x][1],contact[x][2]])
                coordIntervox=numpy.vstack((coordIntervox,midX))
            else:
                midX=numpy.array([contact[x][0]-add,contact[x][1],contact[x][2]])
                coordIntervox=numpy.vstack((coordIntervox,midX))
        ## y axis neighbor
        elif contact[x][1]!=contact[x+1][1]:
            if contact[x][1]<contact[x+1][1]:
                midY=numpy.array([contact[x][0],contact[x][1]+add,contact[x][2]])
                coordIntervox=numpy.vstack((coordIntervox,midY))
            else:
                midY=numpy.array([contact[x][0],contact[x][1]-add,contact[x][2]])
                coordIntervox=numpy.vstack((coordIntervox,midY))
        ## z axis neighbor
        else:
            if contact[x][2]<contact[x+1][2]:
                midZ=numpy.array([contact[x][0],contact[x][1],contact[x][2]+add])
                coordIntervox=numpy.vstack((coordIntervox,midZ))
            else:
                midZ=numpy.array([contact[x][0],contact[x][1],contact[x][2]-add])
                coordIntervox=numpy.vstack((coordIntervox,midZ))

    return coordIntervox


def _contactNormals(dataSet):
    """
    determines the contact normal orientation
    based on the intervoxel positions determined by the function contactPositions()
    uses a principal component analysis
    the smallest eigenvector of the covariance matrix is considered as the contact orientation

    Parameters
    ----------
        dataSet : (len(dataSet))x3 array
            z,y,x positions of the 50 percent probability area of the random walker

    Returns
    -------
        contactNormal : 1x3 array
            z,y,x directions of the normalised contact normal orientation
    """
    covariance = numpy.cov(dataSet,rowvar=0,bias=0)

    # step 3: calculate the eigenvectors and eigenvalues
    # eigenvalues are not necessarily ordered ...
    # colum[:,i] corresponds to eig[i]
    eigVal, eigVec = numpy.linalg.eig(covariance)

    # look for the eigenvector corresponding to the minimal eigenvalue!
    minEV = eigVec[:,numpy.argmin(eigVal)]

    # vector orientation
    contactNormal = numpy.zeros((1,3))
    if minEV[2]<0:
        contactNormal[0,0], contactNormal[0,1], contactNormal[0,2] = -minEV[0], -minEV[1], -minEV[2]
    else:
        contactNormal[0,0], contactNormal[0,1], contactNormal[0,2] = minEV[0], minEV[1], minEV[2]

    return contactNormal


def _markerCorrection(markers,numMarkers,distanceMap,volBin,peakDistance=15,struc=numpy.ones((3,3,3))):
    """
    corrects the number of markers used for the random walker segmentation of two particles
    if too many markers are found, the markers with the largest distance are considered
    if too few markers are found, the minimum distance between parameters is reduced

    Parameters
    ----------
        markers : 3-D array of integers
            volume containing the potential markers for the random walker
            
        numMarkers : integer
            number of markers found so far

        distanceMap : 3-D array of floats
            euclidean distance map

        volBin : 3-D array of integers
            binary volume

        peakDistance : integer
            peak distance as used in skimage.feature.peak_local_max
            Default value is 15 px

        struc=numpy.ones((3,3,3)) : 3x3x3 array of integers
            structuring element for the labelling of the markers
            Default element is a 3x3x3 array of ones

    Returns
    -------
        markers : 3-D array of integers
            volume containing the markers
    """
    counter = 0    
    while (numpy.any(markers)==False or numpy.amax(markers) < 2):
        if (counter > 10 ):
            markers=numpy.zeros(markers.shape)
            return markers
        peakDistance = int(peakDistance/1.3)
        localMaxi = peak_local_max(distanceMap, min_distance=peakDistance, indices=False, exclude_border = False, labels=volBin, num_peaks=2)
        markers, numMarkers = scipy.ndimage.measurements.label(localMaxi,structure=struc)
        counter = counter + 1
        
    if (numpy.amax(markers) > 2):
        centerOfMass = scipy.ndimage.measurements.center_of_mass(markers,labels=markers,index=range(1,numMarkers+1))
        distances = numpy.zeros((numMarkers,numMarkers))
        for i in range(0,numMarkers):
            for j in range(0,numMarkers):
                distances[i,j] = numpy.linalg.norm(numpy.array(centerOfMass[i])-numpy.array(centerOfMass[j]) )

        maxDistance = numpy.amax(distances)
        posMaxDistance = numpy.where(distances == maxDistance )

        # let's choose the markers with the maximum distance
        markers1 = numpy.where( markers == posMaxDistance[0][0]+1, 1, 0 )
        markers2 = numpy.where( markers == posMaxDistance[1][0]+1, 2, 0 )

        localMaxi = markers1 + markers2
        markers, numMarkers = scipy.ndimage.measurements.label(localMaxi,structure=struc)

    return markers


def localDetectionAssembly(volLab,volGrey,contactList,localThreshold,boundingBoxes=None,NumberOfThreads=1,radiusThresh=4):
    """
    local contact refinement of a set of contacts
    checks whether two particles are in contact with a local threshold using ``localDetection()``

    Parameters
    ----------
        volLab : 3D array
            Labelled volume

        volGrey : 3D array
            Grey-scale volume

        contactList : (ContactNumber)x2 array of integers
            contact list with grain labels of each contact in a seperate row,
            as given by ``spam.label.contacts.labelledContacts`` in the list contactingLabels

        localThreshold : integer or float, same type as the 3D array
            threshold for binarisation of the subvolume

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        NumberOfThreads : integer
            Number of Threads for multiprocessing

        radiusThresh : integer, optional
            radius for excluding patches that might not be relevant,
            e.g. noise can lead to patches that are not connected with the grains in contact
            the patches are calculated with ``equivalentRadii()``
            Default is 4

    Returns
    -------
        contactListRefined : (ContactNumber)x2 array of integers
            refined contact list, based on the chosen local threshold

    Note
    ----
        see https://doi.org/10.1088/1361-6501/aa8dbf for further information
    """
    # check if bounding boxes are given
    if boundingBoxes is None:
        #print "bounding boxes are not given. calculating ...."
        boundingBoxes = spam.label.boundingBoxes(volLab)

    contactListRefined = []
    numberOfJobs = len( contactList )
    print ("\n\tLocal contact refinement")
    print ("\tApplying a local threshold of ", localThreshold, " to each contact.")
    print ("\tNumber of contacts for treatment ", numberOfJobs)
    print ("")

    ##########################################

    def worker( workerNumber, qJobs, qResults ):
        while True:
            job = qJobs.get()

            if job == "STOP":
                qResults.put("STOP")
                break
            else:
                print ("\tWorking on job #", job , " of " , numberOfJobs)


            grainA, grainB = contactList[job].astype('int')
            labels = [grainA, grainB]

            subVolLab, subVolBin, subVolGrey = fetchTwoGrains(volLab,volGrey,labels,boundingBoxes)

            contact = localDetection(subVolGrey,localThreshold,radiusThresh)
            if contact == True:
                #print ("we are in contact!")
                qResults.put( [ workerNumber, job, grainA, grainB ] )

    ##########################################

    startTime = time.time()

    #print ("Master: Setting up queues")
    qJobs    = multiprocessing.Queue()
    qResults = multiprocessing.Queue()

    #print ("Master: Adding jobs to queues")
    for x in range(numberOfJobs):
        qJobs.put( x )

    for i in range( NumberOfThreads ):
        qJobs.put( "STOP" )


    #print ("Master: Launching workers")
    for i in range(NumberOfThreads):
        p = multiprocessing.Process( target=worker, args=( i, qJobs, qResults, ) )
        p.start()

    finishedThreads  = 0

    #print ("Master: Waiting for results")
    while finishedThreads < NumberOfThreads:
        result = qResults.get()

        if result == "STOP":
            finishedThreads += 1
            print ("\tNumber of finished threads = ", finishedThreads)

        else:
            contactListRefined.append( [ result[2], result[3] ] )

    timeTotal = time.time() - startTime
    print ("\tFinished after ... ", timeTotal, " s")

    return numpy.asarray(contactListRefined)


def contactOrientationsAssembly(volLab,volGrey,contactList,watershed="ITK",boundingBoxes=None,NumberOfThreads=1):
    """
    determines contact normal orientation in an assembly of touching particles
    uses either directly the labelled image or the random walker implementation from skimage

    Parameters
    ----------
        volLab : 3D array
            Labelled volume

        volGrey : 3D array
            Grey-scale volume

        contactList : (ContactNumber)x2 array of integers
            contact list with grain labels of each contact in a seperate row,
            as given by ``spam.label.contacts.labelledContacts`` in the list contactingLabels
            or by ``spam.label.contacts.localDetectionAssembly()``

        watershed : string
            sets the basis for the determination of the orientation
            options are "ITK" for the labelled image from the input,
            "RW" for a further segmentation by the random walker
            default is "ITK"

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        NumberOfThreads : integer
            Number of Threads for multiprocessing

    Returns
    -------
        contactOrientations : (numContacts)x6 array
            contact normal orientation for every contact
            [labelGrainA, labelGrainB, orientationZ, orientationY, orientationX, intervoxel positions for PCA]

        notTreatedContact : boolean
            if False that contact is not determined
            if the contact consisted of too few voxels a fit is not possible or feasible
    """
    # check if bounding boxes are given
    if boundingBoxes is None:
        #print "bounding boxes are not given. calculating ...."
        boundingBoxes = spam.label.boundingBoxes(volLab)

    contactOrientations = []
    numberOfJobs = len( contactList )
    print ("\n\tDetermining the contact orientations of an assembly of particles")
    print ("\tNumber of contacts ", numberOfJobs)
    print ("")

    ##########################################

    def worker( workerNumber, qJobs, qResults ):
        while True:
            job = qJobs.get()

            if job == "STOP":
                qResults.put("STOP")
                break
            else:
                print ("\tWorking on job #", job , " of " , numberOfJobs)

            grainA, grainB = contactList[job,0:2].astype('int')
            labels = [grainA, grainB]

            subVolLab, subVolBin, subVolGrey = fetchTwoGrains(volLab,volGrey,labels,boundingBoxes)

            contactNormal, intervox, NotTreatedContact = spam.label.contactOrientations(subVolBin,subVolLab,watershed)
            #TODO work on not treated contacts -- output them!

            qResults.put( [ workerNumber, job+1, grainA, grainB, contactNormal[0], contactNormal[1], contactNormal[2], intervox ] )

    ##########################################

    startTime = time.time()

    #print "Master: Setting up queues"
    qJobs    = multiprocessing.Queue()
    qResults = multiprocessing.Queue()

    #print "Master: Adding jobs to queues"
    for x in range(numberOfJobs):
        #qJobs.put( contactList[x,0] )
        qJobs.put( x )

    for i in range( NumberOfThreads ):
        qJobs.put( "STOP" )

    #print "Master: Launching workers"
    for i in range(NumberOfThreads):
        p = multiprocessing.Process( target=worker, args=( i, qJobs, qResults, ) )
        p.start()

    finishedThreads  = 0
    #print "Master: Waiting for results"
    while finishedThreads < NumberOfThreads:
        result = qResults.get()

        if result == "STOP":
            finishedThreads += 1
            print ("\tNumber of finished threads = ", finishedThreads)

        else:
            #print "Master: got {}".format( result )
            contactOrientations.append( [ result[2], result[3], result[4], result[5], result[6], result[7] ] )

    timeTotal = time.time() - startTime
    print ("\tfinished after ... ", timeTotal, " s")

    return numpy.asarray(contactOrientations)
