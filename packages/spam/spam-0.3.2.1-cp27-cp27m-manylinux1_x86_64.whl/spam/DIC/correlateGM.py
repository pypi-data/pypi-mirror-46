# -*- coding: utf-8 -*-
# 2017-05-29 ER and EA


""" Library of image correlation functions for registering two images acquired with different modalities
"""
from __future__ import print_function

import scipy.ndimage
import numpy

from . import DICToolkit
from . import deformationFunction

import matplotlib as mpl
import matplotlib.pyplot as plt


numpy.set_printoptions(precision=3, suppress=True)
mpl.rc('font', size=6)
cmapPhases = 'Set1_r'


def multimodalRegistration(imF, imG, phaseDiagram, gaussianParameters, imFmask=None, PhiInit=None, margin=None,
                           maxIterations=50, minDeltaPhi=0.005, interpolationOrder=1,
                           verbose=False, GRAPHS=False, INTERACTIVE=False, sliceAxis=0, suffix="", rootPath=".", BINS=64):
    """
        Perform subpixel image correlation between imF and imG -- images of the same object acquired with different modalities.

        This function will deform imG until it best matches imF.
        The matching includes sub-pixel displacements, rotation, and linear straining of the whole image.
        The correlation of imF, imG will give a deformationFunction F which maps imF into imG.
        Phi(imF(x),imG(F.x)) = 0
        As per Equation (3) of Tudisco `et al.`

        "Discrete correlation" can be performed by masking imF.

        Parameters
        ----------
        imF : 3D numpy array
            The greyscale image that will not move

        imG : 3D numpy array
            The greyscale image that will be deformed

        gaussianParameters : 2D numpy array Nx6
            Key parameter which is the result of a 2D gaussian fit of the first N peaks in the joint histograms of
            imF and imG.
            The 6 parameters of the fit are:
            φ, μ(imF), μ(imG), and a, b, c, where {a,b,c} are the parameter that can be found for `two-dimensional elliptical Gaussian function` here:
            https://en.wikipedia.org/wiki/Gaussian_function, `i.e.`, coupled with imF², imF*imG and imG² respectively

        imFmask : 3D numpy array, float, optional
            A mask for the zone to correlate in imF with NaNs in the zone to not correlate. Default = None, `i.e.`, correlate all of imF minus the margin

        PhiInit : 4x4 numpy array, optional
            Initial transformation to apply. Default = numpy.eye(4), `i.e.`, no transformation

        margin : int, optional
            Margin, in pixels, to take in imF and imG to allow space for interpolation and movement.
            Default = None (`i.e.`, enough margin for a worse-case 45degree rotation with no displacement)

        maxIterations : int, optional
            Maximum number of quasi-Newton interations to perform before stopping. Default = 25

        minDeltaPhi : float, optional
            Smallest change in the norm of F (the transformation operator) before stopping. Default = 0.001

        interpolationOrder : int, optional
            Order of the greylevel interpolation for applying F to imF when correlating. Reccommended value is 3, but you can get away with 1 for faster calculations. Default = 3

        verbose : bool, optional
            Get to know what the function is really thinking, recommended for debugging only. Default = False

        GRAPHS : bool, optional
            Pop up a window showing the image differences (imF-imG) as imF is progressively deformed.


        Note
        ----
        This correlation is what is proposed in Tudisco et al. "An extension of Digital Image Correlation for intermodality image registration", section 4.3.
    """

    # if verbose:
    #     print("Enter registration")

    # for interactive graphs
    if INTERACTIVE:
        GRAPHS = True
        plt.ion()

    # Detect default case and calculate maring necessary for a 45deg rotation with no displacement
    if margin is None:
        # sqrt
        margin = int((3**0.5 - 1.0) * max(imF.shape)*0.5)
    else:
        # Make sure margin is an int
        margin = int(margin)

    # Exit clause for singular matrices
    singular = False

    crop = (slice(margin, imF.shape[0]-margin),
            slice(margin, imF.shape[1]-margin),
            slice(margin, imF.shape[2]-margin))

    # Figure out coordinates on which the correlation should happen, i.e., the non NaN ones
    # NOTE: these coordinates are within the cropped margin for interpolation
    # cropImCoordsFG = numpy.where( numpy.isfinite( imF[crop] ) )
    if imFmask is not None:
        # TODO: This could just be directly = mask and equals inv of mask
        #  i.e., arry a boolean mask and not a series of coord array
        cropImCoordsFG = numpy.where(imFmask[crop] is True)
        cropImCoordsBG = numpy.where(imFmask[crop] is False)
    else:
        # Everything regular, except that we might have NaNs in the CW...
        # cropImCoordsFG = numpy.ones_like(  imF[crop], dtype='bool' )
        # cropImCoordsBG = numpy.zeros_like( imF[crop], dtype='bool' )
        cropImCoordsFG = numpy.isfinite(imF[crop], dtype='bool')
        cropImCoordsBG = numpy.isnan(imF[crop], dtype='bool')

        # HACK
        # print cropImCoordsFG
        # print cropImCoordsBG

        # HACK: set nans in imG to zero
        imG[numpy.isnan(imG)] = 0.0

        # if numpy.isnan( imF[crop] ).sum() > 0 numpy.isnan( imG[crop] ).sum() > 0:

    # compute image centre
    # imFcentre = (numpy.array(imF.shape)-1)/2.0

    # If there is no initial Phi, initalise it to zero.
    if PhiInit is None:
        Phi = numpy.eye(4)
        imGdef = imG.copy()
    else:
        Phi = PhiInit.copy()
        # transform Phi that is define on the centre (so without additional translations) to the origin (so with additional translations)
        # Phi[0:3, -1] = deformationFunction.decomposePhi(PhiInit, PhiCentre=imFcentre)["t"]
        imGdef = deformationFunction.applyPhi(imG, Phi=Phi, interpolationOrder=interpolationOrder).astype(imG.dtype)

    # At this stage we've computed gradients which we are not going to update, imG and it's gradients will be set equal to
    #   their cropped versions:
    # imGdef      = imGdef[crop]
    # imGdefGradZ = imGdefGradZ[crop]
    # imGdefGradY = imGdefGradY[crop]
    # imGdefGradX = imGdefGradX[crop]

    # Mask nans in gradient (but not before or there are jumps when the grey goes to zero
    #   beacuse of this a label dilate of at least 1 is recommended)
    # imGdefGradZ[ numpy.where( numpy.isnan( imFgradZ ) ) ] = 0
    # imGdefGradY[ numpy.where( numpy.isnan( imFgradY ) ) ] = 0
    # imGdefGradX[ numpy.where( numpy.isnan( imFgradX ) ) ] = 0

    iterationNumber = 0
    returnStatus = 0
    deltaPhiNorm = 0.0

    # compute initial Log likelyhood
    # p, _, _ = numpy.histogram2d(imF[crop].ravel(), imGdef[crop].ravel(), bins=BINS, range=[[0.0, BINS], [0.0, BINS]], normed=False, weights=None)
    # LL = 0.0
    # for v in p.ravel():
    #     if v:
    #         LL += numpy.log(v)
    # LL = numpy.prod(p[numpy.where(p > 0)])

    p, _, _ = numpy.histogram2d(imF[crop].ravel(), imG[crop].ravel(), bins=BINS, range=[[0.0, BINS], [0.0, BINS]], normed=False, weights=None)
    LL = numpy.sum(numpy.log(p[numpy.where(p > 0)]))

    if verbose:
        print("\tInitial state        LL = {:0.2f}".format(LL))
        print("\tIteration Number {:03d} ".format(iterationNumber), end="")
        print("LL = {:0.2f} ".format(LL), end="")
        print("dPhi = {:0.4f} ".format(deltaPhiNorm), end="")
        # print("\nPhi", Phi )
        # currentTransformation = deformationFunction.decomposePhi(Phi, PhiPoint=imFcentre)
        currentTransformation = deformationFunction.decomposePhi(Phi)
        print("Tr = {: .3f}, {: .3f}, {: .3f} ".format(*currentTransformation['t']), end="")
        print("Ro = {: .3f}, {: .3f}, {: .3f} ".format(*currentTransformation['r']), end="")
        print("Zo = {: .3f}, {: .3f}, {: .3f}".format(Phi[0,0], Phi[1,1], Phi[2,2]))

    while (iterationNumber <= maxIterations and deltaPhiNorm > minDeltaPhi) or iterationNumber == 0:
        previousLL = LL

        if verbose:
            print("\tIteration Number {:03d} ".format(iterationNumber+1), end="")

        # No recomputation of gradient
        M = numpy.zeros((12, 12), dtype='<f4')
        A = numpy.zeros((12),     dtype='<f4')

        # Use gradient of image 2 which does move
        imGdefGradZ, imGdefGradY, imGdefGradX = [g.astype('<f4') for g in numpy.gradient(imGdef)]

        DICToolkit.computeDICoperatorsGM(imF[crop],
                                         imGdef[crop],
                                         imGdefGradZ[crop],
                                         imGdefGradY[crop],
                                         imGdefGradX[crop],
                                         phaseDiagram, gaussianParameters, M, A)

        # tifffile.imsave( "imFdef-{}.tif".format( iterationNumber ), imFdef )
        try:
            deltaPhi = numpy.dot(numpy.linalg.inv(M), A)
        except numpy.linalg.linalg.LinAlgError:  # no cover
            singular = True
            # TODO: Calculate error for clean break.
            print('\tsingular M matrix')
            print('exiting')
            exit()
            # break

        deltaPhiNorm = numpy.linalg.norm(deltaPhi)

        # Add padding zeros
        deltaPhi = numpy.hstack([deltaPhi, numpy.zeros(4)]).reshape((4, 4))

        # In Roux X-N paper equation number 11
        Phi = numpy.dot((numpy.eye(4) - deltaPhi), Phi)
        # currentTransformation = deformationFunction.decomposePhi(Phi, PhiPoint=imFcentre)
        currentTransformation = deformationFunction.decomposePhi(Phi)

        # reset imGdef as emtpy matrix for deformed image
        PhiCentre = Phi.copy()
        PhiCentre[0:3, - 1] = currentTransformation["t"]
        # imGdef = deformationFunction.applyPhi(imG, Phi=PhiCentre, PhiPoint=imFcentre, interpolationOrder=interpolationOrder)
        imGdef = deformationFunction.applyPhi(imG, Phi=Phi, interpolationOrder=interpolationOrder)

        residualField = numpy.zeros_like(imG[crop], dtype="<f4")
        phaseField = numpy.zeros_like(imG[crop], dtype="<u1")

        DICToolkit.computeGMresidualAndPhase(imF[crop], imGdef[crop], phaseDiagram, gaussianParameters, residualField, phaseField)

        # compute current log likelyhood
        # p, _, _ = numpy.histogram2d(imF[crop].ravel(), imGdef[crop].ravel(), bins=BINS, range=[[0.0, BINS], [0.0, BINS]], normed=False, weights=None)
        # LL = 0.0
        # for v in p.ravel():
        #     if v:
        #         LL += numpy.log(v)
        p, _, _ = numpy.histogram2d(imF[crop].ravel(), imGdef[crop].ravel(), bins=BINS, range=[[0.0, BINS], [0.0, BINS]], normed=False, weights=None)
        LL = numpy.sum(numpy.log(p[numpy.where(p > 0)]))

        if verbose:
            print("LL = {:0.2f} ".format(LL), end="")
            print("dPhi = {:0.4f} ".format(deltaPhiNorm), end="")
            # print("\nPhi", Phi )
            print("Tr = {: .3f}, {: .3f}, {: .3f} ".format(*currentTransformation['t']), end="")
            print("Ro = {: .3f}, {: .3f}, {: .3f} ".format(*currentTransformation['r']), end="")
            print("Zo = {: .3f}, {: .3f}, {: .3f}".format(Phi[0,0], Phi[1,1], Phi[2,2]))

        if previousLL < LL*0.6:
            # undo this bad Phi which has increased the LL:
            Phi = numpy.dot((numpy.eye(4) + deltaPhi), Phi)
            returnStatus = -1
            print("Log-likelyhood increasing, divergence condition detected, exiting.")
            # break
            print("...no actually continuing...")

        if GRAPHS:
            NPHASES = gaussianParameters.shape[0]
            grid = plt.GridSpec(2, 4)
            plt.clf()
            plt.suptitle("Gaussian Mixture {} iteration number {} "
                         "|deltaPhi|={:.5f} \nT = [{: 2.4f} {: 2.4f} {:.4f}]\n"
                         "R = [{: 2.4f} {: 2.4f} {: 2.4f}]\n"
                         "Z = [{: 2.4f} {: 2.4f} {: 2.4f}]".format(suffix, iterationNumber, deltaPhiNorm,
                                                                   currentTransformation['t'][0],
                                                                   currentTransformation['t'][1],
                                                                   currentTransformation['t'][2],
                                                                   currentTransformation['r'][0],
                                                                   currentTransformation['r'][1],
                                                                   currentTransformation['r'][2],
                                                                   Phi[0,0], Phi[1,1], Phi[2,2]))

            plt.subplot(grid[0, 0])
            plt.axis('off')
            plt.title('Residual field')
            if sliceAxis == 0:
                plt.imshow(residualField[residualField.shape[0]/2, :, :])
            elif sliceAxis == 1:
                plt.imshow(residualField[:, residualField.shape[1]/2, :])
            elif sliceAxis == 2:
                plt.imshow(residualField[:, :, residualField.shape[2]/2])
            # plt.colorbar()

            plt.subplot(grid[0, 1])
            plt.axis('off')
            plt.title('Phase field')
            if sliceAxis == 0:
                plt.imshow(phaseField[phaseField.shape[0]/2, :, :], vmin=-0.5, vmax=NPHASES+0.5, cmap=mpl.cm.get_cmap(cmapPhases, NPHASES+1))
            elif sliceAxis == 1:
                plt.imshow(phaseField[:, phaseField.shape[1]/2, :], vmin=-0.5, vmax=NPHASES+0.5, cmap=mpl.cm.get_cmap(cmapPhases, NPHASES+1))
            elif sliceAxis == 2:
                plt.imshow(phaseField[:, :, phaseField.shape[2]/2], vmin=-0.5, vmax=NPHASES+0.5, cmap=mpl.cm.get_cmap(cmapPhases, NPHASES+1))
            # plt.colorbar(ticks=numpy.arange(0, NPHASES+1))

            plt.subplot(grid[1, 0])
            plt.axis('off')
            plt.title('imF')
            if sliceAxis == 0:
                plt.imshow(imF[crop][imF[crop].shape[0]/2, :, :])
            elif sliceAxis == 1:
                plt.imshow(imF[crop][:, imF[crop].shape[1]/2, :])
            elif sliceAxis == 2:
                plt.imshow(imF[crop][:, :, imF[crop].shape[2]/2])
            # plt.colorbar()

            plt.subplot(grid[1, 1])
            plt.axis('off')
            plt.title('imGdef')
            if sliceAxis == 0:
                plt.imshow(imGdef[crop][imGdef[crop].shape[0]/2, :, :])
            elif sliceAxis == 1:
                plt.imshow(imGdef[crop][:, imGdef[crop].shape[1]/2, :])
            elif sliceAxis == 2:
                plt.imshow(imGdef[crop][:, :, imGdef[crop].shape[2]/2])
            # plt.colorbar()

            plt.subplot(grid[:, 2:])
            plt.axis('off')
            plt.title('Checker Board')
            if sliceAxis == 0:
                plt.imshow(checkerBoard(imF[crop][imGdef[crop].shape[0]/2, :, :], imGdef[crop][imGdef[crop].shape[0]/2, :, :]))
            elif sliceAxis == 1:
                plt.imshow(checkerBoard(imF[crop][:, imGdef[crop].shape[1]/2, :], imGdef[crop][:, imGdef[crop].shape[1]/2, :]))
            elif sliceAxis == 2:
                plt.imshow(checkerBoard(imF[crop][:, :, imGdef[crop].shape[2]/2], imGdef[crop][:, :, imGdef[crop].shape[2]/2]))

            if INTERACTIVE:
                plt.show()
                plt.pause(1.0)
            else:
                plt.savefig('{}/GaussianMixture_Iteration-{}-{}.png'.format(rootPath, iterationNumber, suffix), dpi=600)

        iterationNumber += 1

    if INTERACTIVE:
        plt.ioff()
        plt.close()

    # Positive return status is a healthy end of while loop:
    if iterationNumber >= maxIterations:
        returnStatus = 1
    if deltaPhiNorm <= minDeltaPhi:
        returnStatus = 2
    if singular:
        returnStatus = -2

    # Create Phi appled at the centre of the image for returning
    # PhiCentre = Phi.copy()
    # PhiCentre[0:3, - 1] = deformationFunction.decomposePhi(Phi, PhiPoint=imFcentre)["t"]

    return {'transformation': currentTransformation,
            'Phi': Phi,
            # 'PhiCentre': PhiCentre,
            'returnStatus': returnStatus,
            'iterationNumber': iterationNumber,
            'residualField': residualField,
            'phaseField': phaseField}


################################################################
# helper functions for correlation with different modalities
################################################################

def gaussianMixtureParameters(imF, imG, BINS=64, NPHASES=2, imFthreshold=0, imGthreshold=0, distanceMaxima=None, fitDistance=None,
                              GRAPHS=False, INTERACTIVE=False, sliceAxis=0, rootPath=".", suffix=""):
    """
    To comment
    """

    # To fit 2D likelyhood with gaussian ellipsoids
    from scipy.optimize import curve_fit

    # To find maxima in likelyhood which correspond to phases
    import skimage.feature

    # for interactive graphs
    if INTERACTIVE:
        GRAPHS = True
        plt.ion()

    # DEFINE the global variables needed for curve fitting
    GLOBALmuF = 0.0  # mean of the f image
    GLOBALmuG = 0.0  # mean of the g image
    GLOBALphi = 0.0  # number of hits (value of the maxima)

    # DEFINE fitting functions
    # https://en.wikipedia.org/wiki/Gaussian_function#Two-dimensional_Gaussian_function
    # def gaussian2Delliptical( XY, GLOBALphi, GLOBALmuG, GLOBALmuF, a, b, c ):
    # Thsi needs to be in here in order to pass GLOBALphi as a global variable.
    # Perhaps it should be optimised?
    def computeLambda(a, b, c, x, GLOBALmuF, y, GLOBALmuG):
        return numpy.longfloat(0.5*(a*(x - GLOBALmuF)**2 + 2.0*b*(x - GLOBALmuF)*(y - GLOBALmuG) + c*(y - GLOBALmuG)**2))

    def gaussian2Delliptical(XY, a, b, c):
        # invert x and y on purpose to be consistent with H
        grid = numpy.array(numpy.meshgrid(XY[1], XY[0]))
        field = numpy.zeros(grid.shape[1:3])
        for ny in range(grid.shape[2]):
            y = grid[0, 0, ny]
            for nx in range(grid.shape[1]):
                x = grid[1, nx, 0]
                field[nx, ny] = float(GLOBALphi) * numpy.exp(-computeLambda(a, b, c, x, GLOBALmuF, y, GLOBALmuG))
        return field.ravel()

    # START function

    imFmin = imF.min()
    imFmax = imF.max()
    imGmin = imG.min()
    imGmax = imG.max()

    # f,g discretisation
    X = numpy.linspace(0, BINS-1, BINS)
    Y = numpy.linspace(0, BINS-1, BINS)

    print("\tf from {:.2f} to {:.2f}".format(imFmin, imFmax))
    print("\tg from {:.2f} to {:.2f}".format(imGmin, imGmax))

    # Calculate probability distribution p(f,g)
    p, _, _ = numpy.histogram2d(imF.ravel(), imG.ravel(), bins=BINS, range=[[0.0, BINS], [0.0, BINS]], normed=False, weights=None)
    p /= float(len(imF.ravel()))
    p_sum = p.sum()

    print("\tp normalisation: {:.2f}".format(p_sum))

    # write joint histogram in a dat file for tikz
    # if DATA:
    #     tmp = p.copy()
    #     with open("GaussianMixture_jointHistogram-{}-{}.dat".format(0, suffix), "w") as f:
    #         string = "{}\t {}\t {}\n".format("x", "y", "c")
    #         f.write(string)
    #         for xbin in range(tmp.shape[0]):
    #             x = (xbin+0.5)/tmp.shape[0]
    #             for ybin in range(tmp.shape[1]):
    #                 y = (ybin+0.5)/tmp.shape[1]
    #                 if tmp[xbin, ybin]:
    #                     string = "{}\t {}\t {}\n".format(x, y, tmp[xbin, ybin])
    #                     f.write(string)

    # Get disordered maxima of the joint histogram
    print("\tFind maxima")
    if distanceMaxima is None:
        distanceMaxima = int(BINS/25.0)
    print("\t\tMin distance between maxima: {:.0f}".format(distanceMaxima))
    maxima = skimage.feature.peak_local_max(p, min_distance=int(distanceMaxima))
    nMax = len(maxima)

    if(nMax < NPHASES):
        print("\t\t{} phases asked but only {} maxima...".format(NPHASES, nMax))
    NPHASES = min(NPHASES, nMax)

    # print "\t\t Number of maxima: {:2}".format(nMax)
    if nMax == 0: # no cover
        print("In gaussian fit: no maxium found... Stoping...")
        exit()

    # Organise maxima into muF, muG, p(f,g) the sort at take the maximum
    maxTmp = numpy.zeros((nMax, 3))
    for i, (f, g) in enumerate(maxima):
        if f > imFthreshold or g > imGthreshold:
            maxTmp[i] = [f, g, p[f, g]]
        # print("\t\t max {:2} --- f: {:.2f}   g: {:.2f}   hits: {}".format(i+1,*maxTmp[i]))

    nMax = 0
    percentage = 0.1
    while nMax < NPHASES:
        maxSorted = [m for m in maxTmp[maxTmp[:, 2].argsort()[::-1]] if float(m[2]) > percentage*float(p_sum)]
        nMax = len(maxSorted)
        print("\t\t{:02d} maxima found over the {} needed with {:.2e} times of the total count".format(nMax, NPHASES, percentage))
        percentage /= 10.0

    for i, (GLOBALmuF, GLOBALmuG, GLOBALphi) in enumerate(maxSorted):
        print("\t\tMaximum {}:\t muF={:.2f}\t muG={:.2f}\t Phi={:.2e}".format(i+1, GLOBALmuF, GLOBALmuG, GLOBALphi))
    print("")

    # output of the function: list of fitting gaussian parameters
    # size NPHASES x 6, the 6 parameters being GLOBALlogPhi, GLOBALmuF, GLOBALmuG, a, b, c
    gaussianParameters = numpy.zeros((NPHASES, 6)).astype('<f4')

    # loop over phases
    maxEllipsoid = numpy.zeros_like(p)
    for iPhase in range(NPHASES):
        GLOBALmuF, GLOBALmuG, GLOBALphi = maxSorted[iPhase]
        print("\tPhase {:2}:\t\t muF={:.2f}\t muG={:.2f}\t Phi={:.2e}".format(iPhase+1, GLOBALmuF, GLOBALmuG, GLOBALphi))
        if fitDistance is None:
            fitDistance = BINS/2.0

        # fit the probability distribution p(f,g) with an gaussian ellipsoids
        pFit = p.copy()

        for nf in range(pFit.shape[0]):
            for ng in range(pFit.shape[1]):
                posF = nf
                posG = ng
                dist = numpy.sqrt((posF-GLOBALmuF)**2.0 + (posG-GLOBALmuG)**2.0)  # cicrle
                # dist = abs(posF-GLOBALmuF)+abs(posG-GLOBALmuG) # square
                if dist > fitDistance:
                    pFit[nf, ng] = 0.0

        (a, b, c), _ = curve_fit(gaussian2Delliptical, (X, Y), pFit.ravel(), p0=(1, 1, 1))
        print("\t\tFit:\t\t a={:.2f}\t b={:.2f}\t c={:.2f}\t Hessian: {:.2f}".format(a, b, c, a*c-b**2))
        while a*c-b**2 < 0:
            print("\t\t\tWarning: Hessian < 0")
            print("\t\t\t         The gaussian doesn't have a local maximum.")
            fitDistance /= 2.0
            print("\t\t\t         Try with fit distance = {} ".format(fitDistance))

            for nf in range(pFit.shape[0]):
                for ng in range(pFit.shape[1]):
                    posF = nf/float(pFit.shape[0]-1)
                    posG = ng/float(pFit.shape[1]-1)
                    dist = numpy.sqrt((posF-GLOBALmuF)**2.0 + (posG-GLOBALmuG)**2.0)  # cicrle
                    # dist = abs(posF-GLOBALmuF)+abs(posG-GLOBALmuG) # square
                    if dist > fitDistance:
                        pFit[nf, ng] = 0.0

            (a, b, c), _ = curve_fit(gaussian2Delliptical, (X, Y), pFit.ravel(), p0=(1, 1, 1))
            print("\t\tFit:\t\t a={:.2f}\t b={:.2f}\t c={:.2f}\t Hessian: {:.2f}".format(a, b, c, a*c-b**2))

        # compute covariance function
        cov = scipy.linalg.inv(numpy.array([[a, b], [b, c]]))
        print("\t\tCov:\t\t ff={:.4f}\t fg={:.4f}\t gg={:.4f}".format(cov[0, 0], cov[1, 0], cov[1, 1]))

        gaussianParameters[iPhase, 0] = GLOBALphi
        gaussianParameters[iPhase, 1] = GLOBALmuF
        gaussianParameters[iPhase, 2] = GLOBALmuG
        gaussianParameters[iPhase, 3] = a
        gaussianParameters[iPhase, 4] = b
        gaussianParameters[iPhase, 5] = c

        currentEllipsoid = gaussian2Delliptical((X, Y), a, b, c).reshape((len(X), len(Y)))

        maxEllipsoid = numpy.maximum(maxEllipsoid, currentEllipsoid)

        if GRAPHS:
            plt.clf()
            plt.suptitle("Gaussian Mixture fitting Phase number {}".format(iPhase+1))
            plt.subplot(221)
            plt.title("imF (from {:.2f} to {:.2f})".format(imF.min(), imF.max()))
            plt.axis('off')
            if sliceAxis == 0:
                plt.imshow(imF[imF.shape[0]/2, :, :], vmin=0.0, vmax=BINS)
            elif sliceAxis == 1:
                plt.imshow(imF[:, imF.shape[1]/2, :], vmin=0.0, vmax=BINS)
            elif sliceAxis == 2:
                plt.imshow(imF[:, :, imF.shape[2]/2], vmin=0.0, vmax=BINS)
            plt.colorbar()

            plt.subplot(222)
            plt.title("imG (from {:.2f} to {:.2f})".format(imG.min(), imG.max()))
            plt.axis('off')
            if sliceAxis == 0:
                plt.imshow(imG[imG.shape[0]/2, :, :], vmin=0.0, vmax=BINS)
            elif sliceAxis == 1:
                plt.imshow(imG[:, imG.shape[1]/2, :], vmin=0.0, vmax=BINS)
            elif sliceAxis == 2:
                plt.imshow(imG[:, :, imG.shape[2]/2], vmin=0.0, vmax=BINS)
            plt.colorbar()

            plt.subplot(223)
            tmp = p.copy()
            tmp[p <= 0] = numpy.nan
            tmp = numpy.log(tmp)
            plt.title("Log Probability log(p(f,g))")
            plt.imshow(tmp.T, origin='low', extent=[0.0, BINS, 0.0, BINS])
            for gp in maxSorted:
                plt.plot(gp[0], gp[1], 'b*')
            plt.plot(GLOBALmuF, GLOBALmuG, 'r*')
            fig = plt.gcf()
            ax = fig.gca()
            ax.add_artist(plt.Circle((GLOBALmuF, GLOBALmuG), fitDistance, color='r', fill=False))
            plt.xlabel("f")
            plt.ylabel("g")
            plt.colorbar()

            plt.subplot(224)
            tmp = currentEllipsoid.copy()
            tmp[currentEllipsoid <= 0] = numpy.nan
            tmp = numpy.log(tmp)
            plt.title("Gaussian ellipsoid")
            plt.imshow(tmp.T, origin='low', extent=[0.0, BINS, 0.0, BINS])
            plt.plot(GLOBALmuF, GLOBALmuG, 'r*')
            plt.xlabel("f")
            plt.ylabel("g")
            plt.colorbar()

            if INTERACTIVE:
                plt.show()
                plt.pause(1.0)
            else:
                plt.savefig('{}/GaussianMixture_jointHistogram-{}-{}.png'.format(rootPath, iPhase+1, suffix), dpi=600)

        # p -= currentEllipsoid

        # if DATA:  # write joint histogram in a dat file for tikz
        #     tmp = p.copy()
        #     # tmp_sum = tmp.sum()
        #     with open("GaussianMixture_jointHistogram-{}-{}.dat".format(iPhase+1, suffix), "w") as f:
        #         string = "{}\t {}\t {}\n".format("x", "y", "c")
        #         f.write(string)
        #         for xbin in range(tmp.shape[0]):
        #             x = (xbin+0.5)/tmp.shape[0]
        #             for ybin in range(tmp.shape[1]):
        #                 y = (ybin+0.5)/tmp.shape[1]
        #                 if tmp[xbin, ybin]:
        #                     string = "{}\t {}\t {}\n".format(x, y, float(tmp[xbin, ybin]))
        #                     f.write(string)

        print("")  # end of phase loop

    if INTERACTIVE:
        plt.ioff()
        plt.close()

    # write phase histogram in a dat file for tikz
    # if DATA:
    #     print("\tSave phase repartition")
    #     levels = [10**float(e) for e in numpy.arange(-8,0) ]
    #
    #     contour
    #     plt.clf()
    #     tmp = maxEllipsoid.copy()
    #     plt.title("Maximum gaussian ellispoid")
    #     X = numpy.linspace(0, 1, BINS)
    #     Y = numpy.linspace(0, 1, BINS)
    #     CS = plt.contour(X, Y, tmp.T,  levels=levels)
    #     for gp in maxSorted:
    #     plt.plot(gp[0], gp[1], 'b*')
    #     plt.xlabel("f")
    #     plt.ylabel("g")
    #     plt.colorbar()
    #     plt.savefig('GaussianMixture_phaseContour-{}.png'.format(suffix), dpi=600)

    return gaussianParameters, p


def phaseDiagram(gaussianParameters, jointHistogram, voxelCoverage=None, sigmaMax=9, BINS=64, GRAPHS=False, INTERACTIVE=False, suffix="", rootPath="."):

    if INTERACTIVE:
        GRAPHS = True
        plt.ion()

    def distanceMax(gaussianParameter):
        phi, muf, mug, a, b, c = gaussianParameter
        return (a*(x-muf)**2+2.0*b*(x-muf)*(y-mug)+c*(y-mug)**2)-numpy.log(phi)

    def distanceMahalanobis(gaussianParameter):
        phi, muf, mug, a, b, c = gaussianParameter
        return numpy.sqrt((a*(x-muf)**2+2.0*b*(x-muf)*(y-mug)+c*(y-mug)**2))

    if voxelCoverage == 1.0 or voxelCoverage is None:
        coverage = 1.0
        phase = numpy.zeros((BINS, BINS), dtype='<u1')
        # define corresponding level
        for xbin in range(BINS):
            x = (xbin+0.5)
            for ybin in range(BINS):
                y = (ybin+0.5)
                distances = numpy.array([distanceMax(gp) for gp in gaussianParameters])
                i = numpy.argmin(distances)
                distanceMin = distances[i]
                phase[xbin, ybin] = i+1
        print("\tVoxel coverage = 100 %")

        if GRAPHS:
            NPHASES = len(gaussianParameters)
            plt.clf()
            plt.title("Phase diagram: voxel coverage = 100%")
            plt.imshow(phase.T, origin='low', extent=[0.0, BINS, 0.0, BINS], vmin=-0.5, vmax=NPHASES+0.5, cmap=mpl.cm.get_cmap(cmapPhases, NPHASES+1))
            plt.colorbar(ticks=numpy.arange(0, NPHASES+1))
            for gp in gaussianParameters:
                plt.plot(gp[1], gp[2], 'b*')
            plt.xlabel("f")
            plt.ylabel("g")

            if INTERACTIVE:
                plt.show()
                plt.pause(1.0)

    else:
        sigma = numpy.arange(1, sigmaMax+1, 1)[::-1]

        # phases = numpy.zeros((len(sigma), BINS, BINS), dtype='<u1')
        for n, sig in enumerate(sigma):
            phase = numpy.zeros((BINS, BINS), dtype='<u1')
            # define corresponding level
            for xbin in range(BINS):
                x = (xbin+0.5)
                for ybin in range(BINS):
                    y = (ybin+0.5)
                    distancesMax = numpy.array([distanceMax(gp) for gp in gaussianParameters])
                    distancesMah = numpy.array([distanceMahalanobis(gp) for gp in gaussianParameters])
                    i = numpy.argmin(distancesMax)
                    distanceMin = distancesMah[i]

                    if distanceMin < sig:
                        # phases[n, xbin, ybin] = i+1
                        phase[xbin, ybin] = i+1

            coverage = jointHistogram[phase > 0].sum()

            if GRAPHS:
                NPHASES = len(gaussianParameters)
                plt.clf()
                plt.title("Phase diagram for {:.0f}-sigma: voxel coverage = {:.2f}%".format(sig, 100*coverage))
                plt.imshow(phase.T, origin='low', extent=[0.0, BINS, 0.0, BINS], vmin=-0.5, vmax=NPHASES+0.5, cmap=mpl.cm.get_cmap(cmapPhases, NPHASES+1))
                plt.colorbar(ticks=numpy.arange(0, NPHASES+1))
                for gp in gaussianParameters:
                    plt.plot(gp[1], gp[2], 'b*')
                plt.xlabel("f")
                plt.ylabel("g")

                if INTERACTIVE:
                    plt.show()
                    plt.pause(1.0)
                else:
                    plt.savefig('{}/GaussianMixture_phaseDiagram-{:.0f}sig-{}.png'.format(rootPath, sig, suffix), dpi=600)

            print("\t{:.0f}-sigma: voxel coverage = {:.2f}".format(sig, 100*coverage), end="")
            if coverage > voxelCoverage:
                print(" (> {:.2f}%)".format(100*voxelCoverage))
            else:
                print(" (< {:.2f}%) -> Returning this phase diagram.".format(100*voxelCoverage))
                break

    if GRAPHS and not INTERACTIVE:
        plt.savefig('{}/GaussianMixture_phaseDiagram-{}.png'.format(rootPath, suffix), dpi=600)

    if INTERACTIVE:
        plt.ioff()
        plt.close()

    # phase diagram for different levels
    # for n, sig in enumerate(sigma):
    #     plt.clf()
    #     tmp = phases[n].astype('<f4')
    #     tmp[tmp == 0] = numpy.nan
    #     plt.title("Phases repartition for sigma {}".format(sigma))
    #     plt.imshow(tmp.T, origin='low', extent=[0.0, 1.0, 0.0, 1.0], vmin=-0.5, vmax=NPHASES+0.5, cmap=mpl.cm.get_cmap(cmapPhases, NPHASES+1))
        # plt.colorbar(ticks=numpy.arange(0, NPHASES+1))
    #     for gp in gaussianParameters:
    #         plt.plot(gp[1], gp[2], 'b*')
    #     plt.xlabel("f")
    #     plt.ylabel("g")
    #     plt.savefig('GaussianMixture_phaseDiagram-level{:02d}-{}.png'.format(n, suffix), dpi=600)

    # import spam.helpers
    # spam.helpers.writeStructuredVTK(cellData={"phases": phases},
    #                aspectRatio=(1.0, 1.0, 1.0), fileName="GaussianMixture_phaseDiagram-{}.vtk".format(suffix))
    # tifffile.imsave("{}/GaussianMixture_phaseDiagram-{}.tif".format(rootPath, suffix), phase)

    return phase, coverage


def checkerBoard(imF, imG, n=5, inv=False, rescale=True):
    """ To be commented
    """
    if inv:
        c = -1.0
    else:
        c = 1.0

    if rescale:
        import spam.helpers
        imF = spam.helpers.rescale(imF)
        imG = spam.helpers.rescale(imG)

    # 2D version
    if len(imF.shape) == 2:
        # initialize
        imFG = imF.copy()

        # get number of pixel / square based on min size
        nP = int(min(imF.shape)/n)

        for x in range(imF.shape[0]):
            for y in range(imF.shape[1]):
                if (x % (2*nP))/nP + (y % (2*nP))/nP - 1:
                    imFG[x, y] = c*imG[x, y]
    else:
        print("checkerBoard works only with dim2 images")
        return 0

    return imFG

# if __name__ == "__main__":
#     import spam.datasets as data
#
#     xr = data.loadConcreteXr()[:, 10:50, 50]
#     ne = data.loadConcreteNe()[:, :, 50]
#
#     plt.imshow(checkerBoard(xr, ne, n=7))
#     plt.show()
