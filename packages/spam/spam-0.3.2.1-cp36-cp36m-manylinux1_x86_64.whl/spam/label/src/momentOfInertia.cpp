#include <stdio.h>
#include <math.h>
#include <iostream>
#include "labelToolkitC.hpp"
#include <Eigen/Dense>

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

void momentOfInertia(  int volSizeZ,    int volSizeY, int volSizeX,  labels::label* volLab,   
                       int maxLabelBB,  int sixBB,                  unsigned short* boundingBoxes,
                       int maxLabelCM,  int threeCM,                         float* centresOfMass,
                       int maxLabelMI1, int threeMI1,                        float* momentOfInertiaEigenValues,
                       int maxLabelMI2, int nineMI2,                         float* momentOfInertiaEigenVectors
                    )
{

  /*###############################################################
    ### Step 3 Calculate the moment of inertia...
    ############################################################### */

    for ( labels::label label = 0; label < (labels::label)maxLabelBB; label++ )
    {
        Eigen::Matrix3d inertiaE;
        inertiaE << 0,0,0, 0,0,0, 0,0,0;

//         printf( "\r\tMoment of inertia progress: \t%02.1f%%\t", 100 * (float)label / (float)(maxLabelBB-1) );

        for ( size_t z = boundingBoxes[ 6*label ]; z <= boundingBoxes[ 6*label+1 ]; z++ )
        {

            for ( size_t y = boundingBoxes[ 6*label+2 ]; y <= boundingBoxes[ 6*label+3 ]; y++ )
            {
                for ( size_t x = boundingBoxes[ 6*label+4 ]; x <= boundingBoxes[ 6*label+5 ]; x++ )
                {
                    size_t index_i = z  * volSizeX * volSizeY   +   y * volSizeX   +   x;

                    labels::label pixelValue = volLab[ index_i ];

                    if ( pixelValue == label )
                    {

                        Eigen::Vector3d rE;

                        rE( 0 ) = (float)z - centresOfMass[ 3*label+0 ];
                        rE( 1 ) = (float)y - centresOfMass[ 3*label+1 ];
                        rE( 2 ) = (float)x - centresOfMass[ 3*label+2 ];

                        double innerTemp = rE.dot(rE);

                        Eigen::Matrix3d innerMatrix;
                        innerMatrix << innerTemp,0,0, 0,innerTemp,0, 0,0,innerTemp;

                        inertiaE += innerMatrix - rE*rE.transpose();

//                         std::cout << innerMatrix << std::endl;
//                         printf("\n");
//                         printf("\n");
//                         printf("\n");
                    }
                }
            }
        }

        Eigen::SelfAdjointEigenSolver<Eigen::Matrix3d> eigenSolver( inertiaE );

//         std::cout << eigenSolver.eigenvalues() << std::endl;
//         std::cout << eigenSolver.eigenvectors() << std::endl;

        /* write, flattened, into output array */
        // eigenValue 1,2,3, they appear to be sorted...

        momentOfInertiaEigenValues[3*label+0] = eigenSolver.eigenvalues()(2);
        momentOfInertiaEigenValues[3*label+1] = eigenSolver.eigenvalues()(1);
        momentOfInertiaEigenValues[3*label+2] = eigenSolver.eigenvalues()(0);

        //eigenvectors 1,2,3... check they are not duff
        if ( momentOfInertiaEigenValues[3*label+0] == 0 && momentOfInertiaEigenValues[3*label+1] == 0 && momentOfInertiaEigenValues[3*label+2] == 0 )
        {
            momentOfInertiaEigenVectors[9*label+0] = 0;
            momentOfInertiaEigenVectors[9*label+1] = 0;
            momentOfInertiaEigenVectors[9*label+2] = 0;
            momentOfInertiaEigenVectors[9*label+3] = 0;
            momentOfInertiaEigenVectors[9*label+4] = 0;
            momentOfInertiaEigenVectors[9*label+5] = 0;
            momentOfInertiaEigenVectors[9*label+6] = 0;
            momentOfInertiaEigenVectors[9*label+7] = 0;
            momentOfInertiaEigenVectors[9*label+8] = 0;
        }
        else
        {
            momentOfInertiaEigenVectors[9*label+0] = eigenSolver.eigenvectors()(0,2);
            momentOfInertiaEigenVectors[9*label+1] = eigenSolver.eigenvectors()(1,2);
            momentOfInertiaEigenVectors[9*label+2] = eigenSolver.eigenvectors()(2,2);
            momentOfInertiaEigenVectors[9*label+3] = eigenSolver.eigenvectors()(0,1);
            momentOfInertiaEigenVectors[9*label+4] = eigenSolver.eigenvectors()(1,1);
            momentOfInertiaEigenVectors[9*label+5] = eigenSolver.eigenvectors()(2,1);
            momentOfInertiaEigenVectors[9*label+6] = eigenSolver.eigenvectors()(0,0);
            momentOfInertiaEigenVectors[9*label+7] = eigenSolver.eigenvectors()(1,0);
            momentOfInertiaEigenVectors[9*label+8] = eigenSolver.eigenvectors()(2,0);
        }

    }
//     printf( "\n" );
}


