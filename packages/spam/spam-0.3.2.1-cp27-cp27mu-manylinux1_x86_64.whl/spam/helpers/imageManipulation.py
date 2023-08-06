from __future__ import print_function

import numpy
import tifffile


def stackToArray(prefix, sufix='.tif', stack=range(10), digits='05d', createMask=False, erosion=False, verbose=False):
    """
    Convert of stack of 2D sequential tif images into a 3D array.

    Parameters
    ----------
        prefix : string
            The common name of the 2D images files before the sequential number
        sufix : string, default='.tif'
            The common name and extension of the 2D images after the sequential number
        stack : sequence, default=range(10)
            The numbers of the slices with no formating (with no leading zeros)
        digits : string, default='05d'
            The format (number of digits) of the numbers (add leading zeros).
        createMask : bool, default=False
            Create a mask while stacking the slices. Has been tested for cylinders.
        erosion : bool, default=None
            Apply an erosion of 1px to the mask in order to avoid border noise.
        verbose: bool, default=False
            Verbose mode if True.

    Returns
    -------
        im : array
            The 3D image
        mask : array
            The 3D mask (full of 1 if ``createMask=None``)

    """

    if verbose:
        print("spam.helpers.imageManipulation.stackToArray:")
        print('\tfrom: {p}{first:{d}}{s}'.format(p=prefix, s=sufix, first=stack[0], d=digits))
        print('\tto:   {p}{last:{d}}{s}'.format(p=prefix, s=sufix, last=stack[-1], d=digits))

    # Step 1 If nBytes is not defined: we open the first slice just for the dimensions
    slice_name = '{h}{s:{d}}{t}'.format(h=prefix, t=sufix, s=stack[0], d=digits)
    slice_im = tifffile.imread(slice_name)

    # Step 2 compute the dimension and create the 3D array
    ny = slice_im.shape[0]
    nx = slice_im.shape[1]
    nz = len(stack)
    im = numpy.zeros([nz, ny, nx], dtype=slice_im.dtype)

    # Step 2.1 create empty mask (8 bits)
    mask = numpy.ones([nz, ny, nx], dtype='<u1')

    # Step 3 stack all the slices
    for i, s in enumerate(stack):
        slice_name = '{h}{s:{d}}{t}'.format(h=prefix, t=sufix, s=s, d=digits)
        if verbose:
            print('\tStack slice number {}/{} ({s:{d}})'.format(i+1, len(stack), s=s, d=digits))
        im[i, :, :] = tifffile.imread(slice_name)
        # we fill the mask
        if createMask:
            mask[i, :, :] = _mask2D(im[i, :, :], erosion=erosion)

    return im, mask


def crop(im, boxSize, boxOrigin=None):
    """This function crops an image using slicing.

    Parameters
    ----------
        im: array
            The image to crop.
        boxSize: int
            The size in voxels of the crop box (from boxOrigin). If a int, the size is the same for each axis. If a sequence, ``boxSize`` should contain one value for each axis.
        boxOrigin : int, default=None
            The coordinates in voxels of the origin of the crop box. If a int, the coordinates are the same for each axis. If a tuple, ``boxOrigin`` should contain one value for each axis. If ``None`` the image is cropped from its centre.

    Returns
    -------
            array
                The cropped image.
    """

    # get center of the image
    imCentre = [int(s)/2 for s in im.shape]
    # get sizes
    (sz, sy, sx) = (boxSize,   boxSize,   boxSize) if isinstance(boxSize, int) else boxSize

    # get box origin
    if boxOrigin is not None:
        (cz, cy, cx) = (boxOrigin, boxOrigin, boxOrigin) if isinstance(boxOrigin, int) else boxOrigin
    else:
        (cz, cy, cx) = (imCentre[0]-sz//2, imCentre[1]-sy//2, imCentre[2]-sx//2)

    # test sizes
    if (cz+sz > im.shape[0] or cy+sy > im.shape[1] or cx+sx > im.shape[2]):
        print("spam.helpers.imageManipulation.crop: box bigger than image.")
        print("exit function.")
        return -1

    return im[int(cz):int(cz+sz),
              int(cy):int(cy+sy),
              int(cx):int(cx+sx)]


def rescale(im, scale=(0, 1)):
    """This function **rescale** an image according to a scale
    and save it to as n bytes floats.

    Parameters
    ----------
        im: array
            The image to rescale.

        scale : (float, float), default=(0 1)
            The min and max of the rescaled image.

    Returns
    -------
        array, float
            The rescaled image.

    Examples
    --------
        >>> im = numpy.random.randn( 100, 100, 100 ).astype( '<f4' )
        produce float32 array of positive and negative numbers
        >>> imRescaled = rescale( im, scale=[-1, 1] )
        produce float32 array of numbers between -1 and 1

    """

    im_max = float(im.max())
    im_min = float(im.min())

    return (min(scale)+(max(scale)-min(scale))*((im.astype('<f4')-im_min)/(im_max-im_min))).astype('<f4')


def rescaleToInteger(im, nBytes=1, scale=None):
    """This function **rescale** an image to an unsigned integer.

    Parameters
    ----------
        im: array, float32
            The image to rescale.

        nBytes : int, default=1
            The number of bytes of the unsigned interger output.
            Possible values are power of 2.

            .. code-block:: text

                reminder
                1 byte  =  8 bits -> ouput from 0 to           255
                2 bytes = 16 bits -> ouput from 0 to        65 535
                4 bytes = 32 bits -> ouput from 0 to 4 294 967 295

        scale : (float, float), default=None
            If None, the maximum and minimum use for the rescaling is the maximum and the minimum of the image.

    Returns
    -------
        array, uint
            The rescaled image

    Examples
    --------
        >>> im = numpy.random.randn( 100, 100, 100 ).astype( '<f4' )
        produce float32 array of positive and negative numbers
        >>> imRescaled = rescaleToInteger( im, nBytes=4 )
        produce uint32 array of numbers between 0 and 4 294 967 295

    """

    nBytes = int(nBytes)
    if ((nBytes & (nBytes - 1)) != 0):
        print("spam.helpers.imageManipulation.rescaleToInteger: nBytes = {}. Should be a power of 2.".format(nBytes))
        print("exit function.")
        return -1

    if scale is None:
        # if no scale is given: it takes the max and min of the image
        im_max = im.max()
        im_min = im.min()
    else:
        # if a scale is given take it if larger (smaller) than max (min) of image
        im_max = max(scale) if max(scale) > im.max() else im.max()
        im_min = min(scale) if min(scale) < im.min() else im.min()

    im_min = float(im_min)
    im_max = float(im_max)

    return ((2**(8*nBytes)-1)*((im.astype('<f4')-im_min)/(im_max-im_min))).astype('<u{}'.format(nBytes))


def convertUnsignedIntegers(im, nBytes=1):
    """This function **convert** an images of unsigned integers.

    Note: this function does not rescale.

    Parameters
    ----------
        im: array, uint
            The image to convert.

        nBytes : int, default=1
            The number of bytes of the unsigned interger output.
            Possible values are power of 2.

            .. code-block:: text

                reminder
                1 byte  =  8 bits -> ouput from 0 to           255
                2 bytes = 16 bits -> ouput from 0 to        65 535
                4 bytes = 32 bits -> ouput from 0 to 4 294 967 295

    Returns
    -------
        array, uint
            The converted image.

    Examples
    --------
        >>> im = numpy.random.randint( 12, high=210, size=(100, 100, 100) ).astype( '<u1' )
        produce an uint8 array of numbers between 12 and 210
        >>> imRescaled = rescaleToInteger( im, nBytes=2 )
        produce an uint16 array 3084 and 53970

    """

    nBytes = int(nBytes)
    if ((nBytes & (nBytes - 1)) != 0):
        print('spam.helpers.imageManipulation.convertUnsignedIntegers: nBytes = {}. Should be a power of 2.'.format(nBytes))
        print("exit function.")
        return -1

    # number of bits of the output
    nbo = 8*nBytes

    # number of bits of the input
    inputType = im.dtype
    if inputType == numpy.uint8:
        nbi = 8
    elif inputType == numpy.uint16:
        nbi = 16
    elif inputType == numpy.uint32:
        nbi = 32
    elif inputType == numpy.uint64:
        nbi = 64
    else:
        print('spam.helpers.imageManipulation.convertUnsignedIntegers: im.dytpe = {}. Input should be uint.'.format(inputType))
        print("exit function.")
        return -1

    return (float(2**nbo-1)*(im) / float(2**nbi-1)).astype('<u{}'.format(nBytes))


def singleShift(im, shift, axis, sub=0):
    """ This function shift the image and replace the border by an substitution value.

    It uses on ``numpy.roll``.

    Parameters
    -----------
        im : array
            The input to shift.
        shift : int
            The number of places by which elements are shifted (from numpy.roll).
            Default: 1
        axis : int
            The axis along which elements are shifted (from numpy.rool).
        sub : foat, default=0
            The substitution value of the border

    Returns
    -------
        array :
            The shifted image.

    """

    # Step 1: Cyclic permutation on im
    im = numpy.roll(im, shift, axis=axis)

    # Step 2: get image dimension
    dim = len(im.shape)

    # Step 3: modify the boundary with replacement value
    if dim == 2:  # if 2D image
        if shift == 1 and axis == 0:
            im[0, :] = sub
        elif shift == -1 and axis == 0:
            im[-1, :] = sub
        elif shift == 1 and axis == 1:
            im[:, 0] = sub
        elif shift == -1 and axis == 1:
            im[:, -1] = sub
    elif dim == 3:  # if 3D image
        if shift >= 1 and axis == 0:
            im[0:shift, :, :] = sub
        elif shift <= -1 and axis == 0:
            im[shift:, :, :] = sub
        elif shift >= 1 and axis == 1:
            im[:, 0:shift, :] = sub
        elif shift <= -1 and axis == 1:
            im[:, shift:, :] = sub
        elif shift >= 1 and axis == 2:
            im[:, :, 0:shift] = sub
        elif shift <= -1 and axis == 2:
            im[:, :, shift:] = sub
    else:
        print("spam.helpers.imageManipulation.singleShift: dim={}. Should be 2 or 3.".format(dim))
        print("exit function.")
        return -1

    return im


def multipleShifts(im, shifts, sub=0):
    """
    This function call ``singleShift`` multiple times.

    Parameters
    ----------
        im : array
            The input to shift.
        shifts : [int, int, int]
            Defines the number of shifts to apply in every axis.

            .. code-block:: text

                shift = [s_x, s_y, s_z] applies a shift of:
                .   s_x on axis 0
                .   s_y on axis 1
                .   s_z on axis 2

        sub : float, default=0
            The substitution value of the border

    Returns
    -------
        array :
            The shifted image.

    """

    # loop over the n axis
    for i in range(len(shifts)):
        # if the value of the shift is not 0 on axis i
        if shifts[i]:
            # we call singleShift (only once)
            im = singleShift(im, shift=shifts[i], axis=i)

    return im


def binarisation(im, threshold=0.0, boolean=False, op='>', mask=None):
    """This function binarise an input image according to a given threshold

    It has an option to apply a mask to the binarized image to ignore the
    outside of the sample/specimen

    Parameters
    -----------
        im: array
            The image to binarise.
        threshold : float
            the input limit value for binarization
        boolean : bool
            Changes the output format and phase distribution (see output)
        op : string, default='>'
            defines the thresholding operation
        mask : array, default=None
            The mask of the input image: is 0 outside the boundary(specimen) and 1 inside

    Returns
    --------
        phases : array
            The repartition of phases resulting the binarisation.

            For operator '>' it gives, if ``boolean=True``:

            .. code-block:: text

                0 - masked parts (where mask equals 0)
                0 - below threshold
                1 - above threshold

            and if ``boolean=False``

            .. code-block:: text

                0 - masked parts (where mask equals 0)
                1 - below threshold
                2 - above threshold

    Note
    ----
        I'm not sure this function is really needed since it can really easily be replaced
        by numpy logical functions. --- Manu

    """

    import operator

    # Step 1: Get operator
    operation = {'>': operator.gt,
                 '<': operator.lt,
                 '>=': operator.ge,
                 '<=': operator.le,
                 '=': operator.eq}.get(op)

    # Step 2: binarisation
    phases = operation(im, threshold).astype('<u1')

    # Step 3: rescaling if bool
    if not boolean:
        phases += 1

    # Step 4: apply mask
    if mask is not None:
        phases = phases * mask

    return phases


# private functions

def _mask2D(im, erosion=False, structure=None, ):
    """get contour of 2D image.
    """

    import cv2
    from scipy import ndimage

    # step 2: convert into uint8 if not the case
    if im.dtype != 'uint8':
        # actually it rescales the image but it doesn't really amtter
        im = rescaleToInteger(im, nBytes=1)

    # Step 3: ...
    blur = cv2.GaussianBlur(im, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    largest = 0
    biggest = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if largest < area:
            largest = area
            biggest = contour

    mask = numpy.zeros(im.shape, dtype='<u1')
    cv2.drawContours(mask, [biggest], 0, 1, -1)

    # Step 4: apply erosion of the mask (which corresponds to an erosion of the specimen)
    if erosion:
        mask = ndimage.morphology.binary_erosion(
            mask, structure=structure).astype(mask.dtype)

    return mask
