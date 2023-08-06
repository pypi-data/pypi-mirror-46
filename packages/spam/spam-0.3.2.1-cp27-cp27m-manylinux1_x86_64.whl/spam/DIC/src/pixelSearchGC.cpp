#include <stdio.h>
#include <math.h>
#include <iostream>
#include "pixelSearchGC.hpp"

/* 2017-05-12 Emmanuel Roubin and Edward Ando
 * 
 *
 */

float InvSqrt(float x)
{
    float xhalf = 0.5f * x;
    int i = *(int*)&x;              // get bits for floating value
    i = 0x5f375a86 - (i >> 1);      // gives initial guess y0 -- what the fuck?!
    x = *(float*)&i;                // convert bits back to float
    x = x * (1.5f - xhalf * x * x); // Newton step, repeating increases accuracy
    return x;
}


/*                                  Image sizes, ZYX and images*/
void pixelSearchC(  int im1z,          int im1y,          int im1x, float* im1,
                    int im2z,          int im2y,          int im2x, float* im2,
                    int startPosN,                                  float* startPos,    /* Position in image 1 of the middle of the search range, Z, Y, X */
                    int searchRangeN,  int two,                     float* searchRange, /* minus and plus searching directions [ [ z-, z+ ], [ y-, y+ ], [ x-, x+ ] ] */                     
                    int n1,                                         float* argoutdata )
{
    /* size_t variable to build index to 1D-images from x,y,z coordinates */
//     size_t index1, index2;

    /* loop variables for 3D search range */
    long zDisp, yDisp, xDisp;

    /* loop variables for 3D CC calculation */
    long z, y, x;


    /* empty variables for each pixel of our 3D image */
    float im1px, im2px;

    /* Variable to assemble NCC into. */
    double cc;
    double ccMax;
    ccMax = 0;

    /* Maximum variables, for tracking the best NCC so far... */
    int zMax, yMax, xMax;
    zMax = yMax = xMax = 0;


    /* calculate half-window size of image1, we will use it a lot */
//     unsigned short im1zHalf, im1yHalf, im1xHalf;
//     im1zHalf = im1z/2;
//     im1yHalf = im1y/2;
//     im1xHalf = im1x/2;

    /* Pre-calculate slice dimension for faster indexing */
    long im1yXim1x, im2yXim2x;
    im1yXim1x = im1y*im1x;
    im2yXim2x = im2y*im2x;

//     std::cout << im1zHalf << " " << im1yHalf << " " << im1xHalf << "\n" << std::endl;
    /* Go through search range in im2 -- z, y, x positions are offsets of the window,
            Consequently the first iteration here at z=y=x=0, is comparing im1 with the top
            Corner of im2 */
    for ( zDisp=(long)searchRange[0]; zDisp <= (long)searchRange[1]; zDisp++ )
    {
        for ( yDisp = (long)searchRange[2]; yDisp <= (long)searchRange[3]; yDisp++ )
        {
            for ( xDisp = (long)searchRange[4]; xDisp <= (long)searchRange[5]; xDisp++ )
            {
                /* Calculate this bit as far out as possible to benefit from recycling */
                long zTop, yTop, xTop;
                long zBot, yBot, xBot;

                zTop = (long)startPos[0]+zDisp-(im1z-1)/2;
                yTop = (long)startPos[1]+yDisp-(im1y-1)/2;
                xTop = (long)startPos[2]+xDisp-(im1x-1)/2;

                zBot = zTop+im1z;
                yBot = yTop+im1y;
                xBot = xTop+im1x;

//                 printf("zTop %i yTop %i xTop %i\n", zTop, yTop, xTop);
//                 printf("zDisp %i yDisp %i xDisp %i\n", zDisp, yDisp, xDisp);
//                 std::cout << "Tops: "<< zTop << " " << yTop << " " << xTop << "\n" << std::endl;
//                 std::cout << "Bots: "<< zBot << " " << yBot << " " << xBot << "\n" << std::endl;
                /* Check we're not outside the boundaries... */
                if ( zTop >=   0  && yTop >=   0  && xTop >=   0 &&
                     zBot <= im2z && yBot <= im2y && xBot <= im2x )
                {

//                     std::cout << zDisp << " " << yDisp << " " << xDisp << "\n" << std::endl;
                    /* reset calculations */
                    /* three components to our NCC calculation (see documentation/C-remi.odt) */
                    float a,b,c;
                    a = b = c = 0;

//                     std::cout << im1z << " " << im1y << " " << im1x << "\n" << std::endl;
                    /* CC calculation Loop z-first (for numpy) */
                    for ( z=0; z<im1z; z++ )
                    {
                        /* More speedups, precalculate slice offset*/
                        unsigned long zOffset1 =  z      *im1yXim1x;
                        unsigned long zOffset2 = (z+zTop)*im2yXim2x;

                        for ( y=0; y<im1y; y++ )
                        {
                            /* More speedups, precalculate column offset*/
                            unsigned long yOffset1 =  y      *im1x;
                            unsigned long yOffset2 = (y+yTop)*im2x;

                            for ( x=0; x<im1x; x++ )
                            {
//                                 std::cout << "x = " <<  x << " y = " << y << " z = " << z << std::endl;
                                /* build index to 1D image1 */
//                                 index1 =  z      *im1y*im1x + y      *im1x + x;
                                size_t index1 =  zOffset1 + yOffset1 + x;
//                                 std::cout << "index1 = " <<  index1 << std::endl;

                                /*2015-10-22: EA -- skip NaNs in the reference image
                                *  NaNs in C are not even equal to themselves, so we'll use this simple check. */
                                if ( im1[ index1 ] == im1[ index1 ]  )
                                {
                                    /* build index to 1D image2 */
//                                     index2 = (z+zTop)*im2y*im2x + (y+yTop)*im2x + (x+xTop);
                                    size_t index2 = zOffset2 + yOffset2 + (x+xTop);

                                    // fetch 1 pixel from both images
                                    im1px = im1[ index1 ];
                                    im2px = im2[ index2 ];
//                                     printf( "\tim1px=%f im2px=%f\n", im1px, im2px );

                                    // Our little bits of the NCC
                                    a = a + im1px * im2px;
                                    b = b + im1px * im1px;
                                    c = c + im2px * im2px;
//                                     printf( "\ta=%f b=%f c=%f\n", a, b, c );
                                }
                            }
                        }
                    }
                    /* End CC calculation loop */

                    /* once the sums are done, add up and sqrt
                    * assemble bits and calculate CC */

                    cc = a * InvSqrt( b * c );
//                     cc = a / std::sqrt( b * c );

//                     printf( "\tC: pixel_search: cc = %f\n", cc );
//                     printf( "\t-> CC@(z=%i,y=%i,x=%i) = %f\n", z, y, x, cc );

                    /* If this cc is higher than the previous best, update our best... */
                    if ( cc > ccMax )
                    {
                        xMax   = xDisp;
                        yMax   = yDisp;
                        zMax   = zDisp;
                        ccMax  = cc;
//                         printf("##### CC UPDATED #####");
//                         printf( "\t-> New CC_max@(z=%i,y=%i,x=%i) = %f\n", zMax, yMax, xMax, cc );
                    }
                }
            }
        }
    }

    argoutdata[ 0 ] = (float) zMax;
    argoutdata[ 1 ] = (float) yMax;
    argoutdata[ 2 ] = (float) xMax;
    argoutdata[ 3 ] = ccMax;
}

