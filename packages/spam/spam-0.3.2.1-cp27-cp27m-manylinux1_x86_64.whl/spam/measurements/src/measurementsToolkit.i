/* File: measurementsToolkit.i */

%module measurementsToolkit

%{
#define SWIG_FILE_WITH_INIT
#include "correlationFunction.hpp"
#include "curvatures.hpp"
#include "porosityField.hpp"
%}

%include "numpy.i"
%include "std_vector.i"

%template(VectorFloat)   std::vector<float>;
%template(VectorVectorFloat)   std::vector<std::vector<float> >;
%template(VectorDouble)   std::vector<double>;
%template(VectorVectorDouble)   std::vector<std::vector<double> >;
%template(VectorUnsigned)   std::vector<unsigned int>;
%template(VectorVectorUnsigned)   std::vector<std::vector<unsigned int> >;

%init %{
import_array();
%}

/* WARNING, these names here must be exactly the same as the hpp file (not necessarily the cpp) */

%apply (float*  IN_ARRAY3, int DIM1, int DIM2, int DIM3)  { ( float * vol,    unsigned int volSizeZ,   unsigned int volSizeY,   unsigned int volSizeX ) };
%apply (double* INPLACE_ARRAY2, int DIM1, int DIM2)  { ( double *output, unsigned int outputSize, unsigned int outputTwo ) };
%apply (int DIM3)  { ( unsigned int StepCenter ) };
%apply (int DIM3)  { ( unsigned int nthreads ) };


%apply (int DIM1, int DIM2, int DIM3,    unsigned char         * IN_ARRAY3)     { (              int porosityFieldBinaryVolSizeZ,        int porosityFieldBinaryVolSizeY,        int porosityFieldBinaryVolSizeX, unsigned char*         porosityFieldBinaryVol            ) };
%apply (int DIM1, int DIM2,                        int         * IN_ARRAY2)     { (              int porosityFieldBinaryN,               int porosityFieldBinaryThree,                                                      int*         porosityFieldBinaryPos            ) };
%apply (int DIM1,                                  int         * IN_ARRAY1)     { (              int porosityFieldBinaryNtwo,                                                                                               int*         porosityFieldBinaryHws            ) };
%apply (int DIM1,                                float         * INPLACE_ARRAY1){ (              int porosityFieldBinaryNthree,                                                                                           float*         porosityFieldBinaryOut            ) };

%include "correlationFunction.hpp"
%include "porosityField.hpp"
%include "curvatures.hpp"
