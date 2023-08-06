from __future__ import print_function
"""This module offers a set of tools for unstructured 3D meshes made of tetrahedra.

>>> # import module
>>> import spam.mesh
>>> spam.mesh.createCuboid()


WARNING
-------
    System dependencies
        * ``gmsh``
    Python dependencies
        * ``pygmsh``
        * ``meshio``
"""
import numpy
import spam.mesh


def createCuboid(lengths, lcar, origin=[0., 0., 0.], verbose=False, gmshFile=None, vtkFile=None):
    """
    Creates an unstructured mesh of tetrahedra inside a cuboid.

    Parameters
    ----------
        lengths: 1D array
            The lengths of the cuboid in the three directions
            The axis order is zyx

        origin: 1D array
            The origin of the cuboid (zyx)

        lcar: float
            characteristic length of the elements of the mesh
            (`i.e.`, the average distance between two nodes)

        gmshFile: string, optional
            If not None, save the clear text gmsh file with name ``gmshFile`` and suffix ``.msh``
            Default = None

        vtkFile: string, optional
            If not None, save the clear text vtk file with name ``vtkFile`` and suffix ``.vtk``
            Defaut = None

        verbose: bool, optionsl
            Verbose mode.
            Default = False

    Returns
    -------
        points: 2D numpy array
            The coordinates of the mesh nodes (zyx)
            Each line is [zPos, yPos, xPos]

        connectivity: 2D numpy array
            The connectivity matrix of the tetrahedra elements
            Each line is [node1, node2, node3, node4]

    Example
    -------
        >>> points, connectivity = spam.mesh.createCuboid((1.0,1.5,2.0), 0.5)
        create a mesh in a cuboid of size 1,1.5,2 with a characteristic length of 0.5
    """

    import pygmsh
    import meshio

    # We will switch the input arrays from zyx to xyz before passing them to pygmsh
    lengths = lengths[::-1]
    origin = origin[::-1]

    lx, ly, lz = lengths
    ox, oy, oz = origin
    geom = pygmsh.built_in.Geometry()
    poly = geom.add_polygon([[ox,    ly+oy, oz],
                             [lx+ox, ly+oy, oz],
                             [lx+ox, oy,    oz],
                             [ox,    oy,    oz]], lcar=lcar)
    geom.extrude(poly, translation_axis=[0., 0., lz])

    # create mesh and get connectivity
#    points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=['mesh.Algorithm3D=4', '-optimize_netgen'])
    points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize","-algo","del3d","-clmin",str(lcar),"-clmax",str(lcar)])
    connectivity = cells['tetra']

    # write gmsh/vtk file
    if gmshFile is not None:
        meshio.write_points_cells("{}.msh".format(gmshFile), points, cells, file_format='gmsh2-ascii')
    if vtkFile is not None:
        meshio.write_points_cells("{}.vtk".format(vtkFile), points, {'tetra': connectivity}, file_format='vtk-ascii')

    # NOTE: pygmsh returns coordinates in xyz. This means that:
    # 1. the coordinates array must be switched back to zyx
    # 2. the connectivity array must change so that the nodes of each tetrahedron are numbered
    #    in such a way that the Jacobian is positive. Which means a perturbation of the node numbering.

    points = points[:, ::-1]
    tmp = connectivity.copy()
    connectivity[:, 1] = tmp[:, 3]
    connectivity[:, 3] = tmp[:, 1]

    # return coordinates and connectivity matrix
    return points, connectivity


def createCylinder(centre, radius, height, lcar, verbose=False, gmshFile=None, vtkFile=None):
    """
    Creates an unstructured mesh of tetrahedra inside a cylinder.
    The height of the cylinder is along the z axis.

    Parameters
    ----------
        centre: 1D array
            The two coordinates of the centre of the base disk (yx).

        radius: float
            The radius of the base disk.

        height: float
            The height of the cylinder of the z direction.

        lcar: float
            length of the mesh.
            The average distance between two nodes.

        gmshFile: string, optional
            If not None, save the clear text gmsh file with name ``gmshFile`` and suffix ``.msh``
            Default = None

        vtkFile: string, optional
            If not None, save the clear text vtk file with name ``vtkFile`` and suffix ``.vtk``
            Defaut = None

        verbose: bool, optionsl
            Verbose mode.
            Default = False

    Returns
    -------
        points: 2D numpy array
            The coordinates of the mesh nodes (zyx)
            Each line is [zPos, yPos, xPos]

        connectivity: 2D numpy array
            The connectivity matrix of the tetrahedra elements
            Each line is [node1, node2, node3, node4]

    Example
    -------
        >>> points, connectivity =  spam.mesh.createCylinder((0.0,0.0), 0.5, 2.0, 0.5)
        create a mesh in a cylinder of centre 0,0,0 radius, 0.5 and height 2.0 with a characteristic length of 0.5
    """

    import pygmsh
    import meshio

    # unpack
    cy, cx = centre
    r = radius

    # raw code
    code = []
    code.append("Point(1) = {{ {x}, {y},  0, {lcar} }};".format(x=cx,   y=cy,   lcar=lcar))
    code.append("Point(2) = {{ {x}, {y},  0, {lcar} }};".format(x=cx+r, y=cy,   lcar=lcar))
    code.append("Point(3) = {{ {x}, {y},  0, {lcar} }};".format(x=cx,   y=cy+r, lcar=lcar))
    code.append("Point(4) = {{ {x}, {y},  0, {lcar} }};".format(x=cx-r, y=cy,   lcar=lcar))
    code.append("Point(5) = {{ {x}, {y},  0, {lcar} }};".format(x=cx,   y=cy-r, lcar=lcar))
    code.append("Circle(1) = { 2, 1, 3 };")
    code.append("Circle(2) = { 3, 1, 4 };")
    code.append("Circle(3) = { 4, 1, 5 };")
    code.append("Circle(4) = { 5, 1, 2 };")
    code.append("Line Loop(5) = { 1, 2, 3, 4 };")
    code.append("Plane Surface(6) = { 5 };")
    code.append("Extrude {{ 0, 0, {h} }} {{ Surface{{ 6 }}; }}".format(h=height))

    # geom = pygmsh.opencascade.Geometry(characteristic_length_min=lcar, characteristic_length_max=lcar,)

    # add raw code to geometry
    geom = pygmsh.built_in.Geometry()
    geom.add_raw_code(code)

    # mesh
#    points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize_netgen"])
    points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize","-algo","del3d","-clmin",str(lcar),"-clmax",str(lcar)])
    connectivity = cells['tetra']

    # write gmsh/vtk file
    if gmshFile is not None:
        meshio.write_points_cells("{}.msh".format(gmshFile), points, cells, file_format='gmsh2-ascii')
    if vtkFile is not None:
        meshio.write_points_cells("{}.vtk".format(vtkFile), points, {'tetra': connectivity}, file_format='vtk-ascii')

    # NOTE: pygmsh returns coordinates in xyz. This means that:
    # 1. the coordinates array must be switched back to zyx
    # 2. the connectivity array must change so that the nodes of each tetrahedron are numbered
    #    in such a way that the Jacobian is positive. Which means a perturbation of the node numbering.

    points = points[:, ::-1]
    tmp = connectivity.copy()
    connectivity[:, 1] = tmp[:, 3]
    connectivity[:, 3] = tmp[:, 1]

    # return coordinates and connectivity matrix
    return points, connectivity


def delaunayFromVoronoi(COM, radii=None, radius=None, edges=None):
    """
    Make a clean Delaunay traingulation for granular materials from a
    voronoi tesselation of the particles. Code from Ryan Hurley

    Parameters
    -----------
        COM : Nx3 numpy array
            Centres of mass of particles to triangulate

        radii : Nx1 numpy array
            Radii of particles, optional, Default = None

        radius - float
            radius: an approximate mean radius of particles if not passing radii above
            Optional, Default = None

        edges : 3-list of 2-lists
            specifies the start and end sizes of the box the points are in.
            Optional, Default = None (min and max of COM)

    Returns
    --------
        Tetrahedron connectivity array, Nx4 numpy array

    Example
    --------
        if "lab" is a 3D labelled image of grains:
        spam.mesh.delaunayFromVoronoi(spam.label.getCentresOfMass(lab), radii=spam.label.getEquivalent Radii(lab))
    """
    import pyvoro
    from progressbar import ProgressBar

    # Force floats in COM
    # COM = COM[1:].astype('<f4')
    COM = COM.astype('<f4')

    if radii is None and radius is None:
        print("mesh.unstructured.delaunayFromVoronoi(): Radii array or radius number needs to be passed")
        return

    if radii is not None:
        maxrad = radii.max()
        radii = radii[1:].tolist()
    else:
        maxrad = radius
        radii = []

    edgeBuf = maxrad*4.0
    if edges is None:
        # Construct edge and buffer input for voro++
        # Use 4x max rad for edge buffer -- ignore
        edges = [[COM[:, 0].min()-edgeBuf, COM[:, 0].max()+edgeBuf],
                 [COM[:, 1].min()-edgeBuf, COM[:, 1].max()+edgeBuf],
                 [COM[:, 2].min()-edgeBuf, COM[:, 2].max()+edgeBuf]]

    # Run voro. Use 5x rad max for dispersion (max search distance)
    # pyvoro wants lists, now convert COM
    print("mesh.unstructured.delaunayFromVoronoi(): Starting pyvoro (may take several minutes) ...", end='')
    voroAll = pyvoro.compute_voronoi(COM.tolist(),
                                     edges,
                                     edgeBuf*5.0,
                                     radii=radii)
    print("done")

    # return(voroAll,data_com)
    pbar = ProgressBar()

    # Recursively check for 4 particles that are all neighbours in voroAll
    numGrains = len(voroAll)
    alltets = []
    print("mesh.unstructured.delaunayFromVoronoi(): Constructing Delaunay from Voronoi...")
    for grain in pbar(range(numGrains)):
        # Loop through contacts of grain
        numberOfNeighbours = len(voroAll[grain]['faces'])

        # Create neighbour list for grain
        neighbourListZero = []
        for jj in range(numberOfNeighbours):
            neighbourListZero.append(voroAll[grain]['faces'][jj]['adjacent_cell'])

        # Loop over neighbours of grain
        for jj in range(numberOfNeighbours):
            neighbourNumber1 = len(voroAll[neighbourListZero[jj]]['faces'])

            # Create neighbour list (neighbourList1) for neighbourListZero[jj]
            neighbourList1 = []
            for kk in range(neighbourNumber1):
                neighbourList1.append(voroAll[neighbourListZero[jj]]['faces'][kk]['adjacent_cell'])

            # Continue if grain not in neighbourList1
            if (not grain in neighbourList1):  # should be grain not in neighbourList1 (ER)
                continue

            # If grain in neighbourList1, loop over neighbourList1
            for kk in range(neighbourNumber1):
                neighbourNumber2 = len(voroAll[neighbourList1[kk]]['faces'])

                # Build neighbour list (neighbourList2) for neighbourList1[kk]
                neighbourList2 = []
                for ll in range(neighbourNumber2):
                    neighbourList2.append(voroAll[neighbourList1[kk]]['faces'][ll]['adjacent_cell'])

                # Continue if grain not in neighbourList2
                if (not grain in neighbourList2):  # should be grain not in neighbourList2 (ER)
                    continue

                # If grain in neighbourList2,. loop over neighbourList2
                for ll in range(neighbourNumber2):
                    neighbourNumber3 = len(voroAll[neighbourList2[ll]]['faces'])

                    # Build neighbour list (neighbourList3) for neighbourList2[ll]
                    neighbourList3 = []
                    for mm in range(neighbourNumber3):
                        neighbourList3.append(voroAll[neighbourList2[ll]]['faces'][mm]['adjacent_cell'])

                    # Continue if grain not in neighbourList3 or neighbourListZero[jj] not in neighbourList3
                    if ((not grain in neighbourList3) or (not neighbourListZero[jj] in neighbourList3)):  # should be grain not in neighbourList3 (ER)
                        continue

                    # Create temporary list. Append if list does not contain boundary
                    tmplist = [grain, neighbourListZero[jj], neighbourList1[kk], neighbourList2[ll]]
                    if (min(float(idx) for idx in tmplist) < 0):
                        continue

                    alltets.append(tmplist)

    # Convert list to np array and remove non-unique rows
    alltets = numpy.array(alltets)
    alltets = numpy.sort(alltets, axis=-1)
    y = numpy.ascontiguousarray(alltets).view(numpy.dtype((numpy.void, alltets.dtype.itemsize * alltets.shape[1])))
    _, idx = numpy.unique(y, return_index=True)
    alltets_unique = alltets[idx]

    # Remove rows with duplicate entries
    idxkeep = []
    for ii in range(alltets_unique.shape[0]):
        if numpy.unique(alltets_unique[ii]).shape[0] == 4:
            idxkeep.append(ii)
    alltets_unique_new = alltets_unique[idxkeep]

    # Return alltets_unique_new -- compensate for removing the first row of radii and COM
    # return(alltets_unique_new+1)
    return(alltets_unique_new)


def bagiStrainFromDelaunay(delaunay, com1, com2, largeStrains=True, onlyStrain=True):
    """
    Calculates displacement gradient function using Bagi's 1996 paper, especially equantion 3 on page 174.
    Required inputs are delaunary triangulation (for example from spam.mesh.delaunayFromVoronoi) and
    nodal positions in reference and deformed configurations.

    Parameters
    ----------
        delaunay : n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.delaunayFromVoronoi for example

        com1 : m x 3 numpy array
            M Particles' coordinates in reference configuration

        com2 : m x 3 numpy array
            M Particles' coordinates in deformed configuration

        largeStrains: bool, optional
            Use Large/finite strains framework (recommended)?
            Default = True

    Returns
    -------
        strainTensor: nx3x3 array of n cells
            The full strain field
            If `largeStrains = True` it is the decomposed right stretch tensor U - I
            If `largeStrains = False` it is the small strain symmetric tensor
            Its shape is (nz, ny, nx, 3, 3)

        F: nx3x3 array of n cells
            The field of the transformation gradient tensors
            Its shape is (nz, ny, nx, 3, 3)
            Only if `onlyStrain = False`

        r: nx3x1 array of n cells
            Rotation in "rotation vector" format
            Its shape is (nz, ny, nx, 3)
            Only if onlyStrain=False and largeStrains=True

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

    """
    # Example
    # -------
    # tetStrainSym,tetStrainAsym = spam.mesh.bagiStrainFromDelaunay(delaunay,com1,com2)
    # returns infinitesimal strain and rotation tensors in each tetrahedron.
    from progressbar import ProgressBar
    pbar = ProgressBar()

    if largeStrains:
        # print("\n*** The strain field is computed under the hypothesis of large strains ***")
        smallStrains = False
        F = numpy.zeros([delaunay.shape[0], 3, 3], dtype='<f4')
        U = numpy.zeros([delaunay.shape[0], 3, 3], dtype='<f4')
        R = numpy.zeros([delaunay.shape[0], 3], dtype='<f4')
        volStrain = numpy.zeros(delaunay.shape[0], dtype='<f4')
        devStrain = numpy.zeros(delaunay.shape[0], dtype='<f4')
    else:
        # print("\n*** The strain field is computed under the hypothesis of small strains ***")
        smallStrains = True
        F = numpy.zeros([delaunay.shape[0], 3, 3], dtype='<f4')
        e = numpy.zeros([delaunay.shape[0], 3, 3], dtype='<f4')
        volStrain = numpy.zeros(delaunay.shape[0], dtype='<f4')
        devStrain = numpy.zeros(delaunay.shape[0], dtype='<f4')

    # define dimension
    D = 3.0

    # Import modules

    # Construct 4-list of 3-lists of combinations constituting a face of the tet
    combs = [[0, 1, 2],
             [1, 2, 3],
             [2, 3, 0],
             [0, 1, 3]]
    unode = [3, 0, 1, 2]

    # Precompute tetrahedron Volumes
    tetVolumes1 = spam.mesh.tetVolumes(delaunay, com1)
    # tetVolumes2 = spam.mesh.tetVolumes(delaunay, com2)
    # print("\tbagiStrainFromDelaunay(): TetVolStrain:", ((tetVolumes2-tetVolumes1)/tetVolumes1).mean())

    # Initialize arrays for tet strains
    # print("spam.mesh.bagiStrainFromDelaunay(): Constructing strain from Delaunay and Displacements")

    # Loop through tetrahdra to get avec1, uPos1
    # for tet in pbar(range(delaunay.shape[0])):
    for tet in range(delaunay.shape[0]):
        # Get the list of IDs, centroids, center of tet
        tet_ids = delaunay[tet, :]
        tetComs1 = com1[tet_ids, :]
        tetComs2 = com2[tet_ids, :]
        tetCen = numpy.average(tetComs1, axis=0)

        # Loop through each face of tet to get avec, upos (Bagi, 1996, pg. 172)
        aVec1 = numpy.zeros([4, 3], dtype='<f4')
        uPos1 = numpy.zeros([4, 3], dtype='<f4')
        uPos2 = numpy.zeros([4, 3], dtype='<f4')
        displacementGradient = numpy.zeros((3, 3), dtype='<f4')

        for face in range(4):
            faceNorm = numpy.cross(tetComs1[combs[face][0]]-tetComs1[combs[face][1]],
                                   tetComs1[combs[face][0]]-tetComs1[combs[face][2]])

            # Get a norm vector to face point towards center of tet
            faceCen = numpy.average(tetComs1[combs[face]], axis=0)
            tmpnorm = faceNorm / (numpy.linalg.norm(faceNorm))
            facetocen = tetCen-faceCen
            if (numpy.dot(facetocen, tmpnorm) < 0):
                tmpnorm = -tmpnorm

            # Divide by 6 (1/3 for 1/Dimension; 1/2 for area from cross product)
            # See first eqn., Bagi, 1996, pg. 172.
            aVec1[face] = tmpnorm*numpy.linalg.norm(faceNorm)/6

            # Undeformed positions
            uPos1[face] = tetComs1[unode[face]]

            # Deformed positions
            uPos2[face] = tetComs2[unode[face]]

            displacementGradient += numpy.tensordot((uPos2[face] - uPos1[face]), aVec1[face], axes=0)

        displacementGradient /= float(tetVolumes1[tet])

        # Compute strains
        if largeStrains:
            F[tet], U[tet], R[tet], volStrain[tet], devStrain[tet] = spam.mesh.decomposeDisplacementGradientLargeStrains(displacementGradient)
        else:
            F[tet], e[tet], volStrain[tet], devStrain[tet] = spam.mesh.decomposeDisplacementGradientSmallStrains(displacementGradient)

    # print("\n",uPos1,"\n\n",uPos2,"\n\n",aVec1,"\n\n",displacementGradient)
    if largeStrains:
        if onlyStrain:
            return (U-numpy.eye(3), volStrain, devStrain)
        else:
            return (U-numpy.eye(3), F, R, volStrain, devStrain)
    elif smallStrains:
        if onlyStrain:
            return (e, volStrain, devStrain)
        else:
            return (e, F, volStrain, devStrain)


def projectTetFieldToGrains(delaunay, tetField, com2):
    """
    Projects/coarse-grains any field defined on tetrahedra onto grains by volume-averaging over
    all tetrahedra for which a given grain is a node.
    This can be useful for smoothing out a noisy strain field and will not affect the overall agreement between
    the average of strains and the macroscopically observed strains (R.C. Hurley has verified this in a 2017 paper).

    Parameters
    ----------
        delaunay: n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.delaunayFromVoronoi for example

        tetField: n x 3 x 3 numpy array
            Any field defined on tetrahedra (e.g., Bagi strains from bagiStrainFromDelaunay).

        com2: m x 3 numpy array
            M Particles' coordinates (in deformed configuration for strain field)

    Returns
    -------
        grainField: m x 3 x 3
            array containing (3x3) arrays of strain

    Example
    -------
        grainStrain = spam.mesh.projectBagiStrainToGrains(delaunay,bagiStrain[0],com2)
            Returns strains for each grain.

    """
    # grainStrainVoigt:  Ng array containing (6x1) arrays of strain in Voigt notation.
    # RCH Oct 2018.

    # Import modules
    import numpy
    import scipy.spatial as sps
    from progressbar import ProgressBar
    pbar = ProgressBar()

    #print("spam.mesh.projectTetFieldToGrains(): Pre-computing volumes...", end='')
    tetVolumes2 = spam.mesh.tetVolumes(delaunay, com2)
    #print("done.")

    # Initialize list of grain values
    grainField = numpy.zeros(([com2.shape[0]] + list(tetField.shape[1:])), dtype='<f4')
    # Get all the unique grain IDs in the Deluanay triangulation

    #print("spam.mesh.projectTetFieldToGrains(): Projecting tetrahedal to grains...")
    # Loop through grains...
    #for label in pbar(range(com2.shape[0])):
    for label in range(com2.shape[0]):
        # Get the list of tets for which this label is a node
        touchingTets = numpy.where(delaunay == label)[0]

        volTot = 0.0
        fieldTot = numpy.zeros(list(tetField.shape[1:]), dtype='<f4')
        # Loop through list of tets, summing the strains
        for touchingTet in touchingTets:
            vol = tetVolumes2[touchingTet]
            # Track total volume
            volTot += vol

            # Add volume-weighted field
            fieldTot += tetField[touchingTet]*vol

        # Divide strainTot by volTot
        fieldTot = fieldTot/volTot

        # Store in particles
        grainField[label] = fieldTot

    return(grainField)


def _projectBagiStrainToGrains(delaunay, tet_strain, com2):
    """
    Projects/coarse-grains strains from tetrahedra onto grains by volume-averaging over
        all tetrahedra for which a given grain is a node. This can be useful for smoothing
        out a noisy strain field and will not affect the overall agreement between
        the average of strains and the macroscopically observed strains (we have
        verified this in a 2017 paper).

    Parameters
    ----------
        delaunay: n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.delaunayFromVoronoi for example

        tet_strain: n x 3 x 3 numpy array
            Tetrahedra strain from spam.mesh.bagiStrainFromDelaunay. This can be
            either tetStrainsSym or tetStrainAsym. The resulting projected/coarse-grained
            will be either the symmetric or skew-symmetric strain, respectively

        com2: m x 3 numpy array
            M Particles' coordinates in deformed configuration

    Returns
    -------
        grainStrain: m x 3 x 3
            array containing (3x3) arrays of strain

    Example
    -------
        grainStrain = spam.mesh.projectBagiStrainToGrains(delaunay,tet_strain,com2)
            Returns strains for each grain.

    """
    # grainStrainVoigt:  Ng array containing (6x1) arrays of strain in Voigt notation.
    # RCH Oct 2018.

    # Import modules
    import numpy
    import scipy.spatial as sps
    from progressbar import ProgressBar
    pbar = ProgressBar()

    # Initialize list of tet strains
    grainStrain = []
    # grainStrainVoigt = []
    # Get all the unique grain IDs in the Deluanay triangulation
    indxuniq = numpy.unique(delaunay)

    print("spam.mesh.projectBagiStrainToGrains(): Projecting strains to grains...\n")
    # Loop through tetrahdrons to get avecs, uPos1
    for tet in pbar(range(indxuniq.shape[0])):
        # Get the list of tets for which this grain is a node
        indx = numpy.where(delaunay == indxuniq[tet])

        volTot = 0.0
        strainTot = numpy.zeros((3, 3))
        # Loop through list of tets, summing the strains
        for jj in range(indx[0].shape[0]):
            # Get volume
            tet_ids = delaunay[indx[0][jj], :]
            tetComs1 = com2[tet_ids, :]
            cvxh = sps.ConvexHull(tetComs1)
            vol = cvxh.volume

            # Add volume and strain
            strainTot = strainTot + tet_strain[indx[0][jj]]*vol
            volTot = volTot + vol

        # Divide strainTot by volTot
        strainTot = strainTot/volTot

        # Store in particles
        grainStrain.append(numpy.array(strainTot))
        # grainStrainVoigt.append(numpy.array([strainTot[0, 0], strainTot[1, 1], strainTot[2, 2],
        # strainTot[1, 2], strainTot[0, 2], strainTot[0, 1]]))
    # return(grainStrain, grainStrainVoigt)
    return(grainStrain)


def _projectBagiStrainToGrid(delaunay, tet_strain, com2, nx=8, ny=8, nz=10):
    """
    Projects/coarse-grains strains from tetrahedra onto a grid. The first step is
        constructing a Cartesian grid based on the extremal positions of all tetrahedra
        nodes. The next step is finding all tetrahedra having a node within each grid cell.
        the final step is volume-averaging over all of the corresponding tetrahedra.

    Parameters
    ----------
        delaunay: n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.delaunayFromVoronoi for example

        tet_strain: n x 3 x 3 numpy array
            Tetrahedra strail from spam.mesh.bagiStrainFromDelaunay. This can be
            either tetStrainsSym or tetStrainAsym. The resulting projected/coarse-grained
            will be either the symmetric or skew-symmetric strain, respectively

        com2: m x 3 numpy array
            M Particles' coordinates in deformed configuration

    Returns
    -------
        gridStrain:
            Ng array containing (3x3) arrays of strain. (Ng = number of grains)

    Example
    -------
        grid_bounds,num_in_grid,gridStrain
            = spam.mesh.projectBagiStrainToGrid(delaunay,tet_strain,com2,nx,ny,nz)
            Returns strains for each grid zone and boundaries of grid zone.

    """
    # gridStrainVoigt:  Ng array containing (6x1) arrays of strain in Voigt notation.
    # RCH Oct 2018.

    # Import modules
    import numpy
    import scipy.spatial as sps
    from progressbar import ProgressBar
    pbar = ProgressBar()

    # Artificial edge buffer to make sure we grab the outer-most particles
    edgeBuf = 0.01

    # Get sample extents for grid
    edges = numpy.array([[com2[:, 0].min()-edgeBuf, com2[:, 0].max()+edgeBuf],
                         [com2[:, 1].min()-edgeBuf, com2[:, 1].max()+edgeBuf],
                         [com2[:, 2].min()-edgeBuf, com2[:, 2].max()+edgeBuf]])

    # Construct grid with convention xmin,xmax,ymin,ymax,zmin,zmax
    grid_bounds = []
    xspace = (edges[0, 1]-edges[0, 0])/(nx)
    yspace = (edges[1, 1]-edges[1, 0])/(ny)
    zspace = (edges[2, 1]-edges[2, 0])/(nz)
    for ii in range(nz):
        for jj in range(nx):
            for kk in range(ny):
                grid_bounds.append(numpy.array([edges[0, 0]+jj*xspace, edges[0, 0]+(jj+1)*xspace,
                                                edges[1, 0]+kk*yspace, edges[1, 0]+(kk+1)*yspace,
                                                edges[2, 0]+ii*zspace, edges[2, 0]+(ii+1)*zspace]))
    grid_bounds = numpy.array(grid_bounds)

    # Initialize list of tet strains
    gridStrain = []
    # gridStrainVoigt = []
    # First, find all grains in each grid:
    print("spam.mesh.projectBagiStrainToGrid(): Projecting tetrahedal field to grid...\n")
    for ii in pbar(range(grid_bounds.shape[0])):
        xcond = numpy.logical_and(com2[:, 0] > grid_bounds[ii, 0], com2[:, 0] <= grid_bounds[ii, 1])
        ycond = numpy.logical_and(com2[:, 1] > grid_bounds[ii, 2], com2[:, 1] <= grid_bounds[ii, 3])
        zcond = numpy.logical_and(com2[:, 2] > grid_bounds[ii, 4], com2[:, 2] <= grid_bounds[ii, 5])
        indgrain = numpy.where(numpy.logical_and(xcond, numpy.logical_and(ycond, zcond)))

        # Find all tets for which these grains act as a node:
        indtet = []
        for jj in range(indgrain[0].shape[0]):
            indtettmp, _ = numpy.where(delaunay == indgrain[0][jj])
            for kk in range(indtettmp.shape[0]):
                indtet.append(indtettmp[kk])

        # Find unique values of these tets
        indtet = numpy.unique(indtet, return_index=False)

        # Loop over unique tets to get volume-averaged strains
        volTot = 0.0
        strainTot = numpy.zeros((3, 3))
        num_in_grid = []
        num_in_grid_tmp = 0
        if (indtet.shape[0] > 0):
            for jj in range(indtet.shape[0]):
                # Get volume
                tet_ids = delaunay[indtet[jj], :]
                tetComs1 = com2[tet_ids, :]
                cvxh = sps.ConvexHull(tetComs1)
                vol = cvxh.volume

                # Add volume and strain
                strainTot = strainTot + tet_strain[indtet[jj]]*vol
                volTot = volTot + vol

            # Divide strainTot by volTot
            strainTot = strainTot/volTot
            num_in_grid_tmp = num_in_grid_tmp + indtet.shape[0]

        # Store in grid
        num_in_grid.append(num_in_grid_tmp)
        gridStrain.append(numpy.array(strainTot))
        # gridStrainVoigt.append(numpy.array([strainTot[0, 0], strainTot[1, 1], strainTot[2, 2],
        # strainTot[1, 2], strainTot[0, 2], strainTot[0, 1]]))

    # return(grid_bounds, num_in_grid, gridStrain, gridStrainVoigt)
    return(grid_bounds, num_in_grid, gridStrain)


def BCFieldFromDVCField(meshNodes, dvcField, mask=None, pixelSize=1.0, meshType="cube", centre=[0, 0], radius=1.0, topBottom=False, tol=1e-6, neighbours=4):
    """
    This function imposes boundary conditions coming from a DVC result to the nodes of an unstructured FE mesh.

    Parameters
    ----------
        meshNodes: 2D numpy array
            Array of ``n`` node positions of the unstructured mesh
            Each line is [nodeNumber, z, y, x]

        dvcField: 2D numpy array
            Array of ``m`` points of the dvc field
            Each line is [zPos, yPos, xPos, zDisp, yDisp, xDisp]

        mask: 2D numpy array, optional
            Boolean array of ``m`` points of the dvc field
            Points with 0 will be ignored for the field interpolation
            Default = None (`i.e.` interpolate based on all of the dvc points)

        pixelSize: float, optional
            physical size of a pixel (`i.e.` 1mm/px)
            Default = 1.0

        meshType: string, optional
            For the moment, valid inputs are ``cube`` and ``cylinder``
            The axis of a cylinder is considered to be ``z``
            Note that if a cylindrical mesh is passed, ``centre`` and ``radius`` are highly recommended
            Default = `cube`

        centre: float, optional
            The centre of the cylinder [y, x] in physical units (`i.e.` mm)
            Default = [0, 0]

        radius: float, optional
            The radius of the cylinder in physical units (`i.e.` mm)
            Default = 1.0

        topBottom: bool, optional
            If boundary conditions are passed only for the top (`i.e.` z=zmax)  and bottom (`i.e.` z=zmin) surfaces of the mesh
            Default = False

        tol: float, optional
            Numerical tolerance for floats equality
            Default = 1e-6

        neighbours: int, , optional
            Neighbours for field interpolation
            Default = 4
    Returns
    -------
        bc: 2D numpy array
            Boundary node displacements
            Each line is [nodeNumber, zPos, yPos, xPos, zDisp, yDisp, xDisp]

    WARNING
    -------
        1. All coordinates and displacement arrays are ``z``, ``y``, ``x``
        2. The axis of a cylinder is considered to be ``z``
    """
    import numpy
    from scipy.spatial import KDTree

    # STEP 1: find the edge nodes
    posMax = [meshNodes[:, i].max() for i in range(1, 4)]
    posMin = [meshNodes[:, i].min() for i in range(1, 4)]
    bcNodes = []

    if meshType == "cube":
        # extract edge nodes from the mesh
        for node in meshNodes:
            if topBottom:
                testMin = abs(node[1] - posMin[0]) < tol
                testMax = abs(node[1] - posMax[0]) < tol
            else:
                testMin = abs(node[1] - posMin[0]) < tol or abs(node[2] - posMin[1]) < tol or abs(node[3] - posMin[2]) < tol
                testMax = abs(node[1] - posMax[0]) < tol or abs(node[2] - posMax[1]) < tol or abs(node[3] - posMax[2]) < tol
            if testMin or testMax:
                bcNodes.append(node)
    elif meshType == "cylinder":
        # extract edge nodes from the mesh
        for node in meshNodes:
            testZ = abs(node[1] - posMin[0]) < tol or abs(node[1] - posMax[0]) < tol
            testXY = False
            if not topBottom:
                testXY = (node[2] - centre[0])**2 + (node[3] - centre[1])**2 >= (radius - tol)**2
            if testZ or testXY:
                bcNodes.append(node)

    bcNodes = numpy.array(bcNodes)
    m = bcNodes.shape[0]

    # STEP 2: convert dvc field to physical unit
    dvcField *= pixelSize

    # STEP 3: Interpolate the disp values of FE using a weighted influence of the k nearest neighbours from DVC coord
    bcDisp = numpy.zeros((m, 3))
    # create the k-d tree of the coordinates of DVC good points
    if mask is None:
        mask = numpy.ones(dvcField.shape[0])

    goodPoints = numpy.where(mask == 1)
    treeCoord = KDTree(dvcField[:, :3][goodPoints])

    for node in xrange(m):
        distance, ind = treeCoord.query(bcNodes[node, 1:], k=neighbours)

        # Check if we've hit the same point
        if numpy.any(distance == 0):
            bcDisp[node, 0] = dvcField[goodPoints][ind][numpy.where(distance == 0)][0, 3]
            bcDisp[node, 1] = dvcField[goodPoints][ind][numpy.where(distance == 0)][0, 4]
            bcDisp[node, 2] = dvcField[goodPoints][ind][numpy.where(distance == 0)][0, 5]

        else:
            weightSumInv = sum(1/distance)
            # loop over neighbours
            for neighbour in xrange(neighbours):
                # calculate its weight
                weightInv = (1/distance[neighbour]) / float(weightSumInv)
                # replace the disp values the weighted disp components of the ith nearest neighbour
                bcDisp[node, 0] += dvcField[goodPoints][ind[neighbour], 3] * weightInv
                bcDisp[node, 1] += dvcField[goodPoints][ind[neighbour], 4] * weightInv
                bcDisp[node, 2] += dvcField[goodPoints][ind[neighbour], 5] * weightInv

    # return node number and displacements
    return numpy.hstack((bcNodes, bcDisp))


def tetVolumes(connectivity, positions):
    """
    This function computes volumes of the tetrahedra passed with a connectivity matrix.
    Using algorithm in https://en.wikipedia.org/wiki/Tetrahedron#Volume

    Parameters
    ----------
        connectivity : n times 4 array
            Array of ``n`` none numbers that are connected as tetrahedra (e.g., the output from Delaunay)

        positions : m times 3 array
            Array of ``m`` positions of the nodes

    Returns
    -------
        volumes : vector of length n
            Volumes of tetrahedra
    """
    import numpy
    # Sanity checks on lengths:
    if connectivity.shape[1] != 4 or positions.shape[1] != 3 or connectivity.max() > positions.shape[0]:
        print("spam.mesh.tetVolumes(): Dimensionality problem, not running")
        return

    volumes = numpy.zeros(connectivity.shape[0], dtype='<f4')

    # loop through tetrahedra
    for tetNumber in range(connectivity.shape[0]):
        fourNodes = connectivity[tetNumber]
        a = positions[fourNodes[0]]
        b = positions[fourNodes[1]]
        c = positions[fourNodes[2]]
        d = positions[fourNodes[3]]
        volumes[tetNumber] = numpy.abs(numpy.dot((a - d), numpy.cross((b - d), (c - d)))) / 6.0

    return volumes
