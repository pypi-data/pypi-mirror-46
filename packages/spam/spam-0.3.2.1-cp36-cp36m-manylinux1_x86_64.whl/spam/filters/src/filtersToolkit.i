/* File: filtersToolkit.i */

%module filtersToolkit

%{
#define SWIG_FILE_WITH_INIT
#include "movingFiltersToolkit.hpp"
%}

%include "numpy.i"

%init %{
import_array();
%}

/* WARNING, these names here must be exactly the same as the hpp file (not necessarily the cpp) */
%apply (int DIM1, int DIM2, int DIM3, float* IN_ARRAY3)      { ( int av_nz1, int av_ny1, int av_nx1, float *av_imIn ) };
%apply (int DIM1, int DIM2, int DIM3, float* INPLACE_ARRAY3) { ( int av_nz2, int av_ny2, int av_nx2, float *av_imOu ) };
%apply (int DIM1, int DIM2, int DIM3, float* IN_ARRAY3)      { ( int av_nz3, int av_ny3, int av_nx3, float *av_stEl ) };

%apply (int DIM1, int DIM2, int DIM3, float* IN_ARRAY3)      { ( int var_nz1, int var_ny1, int var_nx1, float *var_imIn ) };
%apply (int DIM1, int DIM2, int DIM3, float* INPLACE_ARRAY3) { ( int var_nz2, int var_ny2, int var_nx2, float *var_imOu ) };
%apply (int DIM1, int DIM2, int DIM3, float* IN_ARRAY3)      { ( int var_nz3, int var_ny3, int var_nx3, float *var_stEl ) };

%apply (int DIM1, int DIM2, int DIM3, float* IN_ARRAY3)      { ( int hess_nz1,    int hess_ny1,     int hess_nx1, float *hess_hzz ),
                                                               ( int hess_nz2,    int hess_ny2,     int hess_nx2, float *hess_hzy ),
                                                               ( int hess_nz3,    int hess_ny3,     int hess_nx3, float *hess_hzx ),
                                                               ( int hess_nz4,    int hess_ny4,     int hess_nx4, float *hess_hyz ),
                                                               ( int hess_nz5,    int hess_ny5,     int hess_nx5, float *hess_hyy ),
                                                               ( int hess_nz6,    int hess_ny6,     int hess_nx6, float *hess_hyx ),
                                                               ( int hess_nz7,    int hess_ny7,     int hess_nx7, float *hess_hxz ),
                                                               ( int hess_nz8,    int hess_ny8,     int hess_nx8, float *hess_hxy ),
                                                               ( int hess_nz9,    int hess_ny9,     int hess_nx9, float *hess_hxx ) };
%apply (int DIM1, int DIM2, int DIM3, float* INPLACE_ARRAY3) { ( int hess_nz10,   int hess_ny10,    int hess_nx10, float *hess_valA  ),
                                                               ( int hess_nz11,   int hess_ny11,    int hess_nx11, float *hess_valB  ),
                                                               ( int hess_nz12,   int hess_ny12,    int hess_nx12, float *hess_valC  ),
                                                               ( int hess_nz13,   int hess_ny13,    int hess_nx13, float *hess_valAz ),
                                                               ( int hess_nz14,   int hess_ny14,    int hess_nx14, float *hess_valAy ),
                                                               ( int hess_nz15,   int hess_ny15,    int hess_nx15, float *hess_valAx ),
                                                               ( int hess_nz16,   int hess_ny16,    int hess_nx16, float *hess_valBz ),
                                                               ( int hess_nz17,   int hess_ny17,    int hess_nx17, float *hess_valBy ),
                                                               ( int hess_nz18,   int hess_ny18,    int hess_nx18, float *hess_valBx ),
                                                               ( int hess_nz19,   int hess_ny19,    int hess_nx19, float *hess_valCz ),
                                                               ( int hess_nz20,   int hess_ny20,    int hess_nx20, float *hess_valCy ),
                                                               ( int hess_nz21,   int hess_ny21,    int hess_nx21, float *hess_valCx ) };

%include "movingFiltersToolkit.hpp"
