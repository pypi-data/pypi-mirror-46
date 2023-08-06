from __future__ import print_function

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy


def plotMultivariateGaussians(phi, mean, hessian, n=100):

    X = numpy.linspace(mean[0]-0.1*hessian[0][0], mean[0]+0.1*hessian[0][0], n)
    Y = numpy.linspace(mean[1]-0.1*hessian[1][1], mean[1]+0.1*hessian[1][1], n)

    X, Y = numpy.meshgrid(X, Y)
    gauss = numpy.zeros((n, n))

    print(X)
    print(Y)
    for ny in range(n):
        y = Y[ny, 0]
        for nx in range(n):
            x = X[0, nx]
            h = numpy.array([x, y])
            gauss[nx, ny] = float(
                phi) * numpy.exp(-0.5*(numpy.dot(numpy.dot(h-mean, hessian), h-mean)))
            # print h, gauss[ nx, ny ]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, gauss, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    plt.show()


if __name__ == "__main__":

    mean = [0, 0]

    a = 9.04
    b = -18.54
    c = 20.90

    hessian = [[a, b],
               [b, c]
               ]

    plot(1, mean, hessian, n=100)
