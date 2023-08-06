from __future__ import print_function
import numpy
import matplotlib.pyplot as plt


def plotParticleSizeDistribution(inputRadii,
        range=None,
        logScaleX=False,
        logScaleY=False,
        units="px",
        bins=256,
        cumulative=False,
        cumulativePassing=True,
        mode="particles",
        returnValues=False,
        plot=True,
        legendNames=None):
    """
    This functions draws particle size distributions.
    There are a number of options, which are detailed below.
    For a typical geotechnical grading curve the following options (not default) should be used:

        * cumulative=True,
        * cumulativePassing=True,
        * mode="mass",
        * logScaleX=True,
        * logScaleY=False

    Parameters
    -----------

        inputRadii : list of particle radii
            This can be in any units, but if they are not in pixels, you should also set the "units" variable so that the label on the x-axis is correct

        range : two-component list (optional, default = [min and max] radii or calculated volumes )
            Contains range for histogram, top and bottom.

        logScaleX : Bool (optional, default = False)
            Log-scale X axis

        logScaleY : Bool (optional, default = False)
            Log-scale Y axis

        units : string (optional, default = "px")
            Units to write on the x-axis

        bins : int (optional, default = 256)
            Number of bins for the histogram, *i.e.,* the number of points

        cumulative : bool (optional, default = False)
            Draw a cumulative histogram, or just a regular histogram?

        cumulativePassing : bool (optional, default = True)
            If you aked for a cumulative histogram, do you want it in "passing" the sieve mode, or in "retained" on the sieve mode?

        mode : string (options, default = "massExact")
            Should the cumulative graphs be based on number of particles,
            or particle volume/mass? In sieving ones measures mass.
            Options:

                * "particles"
                * "mass"
                * "volume" -- the same as above

        returnValues : bool (optional, default=False)
            return size and count vectors

        plot : bool (optional, default=True)
            actually draw a matplotlib graph

        legendNames : list of strings (optional, default=None)
            Description of distribution

    Returns
    --------
        None -- just a matplotlib graph
    """
    def rad2vol(rad): return ((4.0*rad)/(3.0*numpy.pi))**(3.0)

    # detect list of lists with code from: https://stackoverflow.com/questions/5251663/determine-if-a-list-contains-other-lists
    if not any(isinstance(el, list) for el in inputRadii ):
        inputRadii = [ inputRadii ]

    # Determine overall range. Flatten list
    if range is None:
        radiiTemp = numpy.array( [item for sublist in inputRadii for item in sublist] )
        range = [radiiTemp.min(), radiiTemp.max()]
        del radiiTemp

    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

    for n, radii in enumerate( inputRadii ):
        print("\tparticleSizeDistribution.run(): Multiplying radii by two to make diameters")
        #diam = radii*2.0

        if legendNames is None:
            name=""
        else:
            name = legendNames[ n ]

        # Can't use numpy.histogram directly since we need to count particle size and account for their volume
        sieves = numpy.linspace(range[0], range[1], bins)
        counts = numpy.zeros_like(sieves)

        if mode == "mass" or "volume":
            masses = numpy.zeros_like(sieves, dtype=float)

        # Sort radii
        radii = sorted(radii)

        # This holds the sive index of the current bin.
        #   Since we're using sorted data, this will increase monotonically
        currentSieve = 0
        stop = False
        for r in radii:
            d = r*2.0

            if d > sieves[currentSieve]:
                # print "sieve {} (size={})too small for me (size={})!".format( currentSieve, d,  sieves[currentSieve])
                while d > sieves[currentSieve] and currentSieve < len(sieves)-1:
                    currentSieve += 1
                    # print "\tbump"

            if currentSieve < len(sieves)-1:
                # Add count to bin
                counts[currentSieve] += 1

                # Add to mass to this sieve
                if mode == "mass" or "volume":
                    masses[currentSieve] += rad2vol(r)


        if cumulative:
            if plot:
                plt.grid()
            histCumulative = numpy.zeros_like(counts, dtype=numpy.float)

            if mode == "particles":
                for n, item in enumerate(counts):
                    if n == 0:
                        histCumulative[n] = counts[n]
                    else:
                        histCumulative[n] = counts[n] + histCumulative[n-1]
            elif mode == "mass" or "volume":
                for n, item in enumerate(masses):
                    if n == 0:
                        histCumulative[n] = masses[n]
                    else:
                        histCumulative[n] = masses[n] + histCumulative[n-1]
            else:
                print("\tparticleSizeDistribution.run(): Unknown mode")

            # Normalise...
            histCumulative /= float(histCumulative.max())/100.0

            if cumulativePassing:
                if plot:
                    line, = ax.plot(sieves, histCumulative, label=name)
                    #line, = ax.step(sieves, histCumulative, where='post', label=name)
                    plt.ylabel("% {} passing".format(mode))
                if returnValues:
                    returnOutput = [sieves, histCumulative]

            else:
                histCumulative = 100 - histCumulative
                if plot:
                    line, = ax.plot(sieves, histCumulative, label=name)
                    #line, = ax.step(sieves, histCumulative, where='post', label=name)
                    #ax.plot( sieves, histCumulative, )
                    plt.ylabel("% {} retained".format(mode))
                if returnValues:
                    returnOutput = [sieves, histCumulative]

            if plot:
                plt.xlabel("Sieve Size ({})".format(units))

        else:
            if plot:
                #line, = ax.plot(sieves+(sieves[1]-sieves[0])/2.0, counts, label=name)
                line, = ax.step(sieves+(sieves[1]-sieves[0])/2.0, counts, where='post', label=name)
                plt.ylabel("Count")
                plt.xlabel("Particle Size ({})".format(units))
            if returnValues:
                returnOutput = [sieves+(sieves[1]-sieves[0])/2.0, counts]

        if logScaleX and plot:
            ax.set_xscale('log')

        if logScaleY and plot:
            ax.set_yscale('log')

    if legendNames is not None:
        plt.legend()

    if plot:
        plt.show()

    if returnValues:
        return returnOutput


if __name__ == "__main__":
    import tifffile
    import spam.label.toolkit as ltk

    lab = tifffile.imread("./data/M2EA05/M2EA05-quart-01-bin-watershed.tif")

    radii = ltk.getEquivalentRadii(lab)

    # Apply pixel size and binning
    radii = numpy.multiply(radii, 15.0*4.0/1000.0)

    run(radii,
        bins=256,
        units="mm",
        cumulative=True,
        cumulativePassing=True,
        mode="mass",
        range=[0, 2],
        # range=None,
        logScaleX=False,
        logScaleY=False)
