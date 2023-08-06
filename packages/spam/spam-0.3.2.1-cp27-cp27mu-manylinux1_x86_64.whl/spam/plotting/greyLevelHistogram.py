import matplotlib.pyplot as plt
import numpy

def plotGreyvalueHistogram( im, greyRange=None, bins=256, normed=False, series=False ):
    if greyRange is None:
        if im.dtype == 'u1':
            greyRange = [0,256]
        elif im.dtype == 'u2':
            greyRange = [0,65536]
        else:
            # Probably a float...
            greyRange = [ im.min(), im.max() ]


    if series == True:
        steps = im.shape[0]
    else:
        steps = 1
        im = [ im.ravel() ]

    for step in range( steps ):
        # Define smoothly-varying colour from blue to red in series
        if series:  d = step/float(steps-1)
        else:       d = 0
        colour = [ 1.0 - d, 0, d ]

        counts,binLimits = numpy.histogram( im[step].ravel(), range=greyRange, bins=bins, normed=normed )
        
        binWidth = ( greyRange[1]-greyRange[0] ) / float( bins )
        
        midBins = [0.5*(a+b) for (a, b) in zip(binLimits[:-1], binLimits[1:])]
        
        if series:
            plt.plot( midBins, counts, color=colour, label="Step = {}".format(step+1) )
        else:
            plt.plot( midBins, counts, color=colour )
    
    #plt.bar( midBins, counts, binWidth, align='center' )
    plt.xlabel( "Greylevel" )
    plt.ylabel( "Frequency" )
    #plt.ylim( [0, sorted( counts )[int(bins*99.5/100)]] )
    if series:
        plt.legend()
    plt.show()
    return counts, midBins
    
if __name__ == "__main__":
    import tifffile
    grey = tifffile.imread( "../../data/M2EA05-quart-01.tif" )
    
    plot( grey )
