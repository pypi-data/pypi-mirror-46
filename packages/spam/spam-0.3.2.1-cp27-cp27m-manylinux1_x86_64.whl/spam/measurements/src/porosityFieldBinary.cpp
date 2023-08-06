#include <stdio.h>
#include <math.h>
#include <iostream>
#include "porosityField.hpp"


/* 2018-03-07 -- Olga Stamati and Edward Andò -- Measurement a porosity field for an already binarised (or trinarised) 8 bit 3D image */

/* Inputs:
 *    - 3D image (8 bit) where:
 *          0 means   0% porosity
 *        100 means 100% poristy
 *        255 means no do count here
 *    - Nx3 array of ints giving measurement positions
 *    - Nx1 array of ints giving half-window sizes
 *
 * Outputs:
 *    - Nx1 array of floats giving porosity in the window
 * 
 */
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))


void porosityFieldBinary(  int volSizeZ,   int volSizeY,   int volSizeX, unsigned char * vol,
                           int N,          int three,                    int  * posArray,
                           int Ntwo,                                     int  * hwsArray,
                           int Nthree,                                   float* out
                        )
{    
    /**********************************************************
     * Loop over all points that have been passed to us
     *********************************************************/
//     #pragma omp parallel
    for ( int pointN = 0; pointN < N; pointN++ )
    {
        int zPoint = posArray[ pointN*3 + 0 ];
        int yPoint = posArray[ pointN*3 + 1 ];
        int xPoint = posArray[ pointN*3 + 2 ];
        int hws    = hwsArray[ pointN ];
        unsigned int count = 0;
        unsigned long int sum = 0;
//         printf( "Point %i is in position %i %i %i with HWS %i\n", pointN, zPoint, yPoint, xPoint, hws );
        /**********************************************************
        * Loop box around this point, looking out for 255 exclude zone and image edges
        *********************************************************/
        for ( int z = MAX( 0, zPoint - hws ); z <= MIN( volSizeZ - 1, zPoint + hws ); z++ )
        {
            for ( int y = MAX( 0, yPoint - hws ); y <= MIN( volSizeY - 1, yPoint + hws ); y++ )
            {
                for ( int x = MAX( 0, xPoint - hws ); x <= MIN( volSizeX - 1, xPoint + hws ); x++ )
                {
                    /* Build index for 3D access */
                    unsigned long index =   z  * volSizeX * volSizeY   +   y * volSizeX   +   x;

                    if ( vol[ index ] != 255 )
                    {
                        count++;
                        /* if value is > 100 but less than 255 */
                        if ( vol[ index ] > 100 )
                        {
                            sum += 100;
                        }
                        else
                        {
                            sum += vol[ index ];
                        }
                    }
                }
            }
        }
        out[ pointN ] = ( float ) sum / (float) count;
    }
}
