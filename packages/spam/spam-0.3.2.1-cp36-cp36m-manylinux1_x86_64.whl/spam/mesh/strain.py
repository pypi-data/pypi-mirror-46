import numpy
import spam.DIC

def decomposeDisplacementGradientLargeStrains(dudx, twoD=False):
    """
    This module computes strain components given a displacement gradient grad(u) in large strains

    This uses Denis's Caillerie's polar decomposition -- see doc/theory.
    Here it is first a U followed by an R, i.e., F = R.U

    The inputs to this function can come from both spam.mesh.structured.computeStrainField
    or spam.mesh.unstructured.bagiStrainFromDelaunay

    Parameters
    ----------
        dudx : 3x3 numpy array of floats
            Single displacement gradient tensor

        twoD : bool
            Whether dudx represents a 2D (Y,X) gradient.
            Optional. Default = False

    Returns
    -------
        Fi : 3x3 numpy array of floats
            Deformation gradient tensor F=du/dx+I

        Ui : 3x3 numpy array of floats
            Symmetric right stretch tensor

        ri : 3x1 numpy array of floats
            Orthogonal rotation tensor

        volStraini : float
            Volumetric strain (the determinant of F=du/dx+I) -- first invariant of strain

        devStraini : float
            Deviatoric strain -- second invariant of strain
    """
    # Compute the deformation gradient tensor F=du/dx+I
    Fi = numpy.eye(3) + dudx

    # to get rid of numerical noise in 2D
    if twoD:
        Fi[0, :] = [1.0, 0.0, 0.0]
        Fi[:, 0] = [1.0, 0.0, 0.0]

    # We're going for a polar decomposition of F = RU
    # U is right stretch tensor
    # R is rotation tensor

    paddedF = numpy.eye(4)
    paddedF[0:3, 0:3] = Fi
    Ui = spam.DIC.deformationFunction.decomposePhi(paddedF)["U"]
    ri = spam.DIC.deformationFunction.decomposePhi(paddedF)["r"]

    # Compute the volumetric strain from the determinant of F
    volStraini = numpy.linalg.det(Fi) - 1

    # Decompose U into an isotropic and deviatoric part
    # and compute the deviatoric strain as the norm of the deviatoric part
    if twoD:
        Udev = Ui[1:, 1:]*(numpy.linalg.det(Fi[1:, 1:])**(-1/2.0))
        devStraini = numpy.linalg.norm(Udev-numpy.eye(2))
    else:
        Udev = Ui*(numpy.linalg.det(Fi)**(-1/3.0))
        devStraini = numpy.linalg.norm(Udev-numpy.eye(3))

    return Fi, Ui, ri, volStraini, devStraini


def decomposeDisplacementGradientSmallStrains(dudx, twoD=False):
    """
    This module computes strain components given a displacement gradient grad(u) in large strains

    The inputs to this function can come from both spam.mesh.structured.computeStrainField
    or spam.mesh.unstructured.bagiStrainFromDelaunay

    Parameters
    ----------
        dudx : 3x3 numpy array of floats
            Single displacement gradient tensor

        twoD : bool
            Whether dudx represents a 2D (Y,X) gradient.
            Optional. Default = False

    Returns
    -------
        Fi : 3x3 numpy array of floats
            Deformation gradient tensor F=du/dx+I

        ei : 3x3 numpy array of floats
            Strain tensor in small strains

        volStraini : float
            Volumetric strain (the trace of ei) -- first invariant of strain

        devStraini : float
            Deviatoric strain -- second invariant of strain
    """
    # Compute the deformation gradient tensor F=du/dx+I
    Fi = numpy.eye(3) + dudx

    # to get rid of numerical noise in 2D
    if twoD:
        Fi[0, :] = [1.0, 0.0, 0.0]
        Fi[:, 0] = [1.0, 0.0, 0.0]

    # In small strains: 0.5(F+F.T)
    ei = 0.5*(Fi+Fi.T) - numpy.eye(3)

    # The volumetric strain is the trace of the strain matrix
    volStraini = numpy.trace(ei)

    # The deviatoric in the norm of the matrix
    if twoD:
        devStraini = numpy.linalg.norm((ei[1:,1:]-numpy.eye(2)*volStraini/2.0))
    else:
        devStraini = numpy.linalg.norm((ei-numpy.eye(3)*volStraini/3.0))

    return Fi, ei, volStraini, devStraini
