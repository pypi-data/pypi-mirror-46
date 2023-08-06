#include <stdio.h>
#include <math.h>
#include <iostream>
#include "labelToolkitC.hpp"

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))


/* 2016-11-09 -- Edward Andò and Max Wiebicke
 *  Moment of Interia tensor calculation
 */

/* This function takes in:
 *    - labelled 3D image where the object of interest are labelled as non-zero short ints
 *    - a numpy array containing the labels to work on in numerical order (total length nLabels)
 *    - an nLabelsx3x3 float array for output
 * 
 *  Function Layout: This has 3 passes through the data:
 *    1. Bounding Boxes
 *    2. Centre-of-mass
 *    3. Moment-of-inertia
 */

// typedef labelT;



void boundingBoxes(    int volSizeZ,  int volSizeY, int volSizeX,   labels::label* volLab,
                       int maxLabel,  int six,                     unsigned short* boundingBoxes
                    )
{
    for ( labels::label i = 1;  i < (labels::label)maxLabel; i++)
    {
//         printf( "\rResetting label extents: \t%02.1f%%\t", 100 * (float)i / (float)maxLabel );
        boundingBoxes[i*6+0] = volSizeZ-1;
        boundingBoxes[i*6+1] = 0;
        boundingBoxes[i*6+2] = volSizeY-1;
        boundingBoxes[i*6+3] = 0;
        boundingBoxes[i*6+4] = volSizeX-1;
        boundingBoxes[i*6+5] = 0;
    }

  /*###############################################################
    ### Step 1 get bounding boxes for each label
    ############################################################### */

//     printf( "sizes Z: %i Y: %i X: %i\n", volSizeZ, volSizeY, volSizeX );
    /* Loop over pixels and fill it in... */
    for ( size_t z = 0; z <= volSizeZ-1; z++ )
    {
//         printf( "\r\tBounding box progress: \t\t%02.1f%%\t", 100 * (float)(z+1) / (float)volSizeZ );
        for ( size_t y = 0; y <= volSizeY-1; y++ )
        {
            for ( size_t x = 0; x <= volSizeX-1; x++ )
            {
                size_t index_i = z  * volSizeX * volSizeY   +   y * volSizeX   +   x;

                labels::label pixelValue = volLab[ index_i ];

                if ( pixelValue != 0 )
                {
                    boundingBoxes[ pixelValue*6+0 ] = MIN( z, boundingBoxes[ pixelValue*6+0 ] );
                    boundingBoxes[ pixelValue*6+2 ] = MIN( y, boundingBoxes[ pixelValue*6+2 ] );
                    boundingBoxes[ pixelValue*6+4 ] = MIN( x, boundingBoxes[ pixelValue*6+4 ] );

                    boundingBoxes[ pixelValue*6+1 ] = MAX( z, boundingBoxes[ pixelValue*6+1 ] );
                    boundingBoxes[ pixelValue*6+3 ] = MAX( y, boundingBoxes[ pixelValue*6+3 ] );
                    boundingBoxes[ pixelValue*6+5 ] = MAX( x, boundingBoxes[ pixelValue*6+5 ] );
                }
            }
        }
    }

//     printf( "\n" );

}


