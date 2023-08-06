import numpy
import spam.helpers


# operations on greyscale images

def greyDilation(im, nBytes=1):
    """
    This function apply a dilation on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=1
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The dilated image
    """
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 2: Determine substitution value
    sub = 2**(8*nBytes)-1
    # Step 3: apply dilation                                             #  x  y  z
    outputIm = im  # 0  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im,  1, 0, sub=sub))  # 1  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 0, sub=sub))  # -1  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im,  1, 1, sub=sub))  # 0  1  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 1, sub=sub))  # 0 -1  0
    if dim == 3:
        outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im,  1, 2, sub=sub))  # 0  0  1
        outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 2, sub=sub))  # 0  0 -1
    return outputIm


def greyErosion(im, nBytes=1):
    """
    This function apply a erosion on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=1
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The eroded image
    """
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 2: Determine substitution value
    sub = 2**(8*nBytes)-1
    # Step 1: apply erosion                                                       #  x  y  z
    outputIm = im  # 0  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im,  1, 0, sub=sub))  # 1  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 0, sub=sub))  # -1  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im,  1, 1, sub=sub))  # 0  1  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 1, sub=sub))  # 0 -1  0
    if dim == 3:
        outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im,  1, 2, sub=sub))  # 0  0  1
        outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 2, sub=sub))  # 0  0 -1
    return outputIm


def greyMorphologicalGradient(im, nBytes=1):
    """
    This function apply a morphological gradient on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=1
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The morphologycal gradient of the image
    """
    return (greyDilation(im, nBytes=nBytes) - im)


# operation on binary images

def binaryDilation(im, sub=False):
    """
    This function apply a dilation on a binary scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        sub: bool, default=False
            Subtitute value.

    Returns
    --------
        numpy array
            The dilated image
    """
    # Step 0: import as bool
    im = im.astype(bool)
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 1: apply dilation                             #  x  y  z
    outputIm = im  # 0  0  0
    outputIm = outputIm | spam.helpers.singleShift(im,  1, 0, sub=sub)  # 1  0  0
    outputIm = outputIm | spam.helpers.singleShift(im, -1, 0, sub=sub)   # -1  0  0
    outputIm = outputIm | spam.helpers.singleShift(im,  1, 1, sub=sub)  # 0  1  0
    outputIm = outputIm | spam.helpers.singleShift(im, -1, 1, sub=sub)  # 0 -1  0
    if dim == 3:
        outputIm = outputIm | spam.helpers.singleShift(im,  1, 2, sub=sub)  # 0  0  1
        outputIm = outputIm | spam.helpers.singleShift(im, -1, 2, sub=sub)  # 0  0 -1
    return numpy.array(outputIm).astype('<u1')


def binaryErosion(im, sub=False):
    """
    This function apply a erosion on a binary scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        sub: bool, default=False
            Subtitute value.

    Returns
    --------
        numpy array
            The eroded image
    """
    # Step 1: apply erosion with dilation --> erosion = ! dilation( ! image )
    return numpy.logical_not(binaryDilation(numpy.logical_not(im), sub=sub)).astype('<u1')


def binaryMorphologicalGradient(im, sub=False):
    """
    This function apply a morphological gradient on a binary scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=False
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The morphologycal gradient of the image
    """
    return (numpy.logical_xor(binaryDilation(im, sub=sub), im)).astype('<u1')


# def _binary_reconstruction_from_edges(im, dmax=0):
#     """
#     Calculate the morphological reconstruction of an image (binary) with the edges of a CUBE as a marker!
#     PARAMETERS:
#     - im (3D numpy.array): The input image (binary)
#     - dmax (int): the maximum geodesic distance. If zero, the reconstruction is complete.
#     RETURNS:
#     - (3D numpy.array): The reconstructed image
#     TODO:
#     - Consider mask for other geometry than cube
#     #- Consider different marker than the edges (for example, two opposite faces for percolation test)
#     HISTORY:
#     2016-04-21 (Sun Yue): First version of the function
#     """
#     # Step 1: compute marker
#     size = im.shape[0]
#     bord = numpy.zeros((size, size, size), dtype=bool)
#     bord[0, :, :] = im[0, :, :]
#     bord[-1, :, :] = im[-1, :, :]
#     bord[:, 0, :] = im[:, 0, :]
#     bord[:, -1, :] = im[:, -1, :]
#     bord[:, :, 0] = im[:, :, 0]
#     bord[:, :, -1] = im[:, :, -1]
#
#     # Step 2: first dilation and intersection
#     temp1 = (binaryDilation(bord)) & (im)
#     temp2 = temp1
#     temp1 = (binaryDilation(temp2)) & (im)
#     distance = 1
#
#     if dmax == 0:
#         dmax = 1e99  # perform complete reconstruction
#     while ((not(numpy.array_equal(temp1, temp2))) & (distance < dmax)):
#         temp2 = temp1
#         temp1 = (binaryDilation(temp2)) & (im)
#         distance += 1
#         print('distance =', distance)
#
#     return temp1  # send the reconstructed image


def binaryReconstructionFromEdges(im, dmax=None, verbose=False):
    """
    Calculate the morphological reconstruction of an binary image with the edges of a cube as a marker

    Parameters
    -----------
        im: numpy array
            The input image
        dmax: int, default=None
            The maximum geodesic distance. If None, the reconstruction is complete.
        verbose: bool, default=False
            Verbose mode

    Returns
    --------
        numpy.array
            The reconstructed image
    """
    size = im.shape[0]
    bord = numpy.zeros((size, size, size), dtype=bool)
    bord[0, :, :] = im[0, :, :]
    bord[-1, :, :] = im[-1, :, :]
    bord[:, 0, :] = im[:, 0, :]
    bord[:, -1, :] = im[:, -1, :]
    bord[:, :, 0] = im[:, :, 0]
    bord[:, :, -1] = im[:, :, -1]

    # Step 2: first dilation and intersection
    rec1 = (binaryDilation(bord)) & (im)
    rec2 = rec1
    rec1 = (binaryDilation(rec2)) & (im)
    distance = 1

    if dmax is None:
        dmax = numpy.inf  # perform complete reconstruction
    while ((not(numpy.array_equal(rec1, rec2))) & (distance < dmax)):
        rec2 = rec1
        rec1 = (binaryDilation(rec2)) & (im)
        distance += 1
        if verbose:
            print('Distance = {}'.format(distance))

    return rec1  # send the reconstructed image


def reconstructionFromOppositeFaces(im, dmax=None, verbose=False):
    """
    Calculate the morphological reconstruction of an binary image with two opposite faces of a cube as a marker

    Parameters
    -----------
        im: numpy array
            The input image
        dmax: int, default=None
            The maximum geodesic distance. If None, the reconstruction is complete.
        verbose: bool, default=False
            Verbose mode

    Returns
    --------
        numpy.array
            The reconstructed image
    """
    # Step 1: compute marker
    size = im.shape[0]
    bord = numpy.zeros((size, size, size), dtype=bool)
    bord[0, :, :] = im[0, :, :]
    bord[-1, :, :] = im[-1, :, :]

    # Step 2: first dilation and intersection
    rec1 = (binaryDilation(bord)) & (im)
    rec2 = rec1
    rec1 = (binaryDilation(rec2)) & (im)
    distance = 1

    if dmax is None:
        dmax = numpy.inf  # perform complete reconstruction
    while ((not(numpy.array_equal(rec1, rec2))) & (distance < dmax)):
        rec2 = rec1
        rec1 = (binaryDilation(rec2)) & (im)
        distance += 1
        if verbose:
            print('Distance =', distance)

    return rec1  # send the reconstructed image
