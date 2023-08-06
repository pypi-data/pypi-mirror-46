"""This module offers a set of tools in order create non adapted meshes..

The three principal steps in order to create a non adapted mesh are here:

    1. create the non structured mesh
    2. create a distance field of the morphology on a structured mesh
    3. project the morphology (with the distance field) onto the structured mesh


Step 1. can be handled with ``spam.mesh.unstructured`` where this modules handle the projection
and the creation of the distance field either from:

    1. a packing of ideal objects (spheres)
    2. or a segmented 3D image

"""


def packSpheres(totalVolumeFraction, rejectionLength, phases,
                origin=[0, 0, 0], lengths=[1, 1, 1], nCells=[100, 100, 100],
                inside=True,
                fieldName="spam", domainType="cube",
                vtkSpheres=False, vtkField=False):
    """This function packs one or several sets (phase) of spheres of deferent radii
    and create the corresponding distance fields (one per set).

    The packing algorithm is an iterative process based collective rearrangement.

    Parameters
    ----------
        totalVolumeFraction: float
            The total volume fraction of all the phases
        rejectionLength: float
            The minimal distance between two spheres surfaces
        phases: array
            A 2D array containing the phases parameteres.
            A row corresponds to a phase and a column to a parameter:

                * column 0: the minimal ray of the spheres of the phase
                * column 1: the maximal ray of the spheres of the phase
                * column 2: the relative volume fraction of the phase

            Its shape is: number of phases by 3.
        inside: bool, default=True
            Defines whether or not the spheres have to be completly inside the domain or if they can intersect it.
            The centres remain always inside the domain.
        lengths: array, default=[1,1,1]
            The size of the domain the spheres are packed into.
            The axis order is `zyx`.
        origin: array, default=[0,0,0]
            The origin of the domain.
            The axis order is `zyx`.
        domainType: string, default='cube'
            The domain type the spheres are packed into.
            Options are:

                * ``cube``: which corresponds to a cuboid. ``lengths`` is then the length of the cuboids.
                * ``cylinder``: which corresponds to a cylinder which height is in the `z` axis.

        fieldName: string, default='spam'
            The name of the distance field.
            It is used when saving the files.

        nCells: array, default=[100,100,100]
            The number of cells of the structured mesh used to discretise the distance field.
            The axis order is `zyx`.
        vtkSpheres: bool, default=False
            Save vtk files of the spheres for each iterations.
        vtkField: bool, default=False
            Save vtk files of the distance field at the end.

    Returns
    -------
        void:
            It writes a text file ``.dat`` with the flattened (in the lexicographical order) distance field.
            Its format is

            .. code-block:: text

                lengthX, lengthY, lengthZ
                originX, originY, originZ
                nCellsX, nCellY, nCellZ
                fieldValue0
                fieldValue1
                fieldValue2
                ...

            This text format is the input of the projection function.


    Example
    -------
        >>> phases = [ [0.5, 1.5, 0.4],
                       [1.5, 4,   0.6] ]
        Correspond to 2 phases.
        phase 1: with radii from 0.5 to 1.5 corresponding to 40% of the total volume fraction
        phase 2: with radii from 1.5 to 4.0 corresponding to 60% of the total volume fraction
        >>> projection.packSpheres( 0.4, 0.1, phases, lengths=[15.0,50.0,20.0], nCells=[30,100,40] )
        Yields a 40% total volume fraction with rejection lenght of 0.1
        in a cuboid of size z=15, y=50, x=20
        with a discretisation of the distance field of 30, 100 and 40 cells respectively.

    WARNING
    -------
        This function deals with structured mesh thus ``x`` and ``z`` axis are swapped **in python**.

    """
    import numpy
    import spam.mesh.meshToolkit as mtk

    # condition inputs for crPacking c++ constructor
    param = [totalVolumeFraction, rejectionLength]
    phases = numpy.array(phases)
    if len(phases.shape) == 1:
        for j in range(3):
            param.append(phases[j])
        param.append(1)
    else:
        for i in range(phases.shape[0]):
            for j in range(3):
                param.append(phases[i][j])
            param.append(i+1)

    # swith axis
    lengths = [_ for _ in reversed(lengths)]
    origin = [_ for _ in reversed(origin)]
    nCells = [_ for _ in reversed(nCells)]

    # call c++ client in meshToolkit
    mtk.pack_and_field(param, lengths, origin, nCells, inside, vtkSpheres, vtkField, fieldName, domainType)


def packSpheresFromList(objects,
                        rejectionLength,
                        origin=[0, 0, 0], lengths=[1, 1, 1], nCells=[100, 100, 100],
                        inside=True,
                        fieldName="spam", domainType="cube",
                        vtkSpheres=False, vtkField=False):
    """This function packs a set of spheres predefine spheres and create the corresponding distance fields (one per set).
    The predefined position are taken as initial condition to the packing algorithm.

    The packing algorithm is an iterative process based collective rearrangement.

    Parameters
    ----------
        objects: nSpheres times 5 float array
            The list of objects. Rows correspond to a sphere and the 5 columns correspond to (z, y, x) position of the centre, radius and phase number.
        rejectionLength: float
            The minimal distance between two spheres surfaces
        inside: bool, default=True
            Defines whether or not the spheres have to be completly inside the domain or if they can intersect it.
            The centres remain always inside the domain.
        lengths: array, default=[1,1,1]
            The size of the domain the spheres are packed into.
            The axis order is `zyx`.
        origin: array, default=[0,0,0]
            The origin of the domain.
            The axis order is `zyx`.
        domainType: string, default='cube'
            The domain type the spheres are packed into.
            Options are:

                * ``cube``: which corresponds to a cuboid. ``lengths`` is then the length of the cuboids.
                * ``cylinder``: which corresponds to a cylinder which height is in the `z` axis.

        fieldName: string, default='spam'
            The name of the distance field.
            It is used when saving the files.

        nCells: array, default=[100,100,100]
            The number of cells of the structured mesh used to discretise the distance field.
            The axis order is `zyx`.
        vtkSpheres: bool, default=False
            Save vtk files of the spheres for each iterations.
        vtkField: bool, default=False
            Save vtk files of the distance field at the end.

    Returns
    -------
        void:
            It writes a text file ``.dat`` with the flattened (in the lexicographical order) distance field.
            Its format is

            .. code-block:: text

                lengthX, lengthY, lengthZ
                originX, originY, originZ
                nCellsX, nCellY, nCellZ
                fieldValue0
                fieldValue1
                fieldValue2
                ...

            This text format is the input of the projection function.


    WARNING
    -------
        This function deals with structured mesh thus ``x`` and ``z`` axis are swapped **in python**.

    """
    import numpy
    import spam.mesh.meshToolkit as mtk

    # condition inputs for crPacking c++ constructor
    param = [0.0, rejectionLength, 1.0, 1.0, 1.0, 1.0]

    # swith axis
    lengths = [_ for _ in reversed(lengths)]
    origin = [_ for _ in reversed(origin)]
    nCells = [_ for _ in reversed(nCells)]

    # deal with objects
    objects = numpy.array(objects)

    if objects.shape[1] == 5:
        # swap axis spheres
        tmp = objects[:, 0].copy()
        objects[:, 0] = objects[:, 2]
        objects[:, 2] = tmp
        # permutation to put radius first (thanks crpacking!)
        radii = objects[:, 3].copy()
        objects[:, 1:4] = objects[:, 0:3]
        objects[:, 0] = radii
    elif objects.shape[1] == 7:
        # swap axis ellipsoids
        tmp = objects[:, 0].copy()
        objects[:, 0] = objects[:, 2]
        objects[:, 2] = tmp
        tmp = objects[:, 3].copy()
        objects[:, 3] = objects[:, 5]
        objects[:, 5] = tmp

    # create phasesValues
    phasesValues = numpy.unique(objects[:, -1]).astype('<u8').tolist()

    # call c++ client in meshToolkit
    mtk.create_pack_and_field(objects, phasesValues, param, lengths, origin, nCells, inside, vtkSpheres, vtkField, fieldName, domainType)


def distanceFieldFromObjects(objects, origin=[0, 0, 0], lengths=[1, 1, 1], nCells=[100, 100, 100],
                             fieldName="spam", vtkField=False):
    """This function reads a list of objects and creates the corresponding distance field.

    Parameters
    ----------
        objects: array
            The list of objects. Each line corresponds to an object and each column to a property.
            The objects available are:

                        * spheres, with 4 columns: centreZ, centreY, centreX, radius, phaseValue
                        * ellipsoids, with 6 columns: centreZ, centreY, centreX, radiusZ, radiusY, radiusX, phaseValue

        lengths: array, default=[1,1,1]
            The size of the domain the objects are packed into (needed to create the distance field).
            The axis order is `zyx`.
        origin: array, default=[0,0,0]
            The origin of the domain (needed to create the distance field).
            The axis order is `zyx`.
        nCells: array, default=[100,100,100]
            The number of cells of the structured mesh used to discretise the distance field.
            The axis order is `zyx`.
        fieldName: string, default='spam'
            The name of the distance field.
            It is used when saving the files.
        vtkField: bool, default=False
            Save vtk files of the distance field at the end.

    Returns
    -------
        void:
            It writes a text file ``.dat`` with the flattened (in the lexicographical order) distance field.
            Its format is

            .. code-block:: text

                lengthX, lengthY, lengthZ
                originX, originY, originZ
                nCellsX, nCellY, nCellZ
                fieldValue0
                fieldValue1
                fieldValue2
                ...

            This text format is the input of the projection function.

    WARNING
    -------
        This function deals with structured mesh thus ``x`` and ``z`` axis are swapped **in python**.

    """
    import numpy
    import spam.mesh.meshToolkit as mtk

    # swith axis
    lengths = [_ for _ in reversed(lengths)]
    origin = [_ for _ in reversed(origin)]
    nCells = [_ for _ in reversed(nCells)]

    objects = numpy.array(objects)

    if objects.shape[1] == 5:
        # swap axis spheres
        tmp = objects[:, 0].copy()
        objects[:, 0] = objects[:, 2]
        objects[:, 2] = tmp
        # permutation to put radius first (thanks crpacking!)
        radii = objects[:, 3].copy()
        objects[:, 1:4] = objects[:, 0:3]
        objects[:, 0] = radii
    elif objects.shape[1] == 7:
        # swap axis ellipsoids
        tmp = objects[:, 0].copy()
        objects[:, 0] = objects[:, 2]
        objects[:, 2] = tmp
        tmp = objects[:, 3].copy()
        objects[:, 3] = objects[:, 5]
        objects[:, 5] = tmp

    # create phasesValues
    phasesValues = numpy.unique(objects[:, -1]).astype('<u8').tolist()
    #phasesValues = [_ for _ in phasesValues]

    # call c++ client in meshToolkit
    mtk.objects_to_field(objects, phasesValues, lengths, origin, nCells, vtkField, fieldName)


def distanceField(phases, phaseID=1):
    """
    This function tranforms an array/image of integers into a continuous field.
    It works for segmented binary/trinary 3D images or arrays of integers.
    It has to be run for each phase seperately.

    It uses of the **Distance Transform Algorithm**.
    For every voxel belonging to a phase a value indicating the distance
    (in voxels) of that point to the nearest background point is computed.
    The DTA is computed for the inverted image as well and the computed distances
    are setting to negative values.
    The 2 distance fields are merged into the final continuuos distance field where:

        * positive numbers: distances from the phase to the nearest background voxel
        * negative values: distances from the background to the nearest phase voxel
        * zero values: the interface between the considered phase and the background

    Parameters
    -----------
        phases : array
            The input image/array (each phase should be represented with only one number)
        phaseID : int, default=1
            The integer indicating the phase which distance field you want to calculate

    Returns
    --------
        distance field of the phase: array

    Example
    --------
        >>> import tifffile
        >>> im = tifffile.imread( "mySegmentedImage.tif" )
        In this image the inclusions are labelled 1 and the matrix 0
        >>> di = projection.distanceField( im, phase=1 )
        The resulting distance field is made of float between -1 and 1

    """
    import numpy
    from scipy import ndimage

    # create binary image from phases and phaseID
    binary = numpy.zeros_like(phases, dtype=numpy.bool)
    binary[phases == phaseID] = True

    # Create the complementary binary image
    binaryNot = numpy.logical_not(binary)

    # Step 4: Calculate the distance algorithm for the 2 binary images

    binaryDist = ndimage.morphology.distance_transform_edt(binary).astype('<f4')
    binaryNotDist = ndimage.morphology.distance_transform_edt(binaryNot).astype('<f4')

    # normalise if needed

    # if normalise:
    #     binaryDist = binaryDist / binaryDist.max()

    # if normalise:
    #     binaryNotDist = binaryNotDist.astype(numpy.float32)
    #     binaryNotDist = binaryNotDist / binaryNotDist.max()

    # Step 5: Merge the 2 distance fields into the final one
    binaryNotDist = (-1.0)*binaryNotDist
    binaryNotDist = binaryNotDist + binaryDist

    return binaryNotDist


def saveFieldFile(im, lengths=[1.0, 1.0, 1.0], origin=[0, 0, 0], fileName='spam.dat'):
    """
    This function creates the input file (field file) for Projmorpho
    based on a tifffile (image) or an array

    The file structure is:

    .. code-block:: bash

        row 1: field length vector:   lx, ly, lz
        row 2: field origin vector:    x,  y,  z
        row 3: shape of the field3nd: nx, ny, nz) which are (im.shape[2], im.shape[1], im.shape[0])
        row 4: field value

        ...    field values organised in lexicographical order.

        row n: field value

    Parameters
    -----------
        im: array
            The input image/array field
        lengths: array, default=[1,1,1]
            The physical dimensions of the field (*e.g.*, in mm).
            Its length has to be 3 representing direction z, y, and x.
        origin: array, default=[0,0,0]
            The origin of the field.
            Its length has to be 3 representing direction z, y, and x.
        fileName : string, default='spam.vtk'
            Name of the output file.

    """
    with open(fileName, 'w') as f:
        f.write('{}, {}, {}\n'.format(*reversed(lengths)))
        f.write('{}, {}, {}\n'.format(*reversed(origin)))
        f.write('{}, {}, {}\n'.format(*reversed(im.shape)))
        for v in im.reshape(-1):
            f.write('{}\n'.format(v))
    f.close()


def projectField(meshFile, fieldFiles, thresholds=[0.0], outputFile='Ispam', nSkip=1, vtkMesh=False):
    """This function project a set distance fields onto an unstructured mesh.

    Each distance fields corresponds to a phase and the interface between
    the two phases is set by the thresholds.

    Parameters
    ----------
        meshFile: string
            Path to the file that contains the unstructured mesh.
            It currently takes ``gmsh`` format files.
        fieldFiles: array of string
            Array of pathes to the distance fields files.
        thresholds: array of floats
            The list of thresholds.
        outputFile: string, default='Ispam'
            The name used to save the outputs
        nSkip: int, default=1
            In the gmsh file, number of number to ignore between the
            element type (second number, 4 for tetrahedrons) and the connectivity.
        vtkMesh: bool, default=False
            Save vtk file of the mesh.

    Returns
    -------
        void:
            It writes a text file called ``outputFile`` the list of node and the list of elements
            which format is:

            .. code-block:: text

                COORdinates ! number of nodes
                nodeId, 0, x, y, z
                ...

                ELEMents ! number of elemens
                elemId, 0, elemType, n1, n2, n3, n4, subVol, interX, interY, interZ
                ...

            where:

                * ``n1, n2, n3, n4`` is the connectivity
                * ``subVol`` is the sub volume of the terahedron inside the inclusion
                * ``interX, interY, interZ`` are to componants of the interface vector
                * ``elemType`` is the type of element. Their meaning depends on the thresholds and the number of phase. Correspondance can be found in the function output after the key word **MATE** like:

                .. code-block:: text

                    <projmorpho::set_materials
                    .        field 1
                    .        .       MATE,1: background
                    .        .       MATE,2: phase 1
                    .        .       MATE,3: interface phase 1 with background
                    .        field 2
                    .        .       MATE,1: background
                    .        .       MATE,4: phase 2
                    .        .       MATE,5: interface phase 2 with background
                    >

            Sub volumes and interface vector are only relevant for interfaces.

    """
    # call c++ client function in meshToolkit
    import spam.mesh.meshToolkit as mtk

    if type(fieldFiles) is str:
        fieldFiles = [fieldFiles]

    mtk.project_fields(meshFile, outputFile, thresholds, fieldFiles, nSkip, int(vtkMesh))
