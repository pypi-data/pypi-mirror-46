#include <stdio.h>
#include <math.h>
#include <iostream>
#include "computeGMresidualAndPhase.hpp"


/* 2017-10-05 Emmanuel Roubin and Edward Ando
 *
 * Please refer to Tudisco et al. "An extension of Digital Image Correlation for intermodality image registration" for theoretical background.
 *
 * The GM "computeDICoperators" is for Gaussian-Mixture of two modalities
 *
 * Calculate M and A matrices to allow an external function to solve in order to get a deltaF
 *
 * Inputs (from swig):
 *   - im1 (stationary)
 *   - im2 (being progressively deformed outside this function)
 *   - im2gz (gradient of im2 in the z direction)
 *   - im2gy (gradient of im2 in the y direction)
 *   - im2gx (gradient of im2 in the x direction)
 *   - Peaks array, 6*nPeaks. order of data: phi, Muim1, Muim2, a, b, c (a coupled to im1, b coupled to im1*im2, c coupled to im2)
 *   - empty 12x12 M matrix
 *   - empty 12x1  A vector
 *   -
 * Outputs:
 *   - none (M and A are updated)
 */

/*                                  Image sizes, ZYX and images*/
void computeGMresidualAndPhase( int nz1,     int ny1,     int nx1,   float* im1,
                                int nz2,     int ny2,     int nx2,   float* im2,
                                int binsF,   int binsG,              unsigned char* phases,
                                int nPeaks,  int six,                float* peaks,
                                int nz3,     int ny3,     int nx3,   float* residual,
                                int nz4,     int ny4,     int nx4,   unsigned char*   imLabelled
                            )
{

//     std::cout << "countT: " << countThreshold << std::endl;
    /* outside loop over non-deformed image 1 called im1 */
    for ( int z1=0; z1 < nz1; z1++ )
    {
        for ( int y1=0; y1 < ny1; y1++ )
        {
            for ( int x1=0; x1 < nx1; x1++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                unsigned int index1 = z1 * ny1 * nx1 + y1 * nx1 + x1;

                /* check whether this is a NaN -- This can be used to mask the image */
                if ( im2[index1] == im2[index1] )
                {
                    /* Start by finding which peak this pair of voxels corresponds to */
                    // char  thePeak = 0;
                    float phi2min = 0;
                    for ( char i=0; i < (char)nPeaks; i++ )
                    {
                        float phi   = peaks[6*i+0];
                        float Muim1 = peaks[6*i+1];
                        float Muim2 = peaks[6*i+2];
                        float a     = peaks[6*i+3];
                        float b     = peaks[6*i+4];
                        float c     = peaks[6*i+5];
                        float lambda= 0.5 * ( a*pow( im1[index1]-Muim1, 2 ) + 2.0*b*(im1[index1]-Muim1)*(im2[index1]-Muim2) + c*pow( im2[index1]-Muim2, 2 ) );
                        float phi2  = lambda - log( phi ) ;

                        if ( ( i == 0 ) or ( phi2 < phi2min ) )
                        {
                            // thePeak = i;
                            phi2min = phi2;
                        }
                    }

//                     std::cout << "phi: " << phi << " phi2: " << phi2 << " threshold: "  << log(countThreshold) << std::endl;
//
//                     if( -phi2min > log(0.0) )
//                     {
//                     }
//                     else
//                     {
// //                         std::cout << "out\n";
//                         residual[index1] = 0;
//                     }

                    int pixelF = (int)im2[index1];
                    int pixelG = (int)im1[index1];
                    int phase = phases[ pixelF + binsG*pixelG ];
                    imLabelled[index1] = phase;
                    if(phase > 0)
                    {
                        residual[index1] = phi2min;
                    } else
                    {
                        residual[index1] = 0;
                    }

                } /* end NaN check */

            }
        }
    }  /* end of im1 coords loop */
}
