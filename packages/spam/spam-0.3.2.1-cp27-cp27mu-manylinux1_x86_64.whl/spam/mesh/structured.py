"""
This module offers a set of tools in order to manipulate structured meshes.

>>> # import module
>>> import spam.mesh
>>> spam.mesh.computeStrainField()


The strucutred VTK files used to save the data have the form:

.. code-block:: text

    # vtk DataFile Version 2.0
    VTK file from spam: spam.vtk
    ASCII

    DATASET STRUCTURED_POINTS
    DIMENSIONS nx ny nz
    ASPECT_RATIO lx ly lz
    ORIGIN ox oy oz

    POINT_DATA nx x ny x nz

    SCALARS myNodalField1 float
    LOOKUP_TABLE default
        nodalValue_1
        nodalValue_2
        nodalValue_3
        ...

    VECTORS myNodalField2 float
    LOOKUP_TABLE default
        nodalValue_1_X nodalValue_1_Y nodalValue_1_Z
        nodalValue_2_X nodalValue_2_Y nodalValue_2_Z
        nodalValue_3_X nodalValue_3_Y nodalValue_3_Z
        ...

    CELL_DATA (nx-1) x (ny-1) x (nz-1)

    SCALARS myCellField1 float
    LOOKUP_TABLE default
        cellValue_1
        cellValue_2
        cellValue_3
        ...

where nx, ny and nz are the number of nodes in each axis, lx, ly, lz, the mesh length in each axis and ox, oy, oz the spatial postiion of the origin.

"""

from __future__ import print_function

def computeStrainField(displacementField, nodeSpacing=[1.0, 1.0, 1.0], largeStrains=True, onlyStrain=True):
    """
    This function computes the strain field from a given displacement field

    The strain is computed in the centre of a 8-node cell using order one (linear) shape functions.

    Parameters
    ----------
        displacementField: array float
            The vector field to compute the derivatives.
            Its shape is (nz, ny, nx, 3).

        nodeSpacing: array float
            Length between two nodes in every direction (*i.e.,* size of a cell)
            Default = [1.0, 1.0, 1.0]

        largeStrains: bool, optional
            if True, the strain field is computed under the hypothesis of large strains
            if False, the strain field is computed under the hypothesis of small strains
            (*i.e.,* the strain tensor is symmetric and the volumetic strain is the trace)
            Default = True

        onlyStrain: bool, optional
            if True, only the strain fields are returned
            if False, the fields of the gradient of the displacements tensors (F fields) and the
            decomposed Rotation vector (for large strains) are returned
            Default = True

    Returns
    -------
        strainTensor: nx3x3 array of n cells
            The full strain field
            If `largeStrains = True` it is the decomposed right stretch tensor U - I
            If `largeStrains = False` it is the small strain symmetric tensor
            Its shape is (nz, ny, nx, 3, 3)

        volStrain: nx1 array of n cells strain tensors
            The volumetric strain field
            If `largeStrains = True` it is the determinant of the transformation gradient tensor: norm(F) - 1
            If `largeStrains = False` it is the trace of the small strain symmetric tensor
            Its shape is (nz, ny, nx)

        devStrain: nx1 array of n cells strain tensors
            The deviatoric strain field
            If `largeStrains = True` it is the norm of the deviatoric part of the right stretch tensor U
            If `largeStrains = False` ?
            Its shape is (nz, ny, nx)

        F: nx3x3 array of n cells
            The field of the transformation gradient tensors
            Its shape is (nz, ny, nx, 3, 3)
            Only if `onlyStrain = False`

        r: nx3x1 array of n cells
            Rotation in "rotation vector" format
            Its shape is (nz, ny, nx, 3)
            Only if onlyStrain=False and largeStrains=True

    WARNING
    -------
        This function deals with structured mesh thus ``x`` and ``z`` axis are swapped **in python**.

    """
    import numpy
    #import spam.DIC.deformationFunction
    import spam.mesh.strain

    twoD = False

    if largeStrains:
        print("\n*** The strain field is computed under the hypothesis of large strains ***")
        smallStrains = False
    else:
        print("\n*** The strain field is computed under the hypothesis of small strains ***")
        smallStrains = True

    # Define dimensions
    nNodes = [n for n in displacementField.shape[0:3]]
    nCells = [n-1 for n in nNodes]

    # Check if a 2D field is passed
    if nNodes[0] == 1:
        twoD = True

        # Add a ficticious layer of nodes and cells in Z direction
        nNodes[0] += 1
        nCells[0] += 1
        nodeSpacing[0] += 1

        # Add a ficticious layer of equal displacements so that the strain in z is null
        displacementField  = numpy.concatenate((displacementField, displacementField))

    # Set the output matrices
    if largeStrains:
        # Stretch tensor
        U = numpy.zeros((nCells[0], nCells[1], nCells[2], 3, 3))
        # Rotation vector
        r = numpy.zeros((nCells[0], nCells[1], nCells[2], 3))
    elif smallStrains:
        # Small strains tensor
        e = numpy.zeros((nCells[0], nCells[1], nCells[2], 3, 3))
    # Deformation gradient tensor F = du/dx +I
    F = numpy.zeros((nCells[0], nCells[1], nCells[2], 3, 3))
    # Volumetric strain
    volStrain = numpy.zeros((nCells[0], nCells[1], nCells[2], 1))
    # Deviatoric strain
    devStrain = numpy.zeros((nCells[0], nCells[1], nCells[2], 1))

    # Define the coordinates of the Parent Element
    # we're using isoparametric Q8 elements
    lid = numpy.zeros((8, 3)).astype('<u1')  # local index
    lid[0] = [0, 0, 0]
    lid[1] = [0, 0, 1]
    lid[2] = [0, 1, 0]
    lid[3] = [0, 1, 1]
    lid[4] = [1, 0, 0]
    lid[5] = [1, 0, 1]
    lid[6] = [1, 1, 0]
    lid[7] = [1, 1, 1]

    # Calculate the derivatives of the shape functions
    # Since the center is equidistant from all 8 nodes, each one gets equal weighting
    SFderivative = numpy.zeros((8,3))
    for node in range(8):
        # (local nodes coordinates) / weighting of each node
        SFderivative[node, 0] = (2.0 * (float(lid[node, 0]) - 0.5)) / 8.0
        SFderivative[node, 1] = (2.0 * (float(lid[node, 1]) - 0.5)) / 8.0
        SFderivative[node, 2] = (2.0 * (float(lid[node, 2]) - 0.5)) / 8.0

    # Compute the jacobian to go from local(Parent Element) to global base
    jacZ = 2.0 / float(nodeSpacing[0])
    jacY = 2.0 / float(nodeSpacing[1])
    jacX = 2.0 / float(nodeSpacing[2])

    # Loop over the cells
    for kCell in range(nCells[0]):
        print("\rWorking on cell: {} of {}".format(kCell+1, nCells[0]), end=''),
        for jCell in range(nCells[1]):
            for iCell in range(nCells[2]):

                # Check for nans in one of the 8 nodes of the cell
                dCell = displacementField[kCell:kCell+2,jCell:jCell+2, iCell:iCell+2]
                if numpy.all( numpy.isfinite( dCell ) ) == False:
                    if largeStrains:
                        U[kCell, jCell, iCell, :, :] = numpy.zeros((3, 3)) * numpy.nan
                        r[kCell, jCell, iCell, :] = numpy.zeros(3) * numpy.nan
                    else:
                        e[kCell, jCell, iCell, :, :] = numpy.zeros((3, 3)) * numpy.nan
                    F[kCell, jCell, iCell, :, :] = numpy.zeros((3, 3)) * numpy.nan
                    volStrain[kCell, jCell, iCell, :] = numpy.zeros(1) * numpy.nan
                    devStrain[kCell, jCell, iCell, :] = numpy.zeros(1) * numpy.nan

                # If no nans start the strain calculation
                else:
                    # Initialise the gradient of the displacement tensor
                    dudx = numpy.zeros((3, 3))

                    # Loop over each node of the cell
                    for node in range(8):
                        # Get the displacement value
                        d = displacementField[int(kCell+lid[node, 0]), int(jCell+lid[node, 1]), int(iCell+lid[node, 2]), :]

                        # Compute the influence of each node to the displacement gradient tensor
                        dudx[0, 0] += jacZ * SFderivative[node,0] * d[0]
                        dudx[1, 1] += jacY * SFderivative[node,1] * d[1]
                        dudx[2, 2] += jacX * SFderivative[node,2] * d[2]
                        dudx[1, 0] += jacY * SFderivative[node,1] * d[0]
                        dudx[0, 1] += jacZ * SFderivative[node,0] * d[1]
                        dudx[2, 1] += jacX * SFderivative[node,2] * d[1]
                        dudx[1, 2] += jacY * SFderivative[node,1] * d[2]
                        dudx[2, 0] += jacX * SFderivative[node,2] * d[0]
                        dudx[0, 2] += jacZ * SFderivative[node,0] * d[2]

                    # Fill the fields
                    if largeStrains:
                        Fi, Ui, ri, volStraini, devStraini = spam.mesh.strain.decomposeDisplacementGradientLargeStrains(dudx, twoD=twoD)
                        U[kCell, jCell, iCell, :, :] = Ui
                        r[kCell, jCell, iCell, :] = ri
                    elif smallStrains:
                        Fi, ei, volStraini, devStraini = spam.mesh.strain.decomposeDisplacementGradientSmallStrains(dudx, twoD=twoD)
                        e[kCell, jCell, iCell, :, :] = ei
                    F[kCell, jCell, iCell, :, :] = Fi
                    volStrain[kCell, jCell, iCell, :] = volStraini
                    devStrain[kCell, jCell, iCell, :] = devStraini

    if largeStrains:
        if onlyStrain:
            return (U-numpy.eye(3), volStrain, devStrain)
        else:
            return (U-numpy.eye(3), F, r, volStrain, devStrain)
    elif smallStrains:
        if onlyStrain:
            return (e, volStrain, devStrain)
        else:
            return (e, F, volStrain, devStrain)


def createCylindricalMask(shape, radius, voxSize=1.0, centre=None):
    """
    Create a image mask of a cylinder in the z direction.

    Parameters
    ----------
        shape: array, int
            The shape of the array the where the cylinder is saved
        radius: float
            The radius of the cylinder
        voxSize: float (default=1.0)
            The physical size of a voxel
        centre: array of floats of size 2, (default None)
            The center [y,x] of the axis of rotation of the cylinder.
            If None it is taken to be the centre of the array.

    Returns
    -------
        cyl: array, int
            The cylinder

    """
    import numpy

    cyl = numpy.zeros(shape).astype('<u1')

    if centre is None:
        centre = [float(shape[1])/2.0, float(shape[2])/2.0]

    for iy in range(cyl.shape[1]):
        y = (float(iy)+0.5)*float(voxSize)
        for ix in range(cyl.shape[2]):
            x = (float(ix)+0.5)*float(voxSize)
            dist = numpy.sqrt((x-centre[1])**2 + (y-centre[0])**2)
            if dist < radius:
                cyl[:, iy, ix] = 1

    return cyl


def structuringElement(radius=1, order=2, margin=0, dim=3):
    """
    This function construct a structural element.

    Parameters
    -----------
        radius : int, default=1
            The `radius` of the structural element

            .. code-block:: text

                radius = 1 gives 3x3x3 arrays
                radius = 2 gives 5x5x5 arrays
                ...
                radius = n gives (2n+1)x(2n+1)x(2n+1) arrays

        order : int, default=2
            Defines the shape of the structuring element by setting the order of the norm
            used to compute the distance between the centre and the border.

            A representation for the slices of a 5x5x5 element (size=2) from the center to on corner (1/8 of the cube)

            .. code-block:: text

                order=numpy.inf: the cube
                1 1 1    1 1 1    1 1 1
                1 1 1    1 1 1    1 1 1
                1 1 1    1 1 1    1 1 1

                order=2: the sphere
                1 0 0    0 0 0    0 0 0
                1 1 0    1 1 0    0 0 0
                1 1 1    1 1 0    1 0 0

                order=1: the diamond
                1 0 0    0 0 0    0 0 0
                1 1 0    1 0 0    0 0 0
                1 1 1    1 1 0    1 0 0

        margin : int, default=0
            Gives a 0 valued margin of size margin.

        dim : int, default=3
            Spatial dimension (2 or 3).

    Returns
    --------
        array
            The structural element
    """
    import numpy

    tb = tuple([2*radius+2*margin+1 for _ in range(dim)])
    ts = tuple([2*radius+1 for _ in range(dim)])
    c = numpy.abs(numpy.indices(ts) - radius)
    d = numpy.zeros(tb)
    s = tuple([slice(margin, margin+2*radius+1) for _ in range(dim)])
    d[s] = numpy.power(numpy.sum(numpy.power(c, order), axis=0), 1.0/float(order)) <= radius
    return d.astype('<u1')


def createLexicoCoordinates(lenghts, nNodes, origin=(0, 0, 0)):
    """
    Create a list of coordinates following the lexicographical order.

    Parameters
    ----------
        lengths: array of floats
            The length of the cuboids in every directions.
        nNodes: array of int
            The number of nodes of the mesh in every directions.
        origin: array of floats
            The coordinates of the origin of the mesh.

    Returns
    -------
        array
            The list of coordinates. ``shape=(nx*ny*nz, 3)``

    """
    import numpy

    x = numpy.linspace(origin[0], lenghts[0]+origin[0], nNodes[0])
    y = numpy.linspace(origin[1], lenghts[1]+origin[1], nNodes[1])
    z = numpy.linspace(origin[2], lenghts[2]+origin[2], nNodes[2])
    cx = numpy.tile(x, (1, nNodes[1]*nNodes[2]))
    cy = numpy.tile(numpy.sort(numpy.tile(y, (1, nNodes[0]))), (1, nNodes[2]))
    cz = numpy.sort(numpy.tile(z, (1, nNodes[0]*nNodes[1])))
    return numpy.transpose([cx[0], cy[0], cz[0]])
