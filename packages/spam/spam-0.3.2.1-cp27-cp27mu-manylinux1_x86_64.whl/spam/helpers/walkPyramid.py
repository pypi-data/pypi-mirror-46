'''
    2017-04-14 Edward Ando
    
    Moved code here for walking down a pyramid -- this will eventually save a lot of time -- at least for the pixel search, although at the moment for the subpixel there is quite a lot of unwanted structure created in the change of levels
    
'''
from __future__ import print_function


def _walkPyramid(im1pyramid, im2pyramid):
    """
        !!! Untested !!!
    """
    firstPass = True

    # Loop over the pyramid lists backwards, i.e., smallest image first
    for im1floor, im2floor in zip(im1pyramid[::-1], im2pyramid[::-1]):
        print("Downscale level: ", im1floor['zoom'])

        d.corrWin = numpy.round(correaltionHalfWindow / im1floor['zoom'])
        d.nodeSpacing

        if firstPass:
            d.searchWin = numpy.round(searchWin / im1floor['zoom'])
            firstPass = False
        else:
            # TODO: maybe even remove this? sub=pixels refinement should be fine...
            d.searchWin = numpy.array([[0, 0], [-2, 2], [-2, 2]])

        if im1floor['zoom'] == 1:
            d.degreesOfFreedom[d.t.disp] = 1
            d.degreesOfFreedom[d.t.rot] = 0
            d.degreesOfFreedom[d.t.scal] = 0
            d.degreesOfFreedom[d.t.shear] = 0
        else:
            d.degreesOfFreedom[d.t.disp] = 1
            d.degreesOfFreedom[d.t.rot] = 0
            d.degreesOfFreedom[d.t.scal] = 0
            d.degreesOfFreedom[d.t.shear] = 0

        ###############################################################
        # Set up a mesh for the current image resolution
        ###############################################################
        k, zNodes, yNodes, xNodes = layout_nodes.layout_nodes(
            nodeSpacing, [[0, 0, 0], im1floor['shape']], corrWin)
        numberOfNodes = k.shape[0]
        ###############################################################

        ###############################################################
        # If this is not the first pass through the data, interpolate previous kinematics onto current kinematics
        ###############################################################
        if im1floor['zoom'] != im1pyramid[-1]['zoom']:
            # Update kinematics of k from kPrev which is at the previous resolution
            d.pixelSearch = False

            # To account for this change of resolution, multiply positions and displacements:
            # Displacements first
            kPrev[:, d.kCols.Zpos:d.kCols.Xpos +
                  1] *= zoomPrev/im1floor['zoom']
            kPrev[:, d.kCols.Zdisp:d.kCols.Xdisp +
                  1] *= zoomPrev/im1floor['zoom']

            k = regular_prior_interpolator.regular_prior_interpolator(kPrev, k)
            tifffile.imsave("yDisp-interp-scale={}.tif".format(im1floor['zoom']), k[:, kCols.Ydisp].reshape(
                len(zNodes), len(yNodes), len(xNodes)).astype('<f4'))
            tifffile.imsave("xDisp-interp-scale={}.tif".format(im1floor['zoom']), k[:, kCols.Xdisp].reshape(
                len(zNodes), len(yNodes), len(xNodes)).astype('<f4'))

        k = correlateNodes.correlateNodes(im1floor['image'], im2floor['image'], k, range(
            numberOfNodes), searchWin, pixelSearch, degreesOfFreedom, interpolationOrder, greyThreshold, d.twoD, d.lab1)

        tifffile.imsave("yDisp-scale={}.tif".format(im1floor['zoom']), k[:, kCols.Ydisp].reshape(
            len(zNodes), len(yNodes), len(xNodes)).astype('<f4'))
        tifffile.imsave("xDisp-scale={}.tif".format(im1floor['zoom']), k[:, kCols.Xdisp].reshape(
            len(zNodes), len(yNodes), len(xNodes)).astype('<f4'))

        # Undo scaling on mesh dimensions -- displacements should be fine
        #k[:,kCols.Zpos:kCols.Xpos+1] *= im1floor['zoom']

        kPrev = k.copy()
        zoomPrev = im1floor['zoom']

        print

        # if im1floor['zoom'] != 1:
        #kNew, zNodes, yNodes, xNodes = layout_nodes.layout_nodes( nodeSpacingOrig, [ [0,0,0], [ im1.shape[0]*2, im1.shape[1]*2, im1.shape[2]*2 ] ] )
        #kNew = regular_prior_interpolator.regular_prior_interpolator( k, kNew )
