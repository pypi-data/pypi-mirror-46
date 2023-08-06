#include <stdio.h>
#include <math.h>
#include <cmath>
#include <iostream>
//#include <stdlib.h> /* abs */
#include "movingFiltersToolkit.hpp"
#include <Eigen/Dense>

/* 2017-05-23 Emmanuel Roubin
 *

 */

/*              Image sizes, ZYX and images*/
void average(   int nz1,   int ny1,  int nx1, float* imIn,\
                int nz2,   int ny2,  int nx2, float* imOu,\
                int nz3,   int ny3,  int nx3, float* stEl )
{
  // int variable to build index to 1D-images from x,y,z coordinates

  // get the box of the image
  unsigned zMin = nz3/2; unsigned zMax = nz1-nz3/2;
  unsigned yMin = ny3/2; unsigned yMax = ny1-ny3/2;
  unsigned xMin = nx3/2; unsigned xMax = nx1-nx3/2;

  // std::cout << "START C++ moving average" << std::endl;
  // std::cout << "z range: " << zMin << " - " << zMax << std::endl;
  // std::cout << "y range: " << yMin << " - " << yMax << std::endl;
  // std::cout << "x range: " << xMin << " - " << xMax << std::endl;


  /* loop over the structural element to get the sum */
  unsigned idSt = 0;
  float stEl_sum = 0.0;
  for( int k=-nz3/2; k<=nz3/2; k++ ) {
    for( int j=-ny3/2; j<=ny3/2; j++ ) {
      for( int i=-nx3/2; i<=nx3/2; i++ ) {
    stEl_sum += stEl[ idSt ];
    idSt++;
      }
    }
  }
  
  // loop over the image
  for( unsigned z=zMin; z<zMax; z++ ) {
    for( unsigned y=yMin; y<yMax; y++ ) {
      for( unsigned x=xMin; x<xMax; x++ ) {

    // index of output image
    unsigned idImOu = z * ny1 * nx1 + y * nx1 + x;

    // tmp voxel values of the output and
    float im_sum = 0.0;
    //float im_sum2 = 0.0;

    // loop over the structural element
    unsigned idSt = 0;
    for( int k=-nz3/2; k<=nz3/2; k++ ) {
      for( int j=-ny3/2; j<=ny3/2; j++ ) {
        for( int i=-nx3/2; i<=nx3/2; i++ ) {
          unsigned idImIn = ( z+k ) * ny1 * nx1 + ( y+j ) * nx1 + ( x+i );
          im_sum += stEl[ idSt ] * imIn[ idImIn ];
          //im_sum2 += (stEl[ idSt ] * imIn[ idImIn ])*(stEl[ idSt ] * imIn[ idImIn ]);
          idSt++;
        }
      }
    }

    imOu[ idImOu ] = im_sum/stEl_sum;
    //imOu[ idImOu ] = (im_sum2 - im_sum * im_sum/stEl_sum)/stEl_sum;

      }
    }
  }

  //std::cout << "STOP C++ moving average" << std::endl;
}


//int  sgn(double d){
  // float eps = 0.0000000000000000000001;
  // return d<-eps?-1:d>eps;
  // }


void variance(  int nz1,   int ny1,  int nx1, float* imIn,    \
                int nz2,   int ny2,  int nx2, float* imOu,    \
                int nz3,   int ny3,  int nx3, float* stEl )
{
  // int variable to build index to 1D-images from x,y,z coordinates

  // get the box of the image
  unsigned zMin = nz3/2; unsigned zMax = nz1-nz3/2;
  unsigned yMin = ny3/2; unsigned yMax = ny1-ny3/2;
  unsigned xMin = nx3/2; unsigned xMax = nx1-nx3/2;

  // std::cout << "\nSTART C++ moving variance" << std::endl;
  // std::cout << "z range: " << zMin << " - " << zMax << std::endl;
  // std::cout << "y range: " << yMin << " - " << yMax << std::endl;
  // std::cout << "x range: " << xMin << " - " << xMax << std::endl;


  /* loop over the structural element to get the sum */
  unsigned idSt = 0;
  float stEl_sum = 0.0;
  for( int k=-nz3/2; k<=nz3/2; k++ ) {
    for( int j=-ny3/2; j<=ny3/2; j++ ) {
      for( int i=-nx3/2; i<=nx3/2; i++ ) {
    stEl_sum += stEl[ idSt ];
    idSt++;
      }
    }
  }

  // loop over the image
  for( unsigned z=zMin; z<zMax; z++ ) {
    for( unsigned y=yMin; y<yMax; y++ ) {
      for( unsigned x=xMin; x<xMax; x++ ) {

    // index of output image
    unsigned idImOu = z * ny1 * nx1 + y * nx1 + x;

    // tmp voxel values of the output and
    float im_sum = 0.0;
    float im_sum2 = 0.0;

    // loop over the structural element
    unsigned idSt = 0;
    for( int k=-nz3/2; k<=nz3/2; k++ ) {
      for( int j=-ny3/2; j<=ny3/2; j++ ) {
        for( int i=-nx3/2; i<=nx3/2; i++ ) {
          unsigned idImIn = ( z+k ) * ny1 * nx1 + ( y+j ) * nx1 + ( x+i );
          im_sum += stEl[ idSt ] * imIn[ idImIn ];
          im_sum2 += (stEl[ idSt ] * imIn[ idImIn ])*(stEl[ idSt ] * imIn[ idImIn ]);
          idSt++;
        }
      }
    }

    imOu[ idImOu ] = (im_sum2 - im_sum * im_sum/stEl_sum)/stEl_sum;
      }
    }
  }

  // std::cout << "STOP C++ moving variance" << std::endl;
  // std::cout << "abs(-min) = " << std::abs(-4.62e-07) << std::endl;
  // std::cout << " \n*** that was Olga's 1rst C++ function :) " << std::endl;
}


void hessian(   int nz1,    int ny1,     int nx1,  float *hzz,
                int nz2,    int ny2,     int nx2,  float *hzy,
                int nz3,    int ny3,     int nx3,  float *hzx,
                int nz4,    int ny4,     int nx4,  float *hyz,
                int nz5,    int ny5,     int nx5,  float *hyy,
                int nz6,    int ny6,     int nx6,  float *hyx,
                int nz7,    int ny7,     int nx7,  float *hxz,
                int nz8,    int ny8,     int nx8,  float *hxy,
                int nz9,    int ny9,     int nx9,  float *hxx,
                int nz10,   int ny10,    int nx10, float *valA,
                int nz11,   int ny11,    int nx11, float *valB,
                int nz12,   int ny12,    int nx12, float *valC,
                int nz13,   int ny13,    int nx13, float *valAz,
                int nz14,   int ny14,    int nx14, float *valAy,
                int nz15,   int ny15,    int nx15, float *valAx,
                int nz16,   int ny16,    int nx16, float *valBz,
                int nz17,   int ny17,    int nx17, float *valBy,
                int nz18,   int ny18,    int nx18, float *valBx,
                int nz19,   int ny19,    int nx19, float *valCz,
                int nz20,   int ny20,    int nx20, float *valCy,
                int nz21,   int ny21,    int nx21, float *valCx  )
{
    int nPoints = nz1 * ny1 * nx1;

    long int n = 0;

    for ( n=0; n<nPoints; n++ )
    {
        Eigen::Matrix3d inertiaE;
        inertiaE << hzz[n], hzy[n], hzx[n],
                    hyz[n], hyy[n], hyx[n],
                    hxz[n], hxy[n], hxx[n];
        Eigen::SelfAdjointEigenSolver<Eigen::Matrix3d> eigenSolver( inertiaE );
        valA[n] = eigenSolver.eigenvalues()(2);
        valB[n] = eigenSolver.eigenvalues()(1);
        valC[n] = eigenSolver.eigenvalues()(0);
        //eigenvectors 1,2,3...
        valAz[n] = eigenSolver.eigenvectors()(0,2);
        valAy[n] = eigenSolver.eigenvectors()(1,2);
        valAx[n] = eigenSolver.eigenvectors()(2,2);
        valBz[n] = eigenSolver.eigenvectors()(0,1);
        valBy[n] = eigenSolver.eigenvectors()(1,1);
        valBx[n] = eigenSolver.eigenvectors()(2,1);
        valCz[n] = eigenSolver.eigenvectors()(0,0);
        valCy[n] = eigenSolver.eigenvectors()(1,0);
        valCx[n] = eigenSolver.eigenvectors()(2,0);
    }
}
