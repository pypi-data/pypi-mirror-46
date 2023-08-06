import tifffile
import numpy
import spam.measurements.measurementsToolkit as mtk
import spam.DIC.grid as grid
import matplotlib.pyplot as plt


def run(image, nodeSpacing="auto", hws=10, showGraph=False):
    """
    This function calculates a porosity field taking in an 8-bit image
    where solids (0% porosity) are set to zero,
    Pores (100% porosity) are set to 100,
    and the outside of the sample is set to 255.

    Parameters
    ----------
    images : 3D numpy array, 8 bit

    nodeSpacing : int (optional)
        spacing of nodes in pixels

    hws : int or list (optional, default = 10
        half-window size for cubic measurement window

    showGraph : bool (optional, default = False)
        If a list of hws is input, show a graph of the porosity evolution

    Returns
    -------
    3D (or 4D) numpy array for constant half-window size (list of half-window sizes)

    """

    if nodeSpacing == "auto":
        nodeSpacing = min(image.shape)/2
    #if hws == "auto":           10
    if type(hws) == int:
        hws = [hws]

    points, layout = grid.makeGrid(image.shape, nodeSpacing)

    #print points
    #print hws

    pointsArray = []
    hwsArray = []

    for p in points:
        for i in hws:
            pointsArray.append(p)
            hwsArray.append(i)

    pointsArray = numpy.array(pointsArray).astype('<i4')
    hwsArray = numpy.array(hwsArray).astype('<i4')
    porosities = numpy.zeros_like(hwsArray, dtype='<f4')

    #print hwsArray.shape

    mtk.porosityFieldBinary(image,
                            pointsArray,
                            hwsArray,
                            porosities)

    if len(hws) == 1:
        porosities = porosities.reshape((layout[0], layout[1], layout[2]))

    else:
        porosities = porosities.reshape((layout[0], layout[1], layout[2], len(hws)))

        if showGraph:
            for z in range(porosities.shape[0]):
                for y in range(porosities.shape[1]):
                    for x in range(porosities.shape[2]):
                        plt.plot(hws, porosities[z, y, x, :])
            plt.xlabel('Half-window size')
            plt.ylabel('Porosity (%)')
            plt.show()

    return porosities


# if __name__ == "__main__":
#     image = tifffile.imread("COEA01-GL-17-0367x0274x0265-8b.tif")
#
#     run(image,
#         nodeSpacing=75,
#         hws=range(0, 100, 5),
#         showGraph=True
#         )
#     # Right HWS ~30
#     porosity = run(image,
#                    nodeSpacing=20,
#                    hws=30
#                    )
#     plt.imshow(porosity[porosity.shape[0]/2])
#     plt.colorbar()
#     plt.show()
