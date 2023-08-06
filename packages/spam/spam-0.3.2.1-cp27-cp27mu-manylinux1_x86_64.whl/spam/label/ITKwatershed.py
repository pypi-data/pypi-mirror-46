from __future__ import print_function
import numpy
import tifffile
import sys
import os
import SimpleITK


if sys.version_info >= (3, 0):
    def xrange(*args, **kwargs):
        return iter(range(*args, **kwargs))
"""
    Classes binding ITK morphological watershed algorithm implementation

    Note:
    Author is Olumide Okubadejo
"""


class _Label(object):
    def __init__(self, number):
        self._number = number

    def setBoundingBox(self, bb):
        self._bbox = bb

    def getBoundingBox(self):
        return self._bbox

    def setVariance(self, var):
        self._var = var

    def getVariance(self):
        return self._var

    def setSigma(self, sig):
        self._sig = sig

    def getSigma(self):
        return self._sig

    def setIntensitySum(self, isum):
        self._isum = isum

    def getIntensitySum(self):
        return self._isum

    def setIntensityMin(self, imin):
        self._imin = imin

    def getIntensityMin(self):
        return self._imin

    def setIntensityMax(self, imax):
        self._imax = imax

    def getIntensityMax(self):
        return self._imax

    def setIntensityMed(self, imed):
        self._imed = imed

    def getIntensityMed(self):
        return self._imed

    def setCount(self, count):
        self._c = count

    def getCount(self):
        return self._c

    def setPerimeter(self, perimeter):
        self._p = perimeter

    def getPerimeter(self):
        return self._p

    def setRoundness(self, roundness):
        self._r = roundness

    def getRoundness(self):
        return self._r

    def setFlatness(self, flatness):
        self._f = flatness

    def getFlatness(self):
        return self._f

    def setElongation(self, elongation):
        self._e = elongation

    def getElongation(self):
        return self._e

    def setCentroid(self, centroid):
        self._cen = centroid

    def getCentroid(self):
        return self._cen

    def setFeretDiameter(self, fdiameter):
        self._fd = fdiameter

    def getFeretDiameter(self):
        return self._fd

    def setBorderPixels(self, bpixels):
        self._bp = bpixels

    def getBorderPixels(self):
        return self._bp

    def setPhysicalSize(self, psize):
        self._ps = psize

    def getPhysicalSize(self):
        return self._ps

    def setPrincipalAxes(self, paxis):
        self._pa = paxis

    def getPrincipalAxes(self):
        return self._pa

    def setPrincipalMoments(self, pmoments):
        self._pm = pmoments

    def getPrincipalMoments(self):
        return self._pm

    def setEllipsoidalDiameter(self, ediameter):
        self._ed = ediameter

    def getEllipsoidalDiameter(self):
        return self._ed

    def setSphericalPerimeter(self, sperimeter):
        self._sp = sperimeter

    def getSphericalPerimeter(self):
        return self._sp

    def setSphericalRadius(self, srad):
        self._sr = srad

    def getSphericalRadius(self):
        return self._sr

    def getGrayValue(self):
        return self._number

    boundingBox = property(lambda self: self._bbox)
    variance = property(lambda self: self._var)
    sigma = property(lambda self: self._sig)
    intensitySum = property(lambda self: self._isum)
    intensityMax = property(lambda self: self._imax)
    intensityMin = property(lambda self: self._imin)
    intensityMed = property(lambda self: self._imed)
    count = property(lambda self: self._c)
    perimeter = property(lambda self: self._p)
    roundness = property(lambda self: self._r)
    flatness = property(lambda self: self._f)
    elongation = property(lambda self: self._e)
    centroid = property(lambda self: self._cen)

    feretDiameter = property(lambda self: self._fd)
    borderPixels = property(lambda self: self._bp)
    physicalSize = property(lambda self: self._ps)
    principalAxis = property(lambda self: self._pa)
    principalMom = property(lambda self: self._pm)
    elipsoidDiameter = property(lambda self: self._ed)
    sphericalPerimeter = property(lambda self: self._sp)
    sphericalRadius = property(lambda self: self._sr)


def _convertPropertyToList(labels, labelFunctionString):
    variableList = []
    for label in labels:
        variableList.append(getattr(label, labelFunctionString)())
    return numpy.asarray(variableList)


class _Labels(object):
    def __init__(self, image, labelsImage):
        self._image = image
        self._limage = labelsImage
        self._labellist = list()
        self._generateProperties()

    def GetLabels(self):
        return self._labellist

    def _generateProperties(self):
        #itklimage = SimpleITK.GetImageFromArray(self._limage)
        shapestat = SimpleITK.LabelShapeStatisticsImageFilter()
        normstat = SimpleITK.LabelStatisticsImageFilter()

        shaperes = shapestat.Execute(self._limage)
        normres = normstat.Execute(self._image, self._limage)

        for i in xrange(1, normstat.GetNumberOfLabels()+1):
            label = _Label(i)
            label.setBoundingBox(normstat.GetBoundingBox(i))
            label.setVariance(normstat.GetVariance(i))
            label.setSigma(normstat.GetSigma(i))
            label.setIntensitySum(normstat.GetSum(i))
            label.setIntensityMax(normstat.GetMaximum(i))
            label.setIntensityMin(normstat.GetMinimum(i))
            label.setIntensityMed(normstat.GetMedian(i))
            label.setCount(normstat.GetCount(i))
            label.setFeretDiameter(shapestat.GetFeretDiameter(i))
            label.setBorderPixels(shapestat.GetNumberOfPixelsOnBorder(i))
            label.setPerimeter(shapestat.GetPerimeter(i))
            label.setPhysicalSize(shapestat.GetPhysicalSize(i))
            label.setPrincipalAxes(shapestat.GetPrincipalAxes(i))
            label.setPrincipalMoments(shapestat.GetPrincipalMoments(i))
            label.setRoundness(shapestat.GetRoundness(i))
            label.setFlatness(shapestat.GetFlatness(i))
            label.setEllipsoidalDiameter(
                shapestat.GetEquivalentEllipsoidDiameter(i))
            label.setSphericalPerimeter(
                shapestat.GetEquivalentSphericalPerimeter(i))
            label.setSphericalRadius(shapestat.GetEquivalentSphericalRadius(i))
            label.setElongation(shapestat.GetElongation(i))
            label.setCentroid(shapestat.GetCentroid(i))
            self._labellist.append(label)
        # self._obtainRadiusParams()

    def _assignBinPos(self, radius):
        for index in xrange(len(self._binAxisArray)):
            if radius >= self._binAxisArray[index]:
                return index

    def GetSphericalRadiusArray(self):
        self._radiusArray = getattr(self, "_radiusArray", _convertPropertyToList(
            self._labellist, "getSphericalRadius"))
        self._maxRadius = numpy.max(self._radiusArray)
        return self._radiusArray

    def GetCentroidArray(self):
        self._centroidArray = getattr(
            self, "_centroidArray", _convertPropertyToList(self._labellist, "getCentroid"))
        return self._centroidArray

    def GetElongationArray(self):
        self._elongationArray = getattr(
            self, "_elongationArray", _convertPropertyToList(self._labellist, "getElongation"))
        return self._elongationArray

    def GetSphericalPerimeterArray(self):
        self._sphericalPerimeterArray = getattr(
            self, "_sphericalPerimeterArray", _convertPropertyToList(self._labellist, "getSphericalPerimeter"))
        return self._sphericalPerimeterArray

    def GetEllipsoidalDiameterArray(self):
        self._ellipsoidalDiameterArray = getattr(
            self, "_ellipsoidalDiameterArray", _convertPropertyToList(self._labellist, "getEllipsoidalDiameter"))
        return self._ellipsoidalDiameterArray

    def GetFlatnessArray(self):
        self._flatnessArray = getattr(
            self, "_flatnessArray", _convertPropertyToList(self._labellist, "getFlatness"))
        return self._flatnessArray

    def GetRoundnessArray(self):
        self._roundnessArray = getattr(
            self, "_roundnessArray", _convertPropertyToList(self._labellist, "getRoundness"))
        return self._roundnessArray

    def GetPrincipalMomentsArray(self):
        self._principalMomentsArray = getattr(
            self, "_principalMomentsArray", _convertPropertyToList(self._labellist, "getPrincipalMoments"))
        return self._principalMomentsArray

    def GetPrincipalAxesArray(self):
        self._principalAxesArray = getattr(
            self, "_principalAxesArray", _convertPropertyToList(self._labellist, "getPrincipalAxes"))
        return self._principalAxesArray

    def GetPhysicalSizeArray(self):
        self._physicalSizeArray = getattr(
            self, "_physicalSizeArray", _convertPropertyToList(self._labellist, "getPhysicalSize"))
        return self._physicalSizeArray

    def GetPerimeterArray(self):
        self._perimeterArray = getattr(
            self, "_perimeterArray", _convertPropertyToList(self._labellist, "getPerimeter"))
        return self._perimeterArray

    def GetBorderPixelsArray(self):
        self._borderPixelsArray = getattr(
            self, "_borderPixelsArray", _convertPropertyToList(self._labellist, "getBorderPixels"))
        return self._borderPixelsArray

    def GetFeretDiameterArray(self):
        self._feretDiameterArray = getattr(
            self, "_feretDiameterArray", _convertPropertyToList(self._labellist, "getFeretDiameter"))
        return self._feretDiameterArray

    def GetCountArray(self):
        self._countArray = getattr(
            self, "_countArray", _convertPropertyToList(self._labellist, "getCount"))
        return self._countArray

    def GetSigmaArray(self):
        self._sigmaArray = getattr(
            self, "_sigmaArray", _convertPropertyToList(self._labellist, "getSigma"))
        return self._sigmaArray

    def GetIntensityMin(self):
        self._intensityMinArray = getattr(
            self, "_intensityMinArray", _convertPropertyToList(self._labellist, "getIntensityMin"))
        return self._intensityMinArray

    def GetIntensityMed(self):
        self._intensityMedArray = getattr(
            self, "_intensityMedArray", _convertPropertyToList(self._labellist, "getIntensityMed"))
        return self._intensityMedArray

    def GetIntensityMax(self):
        self._intensityMaxArray = getattr(
            self, "_intensityMaxArray", _convertPropertyToList(self._labellist, "getIntensityMax"))
        return self._intensityMaxArray

    def GetIntensitySum(self):
        self._intensitySumArray = getattr(
            self, "_intensitySumArray", _convertPropertyToList(self._labellist, "getIntensitySum"))
        return self._intensitySumArray

    def GetVarianceArray(self):
        self._varianceArray = getattr(
            self, "_varianceArray", _convertPropertyToList(self._labellist, "getVariance"))
        return self._varianceArray

    def GetBoundingBoxArray(self):
        self._boundingBoxArray = getattr(
            self, "_boundingBoxArray", _convertPropertyToList(self._labellist, "getBoundingBox"))
        return self._boundingBoxArray


class _MWatershed(object):

    def __init__(self, data, level=1, watershedLineOn=False, fullyConnected=True, fromMarkers=False, markerImage=None):
        self._level = level
        self._watershedLineOn = watershedLineOn
        self._fullyConnected = fullyConnected
        self._data = SimpleITK.GetImageFromArray(data)
        self._fromMarkers = fromMarkers
        if fromMarkers:
            self._markerImage = SimpleITK.GetImageFromArray(markerImage)

    def _CalculateGradient(self):

        gradient = SimpleITK.GradientMagnitudeImageFilter()
        self._gradient = gradient.Execute(self._bdata)

    def _Binarize(self):
        threshold = SimpleITK.OtsuThresholdImageFilter()
        self._bdata = threshold.Execute(self._data)
        self._bdata = self._Rescale(self._bdata)
        self._threshold = threshold.GetThreshold()

    def _Rescale(self, data):
        rescale = SimpleITK.RescaleIntensityImageFilter()
        return rescale.Execute(data, 0, 65535)

    def _DistanceMap(self):
        distanceMap = SimpleITK.DanielssonDistanceMapImageFilter()
        self._distance = distanceMap.Execute(self._bdata)
        pass

    def _InvertImage(self, data):
        invert = SimpleITK.InvertIntensityImageFilter()
        inverted = invert.Execute(data)
        return inverted

    def _MaskImage(self):
        mask = SimpleITK.MaskImageFilter()
        self._mask = mask.Execute(self._labelImage, self._bdata)

    def _FillHoles(self):
        fill = SimpleITK.BinaryFillholeImageFilter()
        self._bdata = fill.Execute(self._bdata)

    def _LabelOverlay(self):
        overlay = SimpleITK.LabelOverlayImageFilter()
        self._overlay = overlay.Execute(self._bdata, self._mask)

    def _Watershed(self):
        if (self._fromMarkers):
            watershed = SimpleITK.MorphologicalWatershedFromMarkersImageFilter()
        else:
            watershed = SimpleITK.MorphologicalWatershedImageFilter()
        watershed.SetFullyConnected(self._fullyConnected)
        watershed.SetMarkWatershedLine(self._watershedLineOn)

        if (self._fromMarkers):
            self._labelImage = watershed.Execute(
                self._distance, self._markerImage)
        else:
            watershed.SetLevel(self._level)
            self._labelImage = watershed.Execute(self._distance)

    def GetThreshold(self):
        return self._threshold

    def GetLabeledImage(self):
        return SimpleITK.GetArrayFromImage(self._mask)

    def GetITKLabeledImage(self):
        return self._labelImage

    def GetColorMap(self):
        return SimpleITK.GetArrayFromImage(self._overlay)

    def GetBinaryImage(self):
        return SimpleITK.GetArrayFromImage(self._bdata)

    def GetDistanceMapImage(self):
        return SimpleITK.GetArrayFromImage(self._distance)

    def GetMaskImage(self):
        return SimpleITK.GetArrayFromImage(self._mask)

    def GetLabelParams(self):
        return self._labelParams.GetLabels()

    def GetLabelObject(self):
        return self._labelParams

    def GetRadiusArray(self):
        return self._labelParams.GetRadiusArray()

    def run(self):
        self._Binarize()
        #self._bdata = self._InvertImage(self._bdata)
        self._FillHoles()
        self._DistanceMap()
        self._distance = self._InvertImage(self._distance)
        self._Watershed()
        self._bdata = self._InvertImage(self._bdata)
        self._MaskImage()
        self._LabelOverlay()
        self._labelParams = _Labels(self._data, self._labelImage)
        return SimpleITK.GetArrayFromImage(self._overlay)


def watershed(binary, markers=None):
    """
        This function runs an ITK watershed on a binary image and returns a labelled image.
        This function uses an interpixel watershed.

        Parameters
        -----------
        binary : 3D numpy array
            This image which is non-zero in the areas which should be split by the watershed algorithm

        markers : 3D numpy array (optional, default = None)
            Not implemented yet, but try!

        Returns
        --------
        labelled : 3D numpy array of ints
            3D array where each object is numbered
    """
    binary = binary > 0

    # Let's convert it 8-bit
    binary = binary.astype('<u1')*255

    if markers is not None:
        print("\tITKwatershed.watershed(): Running watershed with your markers...", end='')
        mWatershed = _MWatershed(binary, markerImage=markers, fromMarkers=True,
                                 level=1, watershedLineOn=False, fullyConnected=True)
    else:
        print("\tITKwatershed.watershed(): Running watershed...", end='')
        mWatershed = _MWatershed(
            binary, level=1, watershedLineOn=False, fullyConnected=True)
    labels = mWatershed.run()
    print("done.")

    print("\tITKwatershed.watershed(): Collecting labelled image...", end='')
    lab = mWatershed.GetMaskImage().astype('<u4')
    print("done.")

    return lab


if (__name__ == "__main__"):
    import tifffile

    fileName = sys.argv[1]
    markerVol = None

    print("-> Loading binary image...", end='')
    binVol = tifffile.imread(fileName)
    if len(sys.argv) == 3:
        # load markers
        markerVol = tifffile.imread(sys.argv[2])
    print("done.")

    lab = watershed(binVol, markerVol)

    print("-> Saving labelled image...", end='')
    tifffile.imsave(fileName[0:-4]+'-watershed.tif', lab)
    print("done.")
