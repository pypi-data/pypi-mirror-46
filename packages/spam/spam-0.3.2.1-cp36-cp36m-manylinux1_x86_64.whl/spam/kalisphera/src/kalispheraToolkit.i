/* File: kalispheraToolkit.i */

%module kalispheraToolkit

%{
#define SWIG_FILE_WITH_INIT
#include "kalisphera.hpp"
%}


%include "numpy.i"

%init %{
import_array();
%}

/* WARNING, these names here must be exactly the same as the hpp file (not necessarily the cpp) */
%apply (int DIM1, int DIM2, int DIM3,            real_t         * INPLACE_ARRAY3){ ( int kalisphera_volSizeZ,            int kalisphera_volSizeY,            int kalisphera_volSizeX,          real_t*         kalisphera_vol                ) };
%apply (int DIM1,                                real_t         * IN_ARRAY1     ){ ( int kalisphera_three,                                                                                     real_t*         kalisphera_sphereCenterCoords ) };


%include "kalisphera.hpp"
