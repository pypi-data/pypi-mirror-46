 #include <stdio.h>
#include <math.h>
#include <iostream>
#include "binning.hpp"
// #include <Eigen/Dense>

/* 2017-05-12 Emmanuel Roubin and Edward Ando
 * 
 *  Apply a 4x4 transformation matrix F to a subset of a 3D image.
 * 
 * Inputs:
 *   - F (4x4)
 *   - im
 *   - subim (allocated but empty)
 *   - origin of subim
 * 
 * Outputs:
 *   - ???
 * 
 * Approach:
 *   1. 
 */

/*                                  Image sizes, ZYX and images*/
void binningFloat(  int nz1,   int ny1,  int nx1, float* im,
                    int nzb,   int nyb,  int nxb, float* imBin,
                    int three,                      int* offset,
                    int binning )
{
    //unsigned long zOffset = 0; // unused
    //unsigned long yOffset = 0; // unused

    int zo = offset[0];
    int yo = offset[1];
    int xo = offset[2];

    int binningCubed = binning * binning * binning;

//     printf("Offsets (ZYX): %i %i %i", zo, yo, xo);

//     #pragma omp parallel for simd
    /* iterate over binned image */
    for ( int zb=0; zb < nzb; zb++ )
    {
        for ( int yb=0; yb < nyb; yb++ )
        {
            for ( int xb=0; xb < nxb; xb++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                unsigned long indexB = zb * nyb * nxb + yb * nxb + xb;

                /* now loop over large image */
                for ( int zl=0; zl < binning; zl++ )
                {
                    for ( int yl=0; yl < binning; yl++ )
                    {
                        for ( int xl=0; xl < binning; xl++ )
                        {
                            unsigned long index1 = ( binning*zb + zo) * ny1 * nx1 + ( binning*yb + yo) * nx1 + ( binning*xb + xo );
                            imBin[indexB] += im[ index1 ]/binningCubed;
                        }
                    }
                }
             }
        }
    }
}

void binningUInt(   int nz1,   int ny1,  int nx1,   unsigned short* im,
                    int nzb,   int nyb,  int nxb,   unsigned short* imBin,
                    int three,                      int* offset,
                    int binning )
{
    //unsigned long zOffset = 0; // unused
    //unsigned long yOffset = 0; // unused

    int zo = offset[0];
    int yo = offset[1];
    int xo = offset[2];

//     printf("Offsets (ZYX): %i %i %i", zo, yo, xo);

//     #pragma omp parallel for simd
    /* iterate over binned image */
    for ( int zb=0; zb < nzb; zb++ )
    {
        for ( int yb=0; yb < nyb; yb++ )
        {
            for ( int xb=0; xb < nxb; xb++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                unsigned long indexB = zb * nyb * nxb + yb * nxb + xb;

                unsigned long sum = 0;
                int count = 0;
                /* now loop over large image */
                for ( int zl=0; zl < binning; zl++ )
                {
                    for ( int yl=0; yl < binning; yl++ )
                    {
                        for ( int xl=0; xl < binning; xl++ )
                        {
                            unsigned long index1 = ( binning*zb + zo) * ny1 * nx1 + ( binning*yb + yo) * nx1 + ( binning*xb + xo );
                            sum += im[ index1 ];
                            count ++;
                        }
                    }
                }
                imBin[indexB] = sum/count;
             }
        }
    }
}


void binningChar(   int nz1,   int ny1,  int nx1, unsigned char* im,
                    int nzb,   int nyb,  int nxb, unsigned char* imBin,
                    int three,                       int* offset,
                    int binning )
{
    //unsigned long zOffset = 0; // unused
    //unsigned long yOffset = 0; // unused

    int zo = offset[0];
    int yo = offset[1];
    int xo = offset[2];

//     printf("Offsets (ZYX): %i %i %i", zo, yo, xo);

//     #pragma omp parallel for simd
    /* iterate over binned image */
    for ( int zb=0; zb < nzb; zb++ )
    {
        for ( int yb=0; yb < nyb; yb++ )
        {
            for ( int xb=0; xb < nxb; xb++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                unsigned long indexB = zb * nyb * nxb + yb * nxb + xb;

                unsigned long sum = 0;
                int count = 0;
                /* now loop over large image */
                for ( int zl=0; zl < binning; zl++ )
                {
                    for ( int yl=0; yl < binning; yl++ )
                    {
                        for ( int xl=0; xl < binning; xl++ )
                        {
                            unsigned long index1 = ( binning*zb + zo) * ny1 * nx1 + ( binning*yb + yo) * nx1 + ( binning*xb + xo );
                            sum += im[ index1 ];
                            count ++;
                        }
                    }
                }
                imBin[indexB] = sum/count;
             }
        }
    }
}

