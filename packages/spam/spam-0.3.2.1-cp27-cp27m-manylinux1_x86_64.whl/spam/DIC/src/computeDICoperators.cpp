#include <stdio.h>
#include <math.h>
#include <iostream>
#include "computeDICoperators.hpp"
#include <Eigen/Dense>


/* 2017-05-12 Emmanuel Roubin and Edward Ando
 *
 * Please refer to Tudisco et al. "An extension of Digital Image Correlation for intermodality image registration" for theoretical background.
 *
 * The standard "computeDICoperators" is for same-modality registration.
 *
 * Calculate M and A matrices to allow an external function to solve in order to get a deltaF
 *
 * Inputs (from swig):
 *   - im1 (stationary)
 *   - im2 (being progressively deformed outside this function)
 *   - im1gz (gradient of im2 in the z direction)
 *   - im1gy (gradient of im2 in the y direction)
 *   - im1gx (gradient of im2 in the x direction)
 *   - empty 12x12 M matrix
 *   - empty 12x1  A vector
 * Outputs:
 *   - none (M and A are updated)
 */

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

/*                                  Image sizes, ZYX and images*/
void computeDICoperators(   int nz1,     int ny1,     int nx1,   float* im1,   \
                            int nz2,     int ny2,     int nx2,   float* im2,   \
                            int nz2gz,   int ny2gz,   int nx2gz, float* im2gz, \
                            int nz2gy,   int ny2gy,   int nx2gy, float* im2gy, \
                            int nz2gx,   int ny2gx,   int nx2gx, float* im2gx, \
                            int twelve1, int twelve2,            float* M,     \
                            int twelve3,                         float* A  )
{
    // 2018-07-10 EA and OS: offset to calculate dF in centre of image
    float centreOffsetZ = ( nz1 - 1 ) / 2.0;
    float centreOffsetY = ( ny1 - 1 ) / 2.0;
    float centreOffsetX = ( nx1 - 1 ) / 2.0;

    // set ouput matrix to 0 -- issue #105
    for (int i=0; i<twelve1*twelve2; i++)
    {
        M[i] = 0;
    }
    // set ouput vector to 0 -- issue #105
    for (int i=0; i<twelve3; i++)
    {
        A[i] = 0;
    }

    size_t nz1us = (size_t)nz1;
    size_t ny1us = (size_t)ny1;
    size_t nx1us = (size_t)nx1;

    /* outside loop over non-deformed image 1 called im1 */
    for ( size_t z1=0; z1 < nz1us; z1++ )
    {
        for ( size_t y1=0; y1 < ny1us; y1++ )
        {
            for ( size_t x1=0; x1 < nx1us; x1++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                size_t index1 = z1 * ny1us * nx1us + y1 * nx1us + x1;

                /* check whether this is a NaN -- Check if this pixel in im1 is not NaN */
                if ( im1[index1] == im1[index1] )
                {
                    /* See comment just before equation 8 -- i(m) == iofm and j(m) == jofm
                     * These two iterators allow us to go from the 4x4 F matrix to the 12x1
                     * flattened view of F with Voigt notation.
                     *
                     * Note: i(m) goes just to 3 to avoid the last line of F which is just padding*/
                    for ( int iofm=0; iofm < 3; iofm++ )
                    {
                        for ( int jofm=0; jofm < 4; jofm++ )
                        {
                            /* Variable to hold current coordinate (x_j(m)) in both eq 12 and 13 */
                            float xjofm;

                            switch( jofm )
                            {
                                case 0: xjofm = z1 - centreOffsetZ; break;
                                case 1: xjofm = y1 - centreOffsetY; break;
                                case 2: xjofm = x1 - centreOffsetX; break;
                                case 3: xjofm = 1;  break;
                            }

                            /* Variable to hold current greyvalue gTilda_,i(m) which is the gradient of
                             * the deformed im2 in the ith direction which appears in both eq 12 and 13 */
                            float gradim2iofm;
                            switch( iofm )
                            {
                                case 0: gradim2iofm = im2gz[index1]; break;
                                case 1: gradim2iofm = im2gy[index1]; break;
                                case 2: gradim2iofm = im2gx[index1]; break;
                            }

                            /* Calculate 'm' from i(m) and j(m) to access A matrix */
                            /* and sum over pixels into A which is 12x1 (equation 13) */
                            int m = 4*iofm + jofm;
                            A[ m ] += ( im1[index1] - im2[index1] ) * ( xjofm * gradim2iofm );

                            /* Second loop to fill M matrix *
                             * as before loop over 'p' i goes to 3 and j to 4 */
                            for ( int iofp=0; iofp < 3; iofp++    )
                            {
                                for ( int jofp=0; jofp < 4; jofp++ )
                                {
                                    /* Variable to hold current coordinate (x_j(p)) in eq 12 */
                                    float xjofp;
                                    switch( jofp )
                                    {
                                        case 0: xjofp = z1 - centreOffsetZ; break;
                                        case 1: xjofp = y1 - centreOffsetY; break;
                                        case 2: xjofp = x1 - centreOffsetX; break;
                                        case 3: xjofp = 1;  break;
                                    }

                                    /* Variable to hold current greyvalue gTilda_,i(p) which is the gradient of
                                     * the deformed im2 in the ith direction which appears in eq 12 */
                                    float gradim2iofp;
                                    switch( iofp )
                                    {
                                        case 0: gradim2iofp = im2gz[index1]; break;
                                        case 1: gradim2iofp = im2gy[index1]; break;
                                        case 2: gradim2iofp = im2gx[index1]; break;
                                    }


                                    /* Sum over pixels into M which is 12x12 */
                                    int p = ( 4*iofp + jofp );
                                    M[ p + (12 * m) ] += ( xjofm * gradim2iofm ) * ( xjofp * gradim2iofp );
                                }
                            } /* end of 'p' loops */
                        }
                    }  /* end of 'm' loops */
                } /* end NaN check */

            }
        }
    }  /* end of im1 coords loop */
}

/* 2017-10-05 Emmanuel Roubin and Edward Ando
 *
 * Please refer to Tudisco et al. "An extension of Digital Image Correlation for intermodality image registration" for theoretical background.
 *
 * The LL "computeDICoperators" is for Log-Likelihood of both modalities
 *
 * Calculate M and A matrices to allow an external function to solve in order to get a deltaF
 *
 * Inputs (from swig):
 *   - im1 (stationary) strictly scaled [0.0,1.0]
 *   - im2 (being progressively deformed outside this function) strictly scaled [0.0,1.0]
 *   - im2gz (gradient of im2 in the z direction)
 *   - im2gy (gradient of im2 in the y direction)
 *   - im2gx (gradient of im2 in the x direction)
 *   - OxO (first  gradient of joint histrogram in the direction of the deformed image)
 *   - OxO (second gradient of joint histrogram in the direction of the deformed image)
 *   - empty 12x12 M matrix
 *   - empty 12x1  A vector
 *   -
 * Outputs:
 *   - none (M and A are updated)
 */

/*                                  Image sizes, ZYX and images*/
void computeDICoperatorsLL(   int nz1,     int ny1,     int nx1,   float* im1,   \
                              int nz2,     int ny2,     int nx2,   float* im2,   \
                              int nz2gz,   int ny2gz,   int nx2gz, float* im2gz, \
                              int nz2gy,   int ny2gy,   int nx2gy, float* im2gy, \
                              int nz2gx,   int ny2gx,   int nx2gx, float* im2gx, \
                              int nBinsA,  int nBinsB,             float* jointHistGrad1, \
                              int nBinsC,  int nBinsD,             float* jointHistGrad2, \
                              int twelve1, int twelve2,            float* M,     \
                              int twelve3,                         float* A )
{
    if ( nBinsA != nBinsB )
    {
        printf ("computeDICoperators.computeDICoperatorsLL(): Number of bins for the joint histogram not the same, exiting\n");
        return;
    }

    // set ouput matrix to 0 -- issue #105
    for (int i=0; i<twelve1*twelve2; i++)
    {
        M[i] = 0;
    }
    // set ouput vector to 0 -- issue #105
    for (int i=0; i<twelve3; i++)
    {
        A[i] = 0;
    }

    // 2018-07-10 EA and OS: offset to calculate dF in centre of image
    float centreOffsetZ = ( nz1 - 1 ) / 2.0;
    float centreOffsetY = ( ny1 - 1 ) / 2.0;
    float centreOffsetX = ( nx1 - 1 ) / 2.0;

    size_t nz1us = (size_t)nz1;
    size_t ny1us = (size_t)ny1;
    size_t nx1us = (size_t)nx1;

    /* outside loop over non-deformed image 1 called im1 */
    for ( size_t z1=0; z1 < nz1us; z1++ )
    {
        for ( size_t y1=0; y1 < ny1us; y1++ )
        {
            for ( size_t x1=0; x1 < nx1us; x1++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                size_t index1 = z1 * ny1us * nx1us + y1 * nx1us + x1;

                /* check whether this is a NaN -- This can be used to mask the image */
                if ( im2[index1] == im2[index1] )
                {
                    /* convert current im1 and im2 values into bin numbers -- multiply value with bin number and floor it*/
                    int im1Bin = (int)( nBinsA * im1[index1] );
                    int im2Bin = (int)( nBinsA * im2[index1] );

                    // Assuming jointHist is organised im1 first
                    long jointHistindex = im1Bin * nBinsA + im2Bin;

                    float phi2grad1 = jointHistGrad1[jointHistindex];
                    float phi2grad2 = jointHistGrad2[jointHistindex];

                    /* See comment just before equation 8 -- i(m) == iofm and j(m) == jofm
                     * These two iterators allow us to go from the 4x4 F matrix to the 12x1
                     * flattened view of F with Voigt notation.
                     *
                     * Note: i(m) goes just to 3 to avoid the last line of F which is just padding*/
                    for ( int iofm=0; iofm < 3; iofm++ )
                    {
                        for ( int jofm=0; jofm < 4; jofm++ )
                        {
                            /* Variable to hold current coordinate (x_j(m)) in both eq 12 and 13 */
                            float xjofm;

                            switch( jofm )
                            {
                                case 0: xjofm = z1 - centreOffsetZ; break;
                                case 1: xjofm = y1 - centreOffsetY; break;
                                case 2: xjofm = x1 - centreOffsetX; break;
                                case 3: xjofm = 1;  break;
                            }

                            /* Variable to hold current greyvalue gTilda_,i(m) which is the gradient of
                             * the deformed im2 in the ith direction which appears in both eq 12 and 13 */
                            float gradim2iofm;
                            switch( iofm )
                            {
                                case 0: gradim2iofm = im2gz[index1]; break;
                                case 1: gradim2iofm = im2gy[index1]; break;
                                case 2: gradim2iofm = im2gx[index1]; break;
                            }

                            /* Calculate 'm' from i(m) and j(m) to access A matrix */
                            /* and sum over pixels into A which is 12x1 (equation 13) */
                            int m = 4*iofm + jofm;
                            A[ m ] -= phi2grad1 * ( xjofm * gradim2iofm );

                            /* Second loop to fill M matrix *
                             * as before loop over 'p' i goes to 3 and j to 4 */
                            for ( int iofp=0; iofp < 3; iofp++    )
                            {
                                for ( int jofp=0; jofp < 4; jofp++ )
                                {
                                    /* Variable to hold current coordinate (x_j(p)) in eq 12 */
                                    float xjofp;
                                    switch( jofp )
                                    {
                                        case 0: xjofp = z1 - centreOffsetZ; break;
                                        case 1: xjofp = y1 - centreOffsetY; break;
                                        case 2: xjofp = x1 - centreOffsetX; break;
                                        case 3: xjofp = 1;  break;
                                    }

                                    /* Variable to hold current greyvalue gTilda_,i(p) which is the gradient of
                                     * the deformed im2 in the ith direction which appears in eq 12 */
                                    float gradim2iofp;
                                    switch( iofp )
                                    {
                                        case 0: gradim2iofp = im2gz[index1]; break;
                                        case 1: gradim2iofp = im2gy[index1]; break;
                                        case 2: gradim2iofp = im2gx[index1]; break;
                                    }

                                    /* Sum over pixels into M which is 12x12 */
                                    int p = ( 4*iofp + jofp );
                                    M[ p + (12 * m) ] += phi2grad2 * ( xjofm * gradim2iofm ) * ( xjofp * gradim2iofp );
                                }
                            } /* end of 'p' loops */
                        }
                    }  /* end of 'm' loops */
                } /* end NaN check */

            }
        }
    }  /* end of im1 coords loop */
}

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
void computeDICoperatorsGM(   int nz1,     int ny1,     int nx1,   float* im1,   \
                              int nz2,     int ny2,     int nx2,   float* im2,   \
                              int nz2gz,   int ny2gz,   int nx2gz, float* im2gz, \
                              int nz2gy,   int ny2gy,   int nx2gy, float* im2gy, \
                              int nz2gx,   int ny2gx,   int nx2gx, float* im2gx, \
                              int binsF,   int binsG,              unsigned char* phases, \
                              int nPeaks,  int six,                float* peaks, \
                              int twelve1, int twelve2,            float* M,     \
                              int twelve3,                         float* A )
{
    // 2018-07-10 EA and OS: offset to calculate dF in centre of image
    float centreOffsetZ = ( nz1 - 1 ) / 2.0;
    float centreOffsetY = ( ny1 - 1 ) / 2.0;
    float centreOffsetX = ( nx1 - 1 ) / 2.0;

    // set ouput matrix to 0 -- issue #105
    for (int i=0; i<twelve1*twelve2; i++)
    {
        M[i] = 0;
    }
    // set ouput vector to 0 -- issue #105
    for (int i=0; i<twelve3; i++)
    {
        A[i] = 0;
    }

    size_t nz1us = (size_t)nz1;
    size_t ny1us = (size_t)ny1;
    size_t nx1us = (size_t)nx1;

    /* outside loop over non-deformed image 1 called im1 */
    for ( size_t z1=0; z1 < nz1us; z1++ )
    {
        for ( size_t y1=0; y1 < ny1us; y1++ )
        {
            for ( size_t x1=0; x1 < nx1us; x1++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                size_t index1 = z1 * ny1us * nx1us + y1 * nx1us + x1;

                /* check whether this is a NaN -- This can be used to mask the image */
                if ( im2[index1] == im2[index1] )
                {
                    /* Start by finding which peak this pair of voxels corresponds to */
                    /*
                    int   thePeak = 0;
                    float phi2min = 0;
                    for ( int i=0; i < nPeaks; i++ )
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
                            thePeak = i;
                            phi2min = phi2;
                        }
                    }
                    */

                    int pixelF = (int)im2[index1];
                    int pixelG = (int)im1[index1];

                    // This should be done outside here -- check that we're not going outside limits
                    if (pixelF > binsF-1)
                    {
                        pixelF = binsF-1;
                    }
                    if (pixelF < 0)
                    {
                        pixelF = 0;
                    }
                    if (pixelG > binsG-1)
                    {
                        pixelG = binsG-1;
                    }
                    if (pixelG < 0)
                    {
                        pixelG = 0;
                    }
                    unsigned char phase = phases[ pixelF + binsG*pixelG ];
                    // std::cout << pixelF << " " << binsF << " " << phase << std::endl;

                    // std::cout << phi2 << std::endl;
                    if( phase > 0 )
                    {
                        // float phi   = peaks[6*(phase-1)+0]; // not used
                        float Muim1 = peaks[6*(phase-1)+1];
                        float Muim2 = peaks[6*(phase-1)+2];
                        // float a     = peaks[6*(phase-1)+3]; // not used
                        float b     = peaks[6*(phase-1)+4];
                        float c     = peaks[6*(phase-1)+5];

                        // std::cout << pixelF << " " << pixelG << ": "<< phase << std::endl;
                        // std::cout << Muim1 << " " << Muim2 << std::endl;

                        // See comment just before equation 8 -- i(m) == iofm and j(m) == jofm
                        // These two iterators allow us to go from the 4x4 F matrix to the 12x1
                        // flattened view of F with Voigt notation.
                        //  Note: i(m) goes just to 3 to avoid the last line of F which is just padding
                        for ( int iofm=0; iofm < 3; iofm++ )
                        {
                            for ( int jofm=0; jofm < 4; jofm++ )
                            {
                                /* Variable to hold current coordinate (x_j(m)) in both eq 12 and 13 */
                                float xjofm;

                                switch( jofm )
                                {
                                    case 0: xjofm = z1 - centreOffsetZ; break;
                                    case 1: xjofm = y1 - centreOffsetY; break;
                                    case 2: xjofm = x1 - centreOffsetX; break;
                                    case 3: xjofm = 1;  break;
                                    // case 0: xjofm = z1; break;
                                    // case 1: xjofm = y1; break;
                                    // case 2: xjofm = x1; break;
                                    // case 3: xjofm = 1;  break;
                                }

                                /* Variable to hold current greyvalue gTilda_,i(m) which is the gradient of
                                * the deformed im2 in the ith direction which appears in both eq 12 and 13 */
                                float gradim2iofm;
                                switch( iofm )
                                {
                                    case 0: gradim2iofm = im2gz[index1]; break;
                                    case 1: gradim2iofm = im2gy[index1]; break;
                                    case 2: gradim2iofm = im2gx[index1]; break;
                                }

                                /* Calculate 'm' from i(m) and j(m) to access A matrix */
                                /* and sum over pixels into A which is 12x1 (equation 13) */
                                int m = 4*iofm + jofm;
                                A[ m ] -= ( b*(im1[index1]-Muim1) + c*(im2[index1]-Muim2) ) * ( xjofm * gradim2iofm );

                                /* Second loop to fill M matrix *
                                * as before loop over 'p' i goes to 3 and j to 4 */
                                for ( int iofp=0; iofp < 3; iofp++    )
                                {
                                    for ( int jofp=0; jofp < 4; jofp++ )
                                    {
                                        /* Variable to hold current coordinate (x_j(p)) in eq 12 */
                                        float xjofp;
                                        switch( jofp )
                                        {
                                            case 0: xjofp = z1 - centreOffsetZ; break;
                                            case 1: xjofp = y1 - centreOffsetY; break;
                                            case 2: xjofp = x1 - centreOffsetX; break;
                                            case 3: xjofp = 1;  break;
                                            // case 0: xjofp = z1; break;
                                            // case 1: xjofp = y1; break;
                                            // case 2: xjofp = x1; break;
                                            // case 3: xjofp = 1;  break;
                                        }

                                        /* Variable to hold current greyvalue gTilda_,i(p) which is the gradient of
                                        * the deformed im2 in the ith direction which appears in eq 12 */
                                        float gradim2iofp;
                                        switch( iofp )
                                        {
                                            case 0: gradim2iofp = im2gz[index1]; break;
                                            case 1: gradim2iofp = im2gy[index1]; break;
                                            case 2: gradim2iofp = im2gx[index1]; break;
                                        }


                                        /* Sum over pixels into M which is 12x12 */
                                        int p = ( 4*iofp + jofp );
                                        M[ p + (12 * m) ] += c*( xjofm * gradim2iofm ) * ( xjofp * gradim2iofp );
                                    }
                                } /* end of 'p' loops */
                            }
                        }  /* end of 'm' loops */
                    } /* end if phi2 < threshold */
                } /* end NaN check */

            }
        }
    }  /* end of im1 coords loop */
}

/* ========================================================= */
/* ===  Global DVC no sorry DIC starts here              === */
/* ========================================================= */

Eigen::Matrix<float, 4, 4> shapeFunc( Eigen::Matrix<float, 4, 3> pTetMatrix )
{
    /* This function takes four nodes that a tetrahedron, and calculates the four coefficients of the four shape functions, see tetra.pdf */
    /* by the way, since this is C and nothing is easy, we are recieving a pre-allocated 4x4 matrix */
    Eigen::Matrix<float, 4, 4> coeffMatrix;

    /* Fill in jacTet and padd first column with zeros */
    Eigen::Matrix<float, 4, 4> jacTet;
    jacTet(0,0) = 1;
    jacTet(1,0) = 1;
    jacTet(2,0) = 1;
    jacTet(3,0) = 1;
    /* fill in jacTet, which is the jacobian of the tetrahedron (first row padded with ones) */
    for ( unsigned char i = 0; i < 4; i++ )
    {
      for ( unsigned char j = 0; j < 3; j++ )
      {
          jacTet(i,j+1) = pTetMatrix(i,j);
      }
    }

    double sixVee = jacTet.determinant();

    /* define 3x3 matrix to calculate determinant */
    Eigen::Matrix3f tmp;

    /* from tetra.pdf */
    /* a1 */
    tmp(0,0) = jacTet(1,1); tmp(0,1) = jacTet(1,2); tmp(0,2) = jacTet(1,3);
    tmp(1,0) = jacTet(2,1); tmp(1,1) = jacTet(2,2); tmp(1,2) = jacTet(2,3);
    tmp(2,0) = jacTet(3,1); tmp(2,1) = jacTet(3,2); tmp(2,2) = jacTet(3,3);
    coeffMatrix(0,0) =  tmp.determinant() / sixVee;

    /* a2 */
    tmp(0,0) = jacTet(0,1); tmp(0,1) = jacTet(0,2); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(2,1); tmp(1,1) = jacTet(2,2); tmp(1,2) = jacTet(2,3);
    tmp(2,0) = jacTet(3,1); tmp(2,1) = jacTet(3,2); tmp(2,2) = jacTet(3,3);
    coeffMatrix(1,0) = -tmp.determinant() / sixVee;

    /* a3 */
    tmp(0,0) = jacTet(0,1); tmp(0,1) = jacTet(0,2); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(1,1); tmp(1,1) = jacTet(1,2); tmp(1,2) = jacTet(1,3);
    tmp(2,0) = jacTet(3,1); tmp(2,1) = jacTet(3,2); tmp(2,2) = jacTet(3,3);
    coeffMatrix(2,0) =  tmp.determinant() / sixVee;

    /* a4 */
    tmp(0,0) = jacTet(0,1); tmp(0,1) = jacTet(0,2); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(1,1); tmp(1,1) = jacTet(1,2); tmp(1,2) = jacTet(1,3);
    tmp(2,0) = jacTet(2,1); tmp(2,1) = jacTet(2,2); tmp(2,2) = jacTet(2,3);
    coeffMatrix(3,0) = -tmp.determinant() / sixVee;



    /* b1 */
    tmp(0,0) = jacTet(1,0); tmp(0,1) = jacTet(1,2); tmp(0,2) = jacTet(1,3);
    tmp(1,0) = jacTet(2,0); tmp(1,1) = jacTet(2,2); tmp(1,2) = jacTet(2,3);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,2); tmp(2,2) = jacTet(3,3);
    coeffMatrix(0,1) = -tmp.determinant() / sixVee;

    /* b2 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,2); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(2,0); tmp(1,1) = jacTet(2,2); tmp(1,2) = jacTet(2,3);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,2); tmp(2,2) = jacTet(3,3);
    coeffMatrix(1,1) =  tmp.determinant() / sixVee;

    /* b3 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,2); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(1,0); tmp(1,1) = jacTet(1,2); tmp(1,2) = jacTet(1,3);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,2); tmp(2,2) = jacTet(3,3);
    coeffMatrix(2,1) = -tmp.determinant() / sixVee;

    /* b4 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,2); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(1,0); tmp(1,1) = jacTet(1,2); tmp(1,2) = jacTet(1,3);
    tmp(2,0) = jacTet(2,0); tmp(2,1) = jacTet(2,2); tmp(2,2) = jacTet(2,3);
    coeffMatrix(3,1) =  tmp.determinant() / sixVee;



    /* c1 */
    tmp(0,0) = jacTet(1,0); tmp(0,1) = jacTet(1,1); tmp(0,2) = jacTet(1,3);
    tmp(1,0) = jacTet(2,0); tmp(1,1) = jacTet(2,1); tmp(1,2) = jacTet(2,3);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,1); tmp(2,2) = jacTet(3,3);
    coeffMatrix(0,2) =  tmp.determinant() / sixVee;

    /* c2 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,1); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(2,0); tmp(1,1) = jacTet(2,1); tmp(1,2) = jacTet(2,3);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,1); tmp(2,2) = jacTet(3,3);
    coeffMatrix(1,2) = -tmp.determinant() / sixVee;

    /* c3 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,1); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(1,0); tmp(1,1) = jacTet(1,1); tmp(1,2) = jacTet(1,3);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,1); tmp(2,2) = jacTet(3,3);
    coeffMatrix(2,2) =  tmp.determinant() / sixVee;

    /* c4 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,1); tmp(0,2) = jacTet(0,3);
    tmp(1,0) = jacTet(1,0); tmp(1,1) = jacTet(1,1); tmp(1,2) = jacTet(1,3);
    tmp(2,0) = jacTet(2,0); tmp(2,1) = jacTet(2,1); tmp(2,2) = jacTet(2,3);
    coeffMatrix(3,2) = -tmp.determinant() / sixVee;



    /* d1 */
    tmp(0,0) = jacTet(1,0); tmp(0,1) = jacTet(1,1); tmp(0,2) = jacTet(1,2);
    tmp(1,0) = jacTet(2,0); tmp(1,1) = jacTet(2,1); tmp(1,2) = jacTet(2,2);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,1); tmp(2,2) = jacTet(3,2);
    coeffMatrix(0,3) = -tmp.determinant() / sixVee;

    /* d2 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,1); tmp(0,2) = jacTet(0,2);
    tmp(1,0) = jacTet(2,0); tmp(1,1) = jacTet(2,1); tmp(1,2) = jacTet(2,2);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,1); tmp(2,2) = jacTet(3,2);
    coeffMatrix(1,3) =  tmp.determinant() / sixVee;

    /* d3 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,1); tmp(0,2) = jacTet(0,2);
    tmp(1,0) = jacTet(1,0); tmp(1,1) = jacTet(1,1); tmp(1,2) = jacTet(1,2);
    tmp(2,0) = jacTet(3,0); tmp(2,1) = jacTet(3,1); tmp(2,2) = jacTet(3,2);
    coeffMatrix(2,3) = -tmp.determinant() / sixVee;

    /* d4 */
    tmp(0,0) = jacTet(0,0); tmp(0,1) = jacTet(0,1); tmp(0,2) = jacTet(0,2);
    tmp(1,0) = jacTet(1,0); tmp(1,1) = jacTet(1,1); tmp(1,2) = jacTet(1,2);
    tmp(2,0) = jacTet(2,0); tmp(2,1) = jacTet(2,1); tmp(2,2) = jacTet(2,2);
    coeffMatrix(3,3) =  tmp.determinant() / sixVee;

    return coeffMatrix;
}


void applyMeshTransformation(   int volSizeZ,     int volSizeY,     int volSizeX,       float           * volGrey,     // image
                                int volSizeZ2,    int volSizeY2,    int volSizeX2,      unsigned int    * volLab,
                                int volSizeZ3,    int volSizeY3,    int volSizeX3,      float           * volOut,
                                int conneSize,    int connSizeTet,                      unsigned int    * conne,       // Connectivity Matrix      -- should be nTetrahedra * 4
                                int nodesSize,    int pTetSizeDim,                      double          * nodes,       // Tetrahedra Points        -- should be nNodes      * 3
                                int three,        int numberOfNodes,                    double          * displ        // Tetrahedra Displacement  -- should be nNodes      * 3
                    )
{
//     printf("interpolateMeshVoxels in C starting up\n");
    /* Safety checks */
    if ( connSizeTet != 4 || pTetSizeDim != 3 )
    {
        printf ("Did not get 4 nodes or 3 coords per node, exiting.\n");
        return;
    }

    #pragma omp parallel
    #pragma omp for
    /* Looping over all tetrahedra -- future parallelisation should be at this level. */
    for ( int nTet = 0; nTet < conneSize; nTet++ )
    {
//         if ( nTet%(conneSize/100) == 0) printf("\r\t(%2.1f%%) %i of %i", 100.0*(float)(nTet+1)/(float)conneSize, nTet+1, conneSize );

        /* create pTetArray Connectivity matrix and nodes List */
        Eigen::Matrix<float, 4, 3>         pTetMatrix;
        /* same as above for nodal displacements */
        Eigen::Matrix<float, 4, 3>         dispMatrix;
        for ( unsigned char i = 0; i < 4; i++ )
        {
          for ( unsigned char j = 0; j < 3; j++ )
          {
              unsigned int index_t = 3*conne[ 4*nTet+i ] + j;
              pTetMatrix(i,j) = nodes[ index_t ];
              dispMatrix(i,j) = displ[ index_t ];
          }
        }

        /* calculate Shape function coefficient matrix */
        Eigen::Matrix<float, 4, 4> coeffMatrix = shapeFunc( pTetMatrix );

        /* Find limits of the box defined by the extremities of the tetrahedron */
        double Zmin = volSizeZ;
        double Ymin = volSizeY;
        double Xmin = volSizeX;
        double Zmax = 0;
        double Ymax = 0;
        double Xmax = 0;

        for ( unsigned char i = 0; i < 4; i++ )
        {
          if ( Zmin > pTetMatrix(i,0) ) Zmin = MAX( pTetMatrix(i,0),      0     );
          if ( Zmax < pTetMatrix(i,0) ) Zmax = MIN( pTetMatrix(i,0), volSizeZ-1 );
          if ( Ymin > pTetMatrix(i,1) ) Ymin = MAX( pTetMatrix(i,1),      0     );
          if ( Ymax < pTetMatrix(i,1) ) Ymax = MIN( pTetMatrix(i,1), volSizeY-1 );
          if ( Xmin > pTetMatrix(i,2) ) Xmin = MAX( pTetMatrix(i,2),      0     );
          if ( Xmax < pTetMatrix(i,2) ) Xmax = MIN( pTetMatrix(i,2), volSizeX-1 );
        }



        /* Loop over the box defined by the extremities of the tetrahedron */
        for ( size_t Z = floor(Zmin); Z < ceil(Zmax); Z++ )
        {
            for ( size_t Y = floor(Ymin); Y < ceil(Ymax); Y++ )
            {
                for ( size_t X = floor(Xmin); X < ceil(Xmax); X++ )
                {
                    /* Build index for 3D access */
                    size_t index_i =   Z  * volSizeX * volSizeY   +   Y * volSizeX   +   X;

                    /* If our pixel is labelled with this tet number, then continue...*/
    //                 printf( "checking whether this pixel has the correct label at index_i = %i (%i %i %i) [%i %i %i].\n", index_i, Z, Y, X, volSizeZ, volSizeY, volSizeX  );
                    if ( volLab[ index_i ] == (unsigned int)nTet )
                    {
                        double dispPixRel[3];
                        dispPixRel[0] = 0.0; dispPixRel[1] = 0.0; dispPixRel[2] = 0.0;

                        /* Loop over nodes of this tetrahedron */
                        for ( unsigned short a=0; a < 4; a++ )
                        {
                            for ( unsigned short dim=0; dim < 3; dim++ )
                            {
                                dispPixRel[dim] += ( coeffMatrix(a,0)*1.0
                                                   + coeffMatrix(a,1)*(double)Z
                                                   + coeffMatrix(a,2)*(double)Y
                                                   + coeffMatrix(a,3)*(double)X ) * dispMatrix(a,dim);
                            }
                        }

                        /* this could be negative */
    //                     /* start only needed for nearest neighbour interpolation */
    //                     int displacedPosR[3];
    //                     displacedPosR[0] = round( (double)Z-dispPixRel[0] );
    //                     displacedPosR[1] = round( (double)Y-dispPixRel[1] );
    //                     displacedPosR[2] = round( (double)X-dispPixRel[2] );
    //                     /* end only needed for nearest neighbour interpolation */

                        int displacedPosF[3];
                        displacedPosF[0] = floor( (double)Z-dispPixRel[0] );
                        displacedPosF[1] = floor( (double)Y-dispPixRel[1] );
                        displacedPosF[2] = floor( (double)X-dispPixRel[2] );

                        double displacedPosRel[3];
                        displacedPosRel[0] = (double)Z-dispPixRel[0]-(double)displacedPosF[0];
                        displacedPosRel[1] = (double)Y-dispPixRel[1]-(double)displacedPosF[1];
                        displacedPosRel[2] = (double)X-dispPixRel[2]-(double)displacedPosF[2];


                        /* check if the position + rev displacement goes outside our data -- if so, do not interpolate and give this pixel 0.0 */
                        if (  displacedPosF[0] > 0 && displacedPosF[0] < (int)(volSizeZ-1) &&
                              displacedPosF[1] > 0 && displacedPosF[1] < (int)(volSizeY-1) &&
                              displacedPosF[2] > 0 && displacedPosF[2] < (int)(volSizeX-1)     )
                        {
    //                         /* nearest neighbour interpolation */
    //                         unsigned int index_disp =   displacedPosR[0]  * volSizeX * volSizeY   +   displacedPosR[1] * volSizeX   +   displacedPosR[2];
    //                         volOut[index_i] = volGrey[index_disp];
    //                         /* endnearest neighbour interpolation */

                            /* Trilinear interpolation see Eddy Phd page 128-129 */
                            double grey = 0.0;
                            double dZ, dY, dX;
                            for ( unsigned char z = 0; z <= 1; z++ )
                            {
                                for ( unsigned char y = 0; y <= 1; y++ )
                                {
                                    for ( unsigned char x = 0; x <= 1; x++ )
                                    {
                                        /* Build index for 3D access */
                                        size_t index_g =   (size_t)( z + displacedPosF[0] ) * volSizeX * volSizeY   +  (size_t)( y + displacedPosF[1] ) * volSizeX   +   (size_t)( x + displacedPosF[2] );

                                        /* switch cases for the corners of the cube */
                                        if ( z == 0) dZ = 1 - displacedPosRel[0];
                                        else         dZ =     displacedPosRel[0];
                                        if ( y == 0) dY = 1 - displacedPosRel[1];
                                        else         dY =     displacedPosRel[1];
                                        if ( x == 0) dX = 1 - displacedPosRel[2];
                                        else         dX =     displacedPosRel[2];

                                        /* Add recursively to current greyscale value */
                                        grey += volGrey[index_g]*dZ*dY*dX;
                                    }
                                }
                            }
                            volOut[index_i] = grey;
                            /* End Trilinear interpolation see Eddy Phd page 128-129 */
                        }
                        else
                        {
                            volOut[index_i] = 0.0;
                        }
                    }
                }
            }
        }
    }
}

Eigen::Matrix<float, 12, 12> elementaryMatrix( unsigned int * volLab, unsigned int volSizeZ,     unsigned int volSizeY, unsigned int volSizeX,   // image
                                               float * vol4DGrad,
                                               Eigen::Matrix<float, 4, 3> pTetMatrix, // 4*3 points of the tetrahedron
                                               int nTet )
{
    /* Initialise individual element matrix */
    Eigen::Matrix<float, 12, 12> Me;
    for ( unsigned char i = 0; i<12; i++ )
    {
        for ( unsigned char j = 0; j<12; j++ )
        {
            Me(i,j)=0;
        }
    }


    /* calculate Shape function coefficient matrix */
    Eigen::Matrix<float, 4, 4> coeffMatrix = shapeFunc( pTetMatrix );

    /* Find limits of the box defined by the extremities of the tetrahedron */
    double Zmin = volSizeZ;
    double Ymin = volSizeY;
    double Xmin = volSizeX;
    double Zmax = 0;
    double Ymax = 0;
    double Xmax = 0;

    for ( unsigned char i = 0; i < 4; i++ )
    {
      if ( Zmin > pTetMatrix(i,0) ) Zmin = MAX( pTetMatrix(i,0),      0     );
      if ( Zmax < pTetMatrix(i,0) ) Zmax = MIN( pTetMatrix(i,0), volSizeZ-1 );
      if ( Ymin > pTetMatrix(i,1) ) Ymin = MAX( pTetMatrix(i,1),      0     );
      if ( Ymax < pTetMatrix(i,1) ) Ymax = MIN( pTetMatrix(i,1), volSizeY-1 );
      if ( Xmin > pTetMatrix(i,2) ) Xmin = MAX( pTetMatrix(i,2),      0     );
      if ( Xmax < pTetMatrix(i,2) ) Xmax = MIN( pTetMatrix(i,2), volSizeX-1 );
    }

    /* Loop over the pixels of the box defined by the extremities of the tetrahedron */
    for ( size_t Z = floor(Zmin); Z < ceil(Zmax); Z++ )
    {
        for ( size_t Y = floor(Ymin); Y < ceil(Ymax); Y++ )
        {
            for ( size_t X = floor(Xmin); X < ceil(Xmax); X++ )
            {
                /* Build index for 3D access */
                size_t index_i =   Z  * volSizeX * volSizeY   +   Y * volSizeX   +   X;

                /* If our pixel is labelled with this tet number, then continue...*/
//                 printf( "checking whether this pixel has the correct label at index_i = %i (%i %i %i) [%i %i %i].\n", index_i, Z, Y, X, volSizeZ, volSizeY, volSizeX  );
                if ( volLab[ index_i ] == (unsigned int)nTet )
                {

                    /* Loop over the combinations of the nodes -- 4x4 loop, N.B. b=a to fill in the top symmetric part equation 2.2 (10) in g-dic.pdf */
                    /* Said differently the a and b subindices are the Me subindices on the right hand side of the = in equation 18 in g-dic.pdf */
                    for ( unsigned short a=0; a < 4; a++ )
                    {
//                         for ( unsigned short b=a; b < 4; b++ )
                        for ( unsigned short b=0; b < 4; b++ )
                        {
                            /* looping over dimensions in the submatrices of Me -- fx fy in equation 19 in g-dic.pdf */
                            for ( unsigned short alpha=0; alpha < 3; alpha++ )
                            {

                                for ( unsigned short beta=0; beta < 3; beta++ )
                                {
                                    double Na = ( coeffMatrix(a,0)*1.0 + coeffMatrix(a,1)*(double)Z + coeffMatrix(a,2)*(double)Y + coeffMatrix(a,3)*(double)X );
                                    double Nb = ( coeffMatrix(b,0)*1.0 + coeffMatrix(b,1)*(double)Z + coeffMatrix(b,2)*(double)Y + coeffMatrix(b,3)*(double)X );
                                    /* if you're crazy about performance put this in the loop above */
                                    /* create the access index to the 4D grad volume by adding an offset to the current poistion in the image */
                                    size_t indexGradAlpha = index_i + (size_t)( alpha * volSizeZ * volSizeY * volSizeX );
                                    size_t indexGradBeta  = index_i + (size_t)( beta  * volSizeZ * volSizeY * volSizeX );

                                    /* Look up the gradient in the alpha and beta direction * the shape function,
                                     * fill in the correct sub-me with an a and b offset */
                                    Me( 3 * a + alpha, 3 * b + beta ) += vol4DGrad[indexGradAlpha]*vol4DGrad[indexGradBeta]*Na*Nb;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return Me;
}



void computeDICglobalMatrix( int volSizeZ,   int volSizeY,   int volSizeX,   unsigned int  * volLabel,   // image
                   int four, int volSizeZ1,  int volSizeY1,  int volSizeX1,  float         * vol4DGrad,
                             int conneSize,  int connSizeTet,                unsigned int  * conne,      // Connectivity Matrix -- should be nTetrahedra * 4
                             int nodesSize,  int pTetSizeDim,                double        * nodes,      // Tetrahedra Points --   should be nNodes      * 3)
                             int dof1,       int dof2,                       float         * volOut)
{
    /* Safety checks */
    if ( connSizeTet != 4 || pTetSizeDim != 3 )
    {
        printf ("Did not get 4 nodes or 3 coords per node, exiting.\n");
        return;
    }

    /* Allocate global matrix*/
    const unsigned int dof = nodesSize*3;
//     Eigen::MatrixXf globalMatrix( dof, dof );
//     globalMatrix = Eigen::MatrixXf::Zero( dof, dof );

    // set ouput matrix to 0
    for (unsigned long i=0; i<(unsigned long)dof1*(unsigned long)dof2; i++)
    {
        volOut[i] = 0;
    }

    Eigen::Map<Eigen::MatrixXf> globalMatrix( volOut, dof, dof );

    #pragma omp parallel
    #pragma omp for
    /* Looping over all tetrahedra -- future parallelisation should be at this level. */
    for ( int nTet = 0; nTet < conneSize; nTet++ )
    {
//         if ( nTet%(conneSize/100) == 0) printf("\r\t(%2.1f%%) %i of %i", 100.0*(float)(nTet+1)/(float)conneSize, nTet+1, conneSize );

        /* create pTetArray Connectivity matrix and nodes List */
        Eigen::Matrix<float, 4, 3>         pTetMatrix;
        Eigen::Matrix<float, 4, 1>         nodeNumbers;
        /* same as above for nodal displacements */
        for ( unsigned char i = 0; i < 4; i++ )
        {
          /* record global convention node number for reassembly */
          nodeNumbers(i) = conne[ 4*nTet+i ];

          for ( unsigned char j = 0; j < 3; j++ )
          {
              unsigned int index_t = 3*conne[ 4*nTet+i ] + j;
              pTetMatrix(i,j) = nodes[ index_t ];
          }
        }

//         std::cout << nodeNumbers << std::endl;
//         printf( "\n\n" );


        /* Call elementary function and print result for now */
        Eigen::Matrix<float, 12, 12>Me = elementaryMatrix(  volLabel, volSizeZ, volSizeY, volSizeX,
                                                            vol4DGrad,
                                                            pTetMatrix,
                                                            nTet);


        /* Add this into the global matrix, looking up node numbers */
        /* Loop over the combinations of the nodes -- 4x4 loop, N.B. b=a to fill in the top symmetric part equation 2.2 (10) in g-dic.pdf */
        /* Said differently the a and b subindices are the Me subindices on the right hand side of the = in equation 18 in g-dic.pdf */
        for ( unsigned short a=0; a < 4; a++ )
        {
            for ( unsigned short b=0; b < 4; b++ )
            {
                unsigned int nodeA = nodeNumbers(a);
                unsigned int nodeB = nodeNumbers(b);
                globalMatrix.block<3,3>( nodeA * 3, nodeB * 3 ) += Me.block<3,3>( 3 * a, 3 * b );
            }
        }
    }


//     std::cout << globalMatrix << std::endl;
//     printf( "\n\n" );
}




Eigen::Matrix<float, 12, 1> elementaryVector(  unsigned int * volLab, unsigned int volSizeZ,     unsigned int volSizeY, unsigned int volSizeX,   // image
                                               float * vol4DGrad,
                                               float * vol1,
                                               float * vol2,
                                               Eigen::Matrix<float, 4, 3> pTetMatrix, // 4*3 points of the tetrahedron
                                               int nTet )
{
    /* Initialise individual element matrix */
    Eigen::Matrix<float, 12, 1> Fe;
    for ( unsigned char i = 0; i<12; i++ ) Fe(i)=0;

    /* calculate Shape function coefficient matrix */
    Eigen::Matrix<float, 4, 4> coeffMatrix = shapeFunc( pTetMatrix );

    /* Find limits of the box defined by the extremities of the tetrahedron */
    double Zmin = volSizeZ;
    double Ymin = volSizeY;
    double Xmin = volSizeX;
    double Zmax = 0;
    double Ymax = 0;
    double Xmax = 0;

    for ( unsigned char i = 0; i < 4; i++ )
    {
      if ( Zmin > pTetMatrix(i,0) ) Zmin = MAX( pTetMatrix(i,0),      0     );
      if ( Zmax < pTetMatrix(i,0) ) Zmax = MIN( pTetMatrix(i,0), volSizeZ-1 );
      if ( Ymin > pTetMatrix(i,1) ) Ymin = MAX( pTetMatrix(i,1),      0     );
      if ( Ymax < pTetMatrix(i,1) ) Ymax = MIN( pTetMatrix(i,1), volSizeY-1 );
      if ( Xmin > pTetMatrix(i,2) ) Xmin = MAX( pTetMatrix(i,2),      0     );
      if ( Xmax < pTetMatrix(i,2) ) Xmax = MIN( pTetMatrix(i,2), volSizeX-1 );
    }

    /* Loop over the pixels of the box defined by the extremities of the tetrahedron */
    for ( size_t Z = floor(Zmin); Z < ceil(Zmax); Z++ )
    {
        for ( size_t Y = floor(Ymin); Y < ceil(Ymax); Y++ )
        {
            for ( size_t X = floor(Xmin); X < ceil(Xmax); X++ )
            {
                /* Build index for 3D access */
                size_t index_i =   Z  * volSizeX * volSizeY   +   Y * volSizeX   +   X;

                /* If our pixel is labelled with this tet number, then continue...*/
//                 printf( "checking whether this pixel has the correct label at index_i = %i (%i %i %i) [%i %i %i].\n", index_i, Z, Y, X, volSizeZ, volSizeY, volSizeX  );
                if ( volLab[ index_i ] == (unsigned int)nTet )
                {

                    /* Loop over the combinations of the nodes -- 4x4 loop, N.B. b=a to fill in the top symmetric part equation 2.2 (10) in g-dic.pdf */
                    /* Said differently the a and b subindices are the Me subindices on the right hand side of the = in equation 18 in g-dic.pdf */
                    for ( unsigned short a=0; a < 4; a++ )
                    {
                        /* looping over dimensions in the submatrices of Me -- fx fy in equation 19 in g-dic.pdf */
                        for ( unsigned short alpha=0; alpha < 3; alpha++ )
                        {
                            double Na = ( coeffMatrix(a,0)*1.0 + coeffMatrix(a,1)*(double)Z + coeffMatrix(a,2)*(double)Y + coeffMatrix(a,3)*(double)X );
                            /* if you're crazy about performance put this in the loop above */
                            /* create the access index to the 4D grad volume by adding an offset to the current poistion in the image */
                            unsigned long indexGradAlpha = index_i + ( alpha * volSizeZ * volSizeY * volSizeX );

                            /* Look up the gradient in the alpha and beta direction * the shape function,
                              * fill in the correct sub-me with an a and b offset */
                            Fe( 3 * a + alpha ) += ( vol1[ index_i ] - vol2[ index_i ] ) * Na * vol4DGrad[ indexGradAlpha ];
                        }

                    }
                }
            }
        }
    }

//     std::cout << Fe << std::endl;
    return Fe;
}




void computeDICglobalVector( int volSizeZ,   int volSizeY,   int volSizeX,   unsigned int  * volLabel,    // image
                   int four, int volSizeZ1,  int volSizeY1,  int volSizeX1,  float         * vol4DGrad,
                             int volSizeZ2,  int volSizeY2,  int volSizeX2,  float         * vol1,        // numerically deformed image 1
                             int volSizeZ3,  int volSizeY3,  int volSizeX3,  float         * vol2,        // physically  deformed image 2 -- we want image 1 to look like image 2
                             int conneSize,  int connSizeTet,                unsigned int  * conne,       // Connectivity Matrix -- should be nTetrahedra * 4
                             int nodesSize,  int pTetSizeDim,                double        * nodes,       // Tetrahedra Points --   should be nNodes      * 3)
                             int dof3,                                       float         * vecOut )
{
    /* Safety checks */
    if ( connSizeTet != 4 || pTetSizeDim != 3 )
    {
        printf ("Did not get 4 nodes or 3 coords per node, exiting.\n");
        return;
    }

    // set ouput matrix to 0
    for (int i=0; i<dof3; i++)
    {
        vecOut[i] = 0;
    }

    /* Allocate global matrix*/
    const unsigned int dof = nodesSize*3;

    Eigen::Map<Eigen::MatrixXf> globalVector( vecOut, dof, 1 );

    #pragma omp parallel
    #pragma omp for
    /* Looping over all tetrahedra -- future parallelisation should be at this level. */
    for ( int nTet = 0; nTet < conneSize; nTet++ )
    {
//         if ( nTet%(conneSize/100) == 0) printf("\r\t(%2.1f%%) %i of %i", 100.0*(float)(nTet+1)/(float)conneSize, nTet+1, conneSize );

        /* create pTetArray Connectivity matrix and nodes List */
        Eigen::Matrix<float, 4, 3>         pTetMatrix;
        Eigen::Matrix<float, 4, 1>         nodeNumbers;
        /* same as above for nodal displacements */
        for ( unsigned char i = 0; i < 4; i++ )
        {
          /* record global convention node number for reassembly */
          nodeNumbers(i) = conne[ 4*nTet+i ];

          for ( unsigned char j = 0; j < 3; j++ )
          {
              unsigned int index_t = 3*conne[ 4*nTet+i ] + j;
              pTetMatrix(i,j) = nodes[ index_t ];
          }
        }

//         std::cout << nodeNumbers << std::endl;
//         printf( "\n\n" );


        /* Call elementary function and print result for now */
        Eigen::Matrix<float, 12, 1>Fe = elementaryVector(  volLabel, volSizeZ, volSizeY, volSizeX,
                                                           vol4DGrad,
                                                           vol1,
                                                           vol2,
                                                           pTetMatrix,
                                                           nTet);


        /* Add this into the global matrix, looking up node numbers */
        /* Loop over the combinations of the nodes -- 4x4 loop, N.B. b=a to fill in the top symmetric part equation 2.2 (10) in g-dic.pdf */
        /* Said differently the a and b subindices are the Me subindices on the right hand side of the = in equation 18 in g-dic.pdf */
        for ( unsigned short a=0; a < 4; a++ )
        {
            unsigned int nodeA = nodeNumbers(a);
            globalVector( nodeA * 3 + 0 ) += Fe( 3 * a + 0 );
            globalVector( nodeA * 3 + 1 ) += Fe( 3 * a + 1 );
            globalVector( nodeA * 3 + 2 ) += Fe( 3 * a + 2 );
        }
    }

}
