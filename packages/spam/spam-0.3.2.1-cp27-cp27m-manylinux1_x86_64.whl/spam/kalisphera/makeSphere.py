from __future__ import print_function
import spam.kalisphera._kalispheraToolkit as kaliC
import numpy

real_t = '<f8'
# also need to select double or float in kalisphera C call


def run(vol, centre, radius):
    """
        This function creates a sphere in a given 3D volume,
        with analytically-calculated partial-volume effects.
        Background is assumed to have a greyvalue of zero,
        and a fully-occupied sphere voxel is considered to
        have a greyvalue of 1.

        Greyvalues are added to the volume, so spheres can be
        added to an existing background.

        Parameters
        ----------
        vol : 3D numpy array of doubles
            A 3D image of greylevels (typically zeros) into which sphere(s) should be added

        centre : 1D or 2D numpy array
            Either a 3-component vector, or an Nx3 matrix of sphere centres to draw with respect to 0,0,0 in `vol`

        radius : float or 1D numpy array
            Raduis(ii) of spheres to draw in `vol`


        Returns
        -------
        None : function updates vol
    """

    if len(vol.shape) != 3:
        print("\tkalisphera.makeSphere.run(), need 3D vol array")
        exit

    centre = numpy.array(centre, dtype=real_t)

    # Turn centre into a numpy array in case it is passed as a list-of-lists
    if len(centre.shape) == 1:
        centre = numpy.array([centre])

    if len(centre.shape) == 2:
        if type(radius) == float or type(radius) == int:
            #print("\tkalisphera.makeSphere.run(), Got single radius for multiple spheres... fine")
            radius = [radius]*centre.shape[0]

        if len(radius) == centre.shape[0]:
            for centre, radius in zip(centre, radius):
                volTemp = numpy.zeros_like(vol, dtype=real_t)
                ## For compatibility with scipy centre of mass
                #centre+=0.5
                # print centre, radius
                # print vol.sum()
                kaliC.kalisphera(volTemp, numpy.array(centre).astype(real_t), float(radius))
                # print vol.sum()
                vol += volTemp #.copy()

        else:
            print(
                "\tkalisphera.makeSphere.run(), Got multiple radii, but different number from number of centres")
            exit
