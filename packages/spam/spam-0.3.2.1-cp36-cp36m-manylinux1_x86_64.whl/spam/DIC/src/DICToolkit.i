/* File: DICToolkit.i */

%module DICToolkit

%{
#define SWIG_FILE_WITH_INIT
#include "computeDICoperators.hpp"
#include "applyPhiC.hpp"
#include "binning.hpp"
#include "pixelSearchGC.hpp"
#include "computeGMresidualAndPhase.hpp"
%}


%include "numpy.i"

%init %{
import_array();
%}

/* WARNING, these names here must be exactly the same as the hpp file (not necessarily the cpp) */
%apply (int DIM1, int DIM2, int DIM3,            float         * IN_ARRAY3)     { (              int computeDICoperators_nz1,            int computeDICoperators_ny1,            int computeDICoperators_nx1,          float*         computeDICoperators_im1                ),
                                                                                  (              int computeDICoperators_nz2,            int computeDICoperators_ny2,            int computeDICoperators_nx2,          float*         computeDICoperators_im2                ),
                                                                                  (              int computeDICoperators_nz2gz,          int computeDICoperators_ny2gz,          int computeDICoperators_nx2gz,        float*         computeDICoperators_im2gz              ),
                                                                                  (              int computeDICoperators_nz2gy,          int computeDICoperators_ny2gy,          int computeDICoperators_nx2gy,        float*         computeDICoperators_im2gy              ),
                                                                                  (              int computeDICoperators_nz2gx,          int computeDICoperators_ny2gx,          int computeDICoperators_nx2gx,        float*         computeDICoperators_im2gx              ) };
%apply (int DIM1, int DIM2,                      float         * INPLACE_ARRAY2){ (              int computeDICoperators_twelve1,        int computeDICoperators_twelve2,                                              float*         computeDICoperators_M                  ) };
%apply (int DIM1,                                float         * INPLACE_ARRAY1){ (              int computeDICoperators_twelve3,                                                                                      float*         computeDICoperators_A                  ) };
%apply (int DIM1, int DIM2, int DIM3,            float         * IN_ARRAY3)     { (              int computeDICoperators_cz1,            int computeDICoperators_cy1,            int computeDICoperators_cx1,          float*         computeDICoperators_c1                 ) };


%apply (int DIM1, int DIM2, int DIM3,            float         * IN_ARRAY3)     { (              int computeDICoperatorsGM_nz1,          int computeDICoperatorsGM_ny1,          int computeDICoperatorsGM_nx1,        float*         computeDICoperatorsGM_im1              ),
                                                                                  (              int computeDICoperatorsGM_nz2,          int computeDICoperatorsGM_ny2,          int computeDICoperatorsGM_nx2,        float*         computeDICoperatorsGM_im2              ),
                                                                                  (              int computeDICoperatorsGM_nz2gz,        int computeDICoperatorsGM_ny2gz,        int computeDICoperatorsGM_nx2gz,      float*         computeDICoperatorsGM_im2gz            ),
                                                                                  (              int computeDICoperatorsGM_nz2gy,        int computeDICoperatorsGM_ny2gy,        int computeDICoperatorsGM_nx2gy,      float*         computeDICoperatorsGM_im2gy            ),
                                                                                  (              int computeDICoperatorsGM_nz2gx,        int computeDICoperatorsGM_ny2gx,        int computeDICoperatorsGM_nx2gx,      float*         computeDICoperatorsGM_im2gx            ) };
%apply (int DIM1, int DIM2,                      float         * IN_ARRAY2)     { (              int computeDICoperatorsGM_nPeaks,       int computeDICoperatorsGM_six,                                                float*         computeDICoperatorsGM_peaks            ) };
%apply (int DIM1, int DIM2,                      unsigned char * IN_ARRAY2)     { (              int computeDICoperatorsGM_binsF,        int computeDICoperatorsGM_binsG,                                              unsigned char* computeDICoperatorsGM_phases           ) };
%apply (int DIM1, int DIM2,                      float         * INPLACE_ARRAY2){ (              int computeDICoperatorsGM_twelve1,      int computeDICoperatorsGM_twelve2,                                            float*         computeDICoperatorsGM_M                ) };
%apply (int DIM1,                                float         * INPLACE_ARRAY1){ (              int computeDICoperatorsGM_twelve3,                                                                                    float*         computeDICoperatorsGM_A                ) };

%apply (int DIM1, int DIM2, int DIM3,            float         * IN_ARRAY3)     { (              int computeDICoperatorsLL_nz1,          int computeDICoperatorsLL_ny1,          int computeDICoperatorsLL_nx1,        float*         computeDICoperatorsLL_im1              ),
                                                                                  (              int computeDICoperatorsLL_nz2,          int computeDICoperatorsLL_ny2,          int computeDICoperatorsLL_nx2,        float*         computeDICoperatorsLL_im2              ),
                                                                                  (              int computeDICoperatorsLL_nz2gz,        int computeDICoperatorsLL_ny2gz,        int computeDICoperatorsLL_nx2gz,      float*         computeDICoperatorsLL_im2gz            ),
                                                                                  (              int computeDICoperatorsLL_nz2gy,        int computeDICoperatorsLL_ny2gy,        int computeDICoperatorsLL_nx2gy,      float*         computeDICoperatorsLL_im2gy            ),
                                                                                  (              int computeDICoperatorsLL_nz2gx,        int computeDICoperatorsLL_ny2gx,        int computeDICoperatorsLL_nx2gx,      float*         computeDICoperatorsLL_im2gx            ) };
%apply (int DIM1, int DIM2,                      float         * IN_ARRAY2)     { (              int computeDICoperatorsLL_nBinsA,       int computeDICoperatorsLL_nBinsB,                                             float*         computeDICoperatorsLL_jointHistGrad1   ),
                                                                                  (              int computeDICoperatorsLL_nBinsC,       int computeDICoperatorsLL_nBinsD,                                             float*         computeDICoperatorsLL_jointHistGrad2   ) };
%apply (int DIM1, int DIM2,                      float         * INPLACE_ARRAY2){ (              int computeDICoperatorsLL_twelve1,      int computeDICoperatorsLL_twelve2,                                            float*         computeDICoperatorsLL_M                ) };
%apply (int DIM1,                                float         * INPLACE_ARRAY1){ (              int computeDICoperatorsLL_twelve3,                                                                                    float*         computeDICoperatorsLL_A                ) };


%apply (int DIM1, int DIM2, int DIM3,            unsigned   int* IN_ARRAY3)     { (              int computeDICglobalMatrix_nz1,         int computeDICglobalMatrix_ny1,         int computeDICglobalMatrix_nx1,       unsigned int*  computeDICglobalMatrix_volLabel        ) };
%apply (int DIM1, int DIM2, int DIM3, int DIM4,  float         * IN_ARRAY4)     { ( int cgmFour, int computeDICglobalMatrix_nz2,         int computeDICglobalMatrix_ny2,         int computeDICglobalMatrix_nx2,       float*         computeDICglobalMatrix_vol4DGrad       ) };
%apply (int DIM1, int DIM2,                      unsigned int  * IN_ARRAY2)     { (              int computeDICglobalMatrix_ConneSize,   int computeDICglobalMatrix_ConnSizeTet,                                       unsigned int*  computeDICglobalMatrix_conne           ) };
%apply (int DIM1, int DIM2,                      double        * IN_ARRAY2)     { (              int computeDICglobalMatrix_nodesSize,   int computeDICglobalMatrix_pTetSizeDim,                                       double*        computeDICglobalMatrix_nodes           ) };
%apply (int DIM1, int DIM2,                      float         * INPLACE_ARRAY2){ (              int computeDICglobalMatrix_dof1,        int computeDICglobalMatrix_dof2,                                              float*         computeDICglobalMatrix_matrixOut       ) };

%apply (int DIM1, int DIM2, int DIM3,            unsigned int * IN_ARRAY3)      { (              int computeDICglobalVector_nz1,         int computeDICglobalVector_ny1,         int computeDICglobalVector_nx1,       unsigned int*  computeDICglobalVector_volLabel        ) };
%apply (int DIM1, int DIM2, int DIM3, int DIM4,  float        * IN_ARRAY4)      { ( int cgvFour, int computeDICglobalVector_nz2,         int computeDICglobalVector_ny2,         int computeDICglobalVector_nx2,       float*         computeDICglobalVector_vol4DGrad       ) };
%apply (int DIM1, int DIM2, int DIM3,            float        * IN_ARRAY3)      { (              int computeDICglobalVector_nz3,         int computeDICglobalVector_ny3,         int computeDICglobalVector_nx3,       float*         computeDICglobalVector_vol1            ),
                                                                                  (              int computeDICglobalVector_nz4,         int computeDICglobalVector_ny4,         int computeDICglobalVector_nx4,       float*         computeDICglobalVector_vol2            ) };
%apply (int DIM1, int DIM2,                      unsigned int * IN_ARRAY2)      { (              int computeDICglobalVector_ConneSize,   int computeDICglobalVector_ConnSizeTet,                                       unsigned int*  computeDICglobalVector_conne           ) };
%apply (int DIM1, int DIM2,                      double       * IN_ARRAY2)      { (              int computeDICglobalVector_nodesSize,   int computeDICglobalVector_pTetSizeDim,                                       double*        computeDICglobalVector_nodes           ) };
%apply (int DIM1,                                float        * INPLACE_ARRAY1) { (              int computeDICglobalVector_dof3,                                                                                      float*         computeDICglobalVector_vecOut          ) };


%apply (int DIM1, int DIM2, int DIM3,            float         * IN_ARRAY3)     { (              int applyMeshTransformation_nz1,        int applyMeshTransformation_ny1,        int applyMeshTransformation_nx1,      float*         applyMeshTransformation_volGrey        ) };
%apply (int DIM1, int DIM2, int DIM3,            unsigned int  * IN_ARRAY3)     { (              int applyMeshTransformation_nz2,        int applyMeshTransformation_ny2,        int applyMeshTransformation_nx2,      unsigned int*  applyMeshTransformation_volLabel       ) };
%apply (int DIM1, int DIM2, int DIM3,            float         * INPLACE_ARRAY3){ (              int applyMeshTransformation_nz3,        int applyMeshTransformation_ny3,        int applyMeshTransformation_nx3,      float*         applyMeshTransformation_volOut         ) };
%apply (int DIM1, int DIM2,                      unsigned int  * IN_ARRAY2)     { (              int applyMeshTransformation_ConneSize,  int applyMeshTransformation_ConnSizeTet,                                      unsigned int*  applyMeshTransformation_conne          ) };
%apply (int DIM1, int DIM2,                      double        * IN_ARRAY2)     { (              int applyMeshTransformation_nodesSize,  int applyMeshTransformation_pTetSizeDim,                                      double*        applyMeshTransformation_nodes          ),
                                                                                  (              int applyMeshTransformation_three,      int applyMeshTransformation_nNodes,                                           double*        applyMeshTransformation_displ          ) };




%apply (int DIM1, int DIM2, int DIM3,            float        * IN_ARRAY3)      { (              int computeGMresidualAndPhase_nz1,      int computeGMresidualAndPhase_ny1,      int computeGMresidualAndPhase_nx1,    float*         computeGMresidualAndPhase_im1          ),
                                                                                  (              int computeGMresidualAndPhase_nz2,      int computeGMresidualAndPhase_ny2,      int computeGMresidualAndPhase_nx2,    float*         computeGMresidualAndPhase_im2          ) };
%apply (int DIM1, int DIM2,                      unsigned char* IN_ARRAY2)      { (              int computeGMresidualAndPhase_binsF,    int computeGMresidualAndPhase_binsG,                                          unsigned char* computeGMresidualAndPhase_phases       ) };
%apply (int DIM1, int DIM2,                      float        * IN_ARRAY2)      { (              int computeGMresidualAndPhase_nPeaks,   int computeGMresidualAndPhase_six,                                            float*         computeGMresidualAndPhase_peaks        ) };
%apply (int DIM1, int DIM2, int DIM3,            float        * INPLACE_ARRAY3) { (              int computeGMresidualAndPhase_nz3,      int computeGMresidualAndPhase_ny3,      int computeGMresidualAndPhase_nx3,    float*         computeGMresidualAndPhase_residual     ) };
%apply (int DIM1, int DIM2, int DIM3,            unsigned char* INPLACE_ARRAY3) { (              int computeGMresidualAndPhase_nz4,      int computeGMresidualAndPhase_ny4,      int computeGMresidualAndPhase_nx4,    unsigned char* computeGMresidualAndPhase_imLabelled       ) };




%apply (int DIM1, int DIM2, int DIM3,            float        * IN_ARRAY3)      { (              int applyPhiC_nz1,   int applyPhiC_ny1,   int applyPhiC_nx1, float*         applyPhiC_im        ) };
%apply (int DIM1, int DIM2, int DIM3,            float        * INPLACE_ARRAY3) { (              int applyPhiC_nz2,   int applyPhiC_ny2,   int applyPhiC_nx2, float*         applyPhiC_imSub     ) };
%apply (int DIM1,                                int          * IN_ARRAY1)      { (              int applyPhiC_threeA,                                                                                int*         applyPhiC_originSub ) };
%apply (int DIM1, int DIM2,                      float        * IN_ARRAY2)      { (              int applyPhiC_fourA, int applyPhiC_fourB,                                       float*         applyPhiC_Finv      ) };
%apply (int DIM1,                                float        * IN_ARRAY1)      { (              int applyPhiC_threeB,                                                                              float*         applyPhiC_Fpoint    ) };



%apply (int DIM1, int DIM2, int DIM3,            float        * IN_ARRAY3)      { (              int binningFloat_nz1,                        int binningFloat_ny1,                        int binningFloat_nx1,       float*         binningFloat_im        ) };
%apply (int DIM1, int DIM2, int DIM3,            float        * INPLACE_ARRAY3) { (              int binningFloat_nz2,                        int binningFloat_ny2,                        int binningFloat_nx2,       float*         binningFloat_imBin     ) };
%apply (int DIM1,                                int          * IN_ARRAY1)      { (              int binningFloat_three,                                                                                                 int*         binningFloat_offset    ) };

%apply (int DIM1, int DIM2, int DIM3,          unsigned short * IN_ARRAY3)      { (              int binningUInt_nz1,                        int binningUInt_ny1,                        int binningUInt_nx1, unsigned short*         binningUInt_im        ) };
%apply (int DIM1, int DIM2, int DIM3,          unsigned short * INPLACE_ARRAY3) { (              int binningUInt_nz2,                        int binningUInt_ny2,                        int binningUInt_nx2, unsigned short*         binningUInt_imBin     ) };
%apply (int DIM1,                              int            * IN_ARRAY1)      { (              int binningUInt_three,                                                                                                  int*         binningUInt_offset    ) };

%apply (int DIM1, int DIM2, int DIM3,         unsigned  char * IN_ARRAY3)      { (              int binningChar_nz1,                        int binningChar_ny1,                        int binningChar_nx1,   unsigned char*         binningChar_im        ) };
%apply (int DIM1, int DIM2, int DIM3,         unsigned  char * INPLACE_ARRAY3) { (              int binningChar_nz2,                        int binningChar_ny2,                        int binningChar_nx2,   unsigned char*         binningChar_imBin     ) };
%apply (int DIM1,                                int         * IN_ARRAY1)      { (              int binningChar_three,                                                                                                   int*         binningChar_offset    ) };




%apply (int DIM1, int DIM2, int DIM3,            float        * IN_ARRAY3)      { (              int pixelSearch_im1z,                   int pixelSearch_im1y,                   int pixelSearch_im1x,                 float*         pixelSearch_im1                        ),
                                                                                  (              int pixelSearch_im2z,                   int pixelSearch_im2y,                   int pixelSearch_im2x,                 float*         pixelSearch_im2                        ) };
%apply (int DIM1,                                float        * IN_ARRAY1)      { (              int pixelSearch_startPosN,                                                                                            float*         pixelSearch_startPos                   ) };
%apply (int DIM1, int DIM2,                      float        * IN_ARRAY2)      { (              int pixelSearch_searchRangeN,           int pixelSearch_two,                                                          float*         pixelSearch_searchRange                ) };
%apply (int DIM1,                                float        * ARGOUT_ARRAY1)  { (              int pixelSearch_n1,                                                                                                   float*         pixelSearch_argoutdata                 ) };


%include "computeDICoperators.hpp"
%include "applyPhiC.hpp"
%include "binning.hpp"
%include "pixelSearchGC.hpp"
%include "computeGMresidualAndPhase.hpp"
