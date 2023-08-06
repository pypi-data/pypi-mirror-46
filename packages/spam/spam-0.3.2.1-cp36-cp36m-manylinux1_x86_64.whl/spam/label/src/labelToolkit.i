/* File: labelToolkit.i */

%module labelToolkit

%{
#define SWIG_FILE_WITH_INIT
#include "labelToolkitC.hpp"
%}


%include "numpy.i"

%init %{
import_array();
%}

/* WARNING, these names here must be exactly the same as the hpp file (not necessarily the cpp) */
%apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int boundingBoxes_volSizeZ,       int boundingBoxes_volSizeY,     int boundingBoxes_volSizeX  ,    labels::label* boundingBoxes_volLab             ) };
%apply (int DIM1, int DIM2,           unsigned short* INPLACE_ARRAY2 ) { ( int boundingBoxes_maxLabel,       int boundingBoxes_six,                                          unsigned short* boundingBoxes_boundingBoxes      ) };

%apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int centresOfMass_volSizeZ,       int centresOfMass_volSizeY,     int centresOfMass_volSizeX,      labels::label* centresOfMass_volLab           ) };
%apply (int DIM1, int DIM2,           unsigned short* IN_ARRAY2      ) { ( int centresOfMass_maxLabelBB,     int centresOfMass_sixBB,                                        unsigned short* centresOfMass_boundingBoxes    ) };
%apply (int DIM1, int DIM2,                    float* INPLACE_ARRAY2 ) { ( int centresOfMass_maxLabelCM,     int centresOfMass_threeCM,                                               float* centresOfMass_centresOfMass    ) };

%apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int volumes_______volSizeZ,       int volumes_______volSizeY,     int volumes_______volSizeX,      labels::label* volumes_______volLab           ) };
%apply (int DIM1, int DIM2,           unsigned short* IN_ARRAY2      ) { ( int volumes_______maxLabelBB,     int volumes_______sixBB,                                        unsigned short* volumes_______boundingBoxes    ) };
%apply (int DIM1,                       unsigned int* INPLACE_ARRAY1 ) { ( int volumes_______maxLabelCM,                                                                       unsigned int* volumes_______volumes          ) };


%apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int momentOfInertia_volSizeZ,     int momentOfInertia_volSizeY,   int momentOfInertia_volSizeX,    labels::label* momentOfInertia_volLab         ) };
%apply (int DIM1, int DIM2,           unsigned short* IN_ARRAY2      ) { ( int momentOfInertia_maxLabelBB,   int momentOfInertia_sixBB,                                      unsigned short* momentOfInertia_boundingBoxes  ) };
%apply (int DIM1, int DIM2,                    float* IN_ARRAY2      ) { ( int momentOfInertia_maxLabelCM,   int momentOfInertia_threeCM,                                             float* momentOfInertia_centresOfMass  ) };
%apply (int DIM1, int DIM2,                    float* INPLACE_ARRAY2 ) { ( int momentOfInertia_maxLabelMI1,  int momentOfInertia_threeMI1,                                            float* momentOfInertia_momentOfInertiaEigenValues ),
                                                                         ( int momentOfInertia_maxLabelMI2,  int momentOfInertia_nineMI2,                                             float* momentOfInertia_momentOfInertiaEigenVectors) };

%apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int labelToFloat_volSizeZin,      int labelToFloat_volSizeYin,    int labelToFloat_volSizeXin,     labels::label* labelToFloat_volLab                 ) };
%apply (int DIM1,                              float* IN_ARRAY1      ) { ( int labelToFloat_maxLabel,                                                                                 float* labelToFloat_labelFloats            ) };
%apply (int DIM1, int DIM2, int DIM3,          float* INPLACE_ARRAY3 ) { ( int labelToFloat_volSizeZout,     int labelToFloat_volSizeYout,   int labelToFloat_volSizeXout,            float* labelToFloat_volOutput              ) };

%apply (int DIM1, int DIM2, int DIM3,  labels::label* INPLACE_ARRAY3 ) { ( int relabel_volSizeZin,           int relabel_volSizeYin,         int relabel_volSizeXin,          labels::label* relabel_volLab              ) };
%apply (int DIM1,                      labels::label* IN_ARRAY1      ) { ( int relabel_maxLabel,                                                                              labels::label* relabel_labelMap            ) };


%apply (int DIM1, int DIM2, int DIM3,  labels::label* INPLACE_ARRAY3 ) { ( int tetPixelLabel_volSizeZ,       int tetPixelLabel_volSizeY,     int tetPixelLabel_volSizeX,      labels::label* tetPixelLabel_vol              ) };
%apply (int DIM1, int DIM2,           unsigned int* IN_ARRAY2      ) { ( int tetPixelLabel_conneSize,      int tetPixelLabel_connSizeTet,                                  unsigned int* tetPixelLabel_conne            ) };
%apply (int DIM1, int DIM2,                    float* IN_ARRAY2      ) { ( int tetPixelLabel_nodesSize,      int tetPixelLabel_pTetSizeDim,                                           float* tetPixelLabel_nodes            ) };

%apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int setVoronoi_volSizeZ1,         int setVoronoi_volSizeY1,       int setVoronoi_volSizeX1,        labels::label* setVoronoi_volLab       ) };
%apply (int DIM1, int DIM2, int DIM3,          float* IN_ARRAY3      ) { ( int setVoronoi_PoreEDTsizeZ,      int setVoronoi_PoreEDTsizeY,    int setVoronoi_PoreEDTsizeX,             float* setVoronoi_volPoreEDT   ) };
%apply (int DIM1, int DIM2, int DIM3,  labels::label* INPLACE_ARRAY3 ) { ( int setVoronoi_volSizeZ2,         int setVoronoi_volSizeY2,       int setVoronoi_volSizeX2,        labels::label* setVoronoi_volLabOut    ) };
%apply (int DIM1, int DIM2,                      int* IN_ARRAY2      ) { ( int setVoronoi_nPoints,           int setVoronoi_three,                                                      int* setVoronoi_indicesSorted) };
%apply (int DIM1,                                int* IN_ARRAY1      ) { ( int setVoronoi_threshPlusOne,                                                                                int* setVoronoi_indices      ) };

%apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int labelContacts_volSizeZ1,      int labelContacts_volSizeY1,    int labelContacts_volSizeX1,     labels::label* labelContacts_volLab           ) };
%apply (int DIM1, int DIM2, int DIM3,labels::contact* INPLACE_ARRAY3 ) { ( int labelContacts_volSizeZ2,      int labelContacts_volSizeY2,    int labelContacts_volSizeX2,   labels::contact* labelContacts_volContacts      ) };
%apply (int DIM1,                      unsigned char* INPLACE_ARRAY1 ) { ( int labelContacts_nLabels,                                                                         unsigned char* labelContacts_Z                ) };
%apply (int DIM1, int DIM2,          labels::contact* INPLACE_ARRAY2 ) { ( int labelContacts_nLabelsTwo,     int labelContacts_twoZmax,                                     labels::contact* labelContacts_contactTable     ) };
%apply (int DIM1, int DIM2,            labels::label* INPLACE_ARRAY2 ) { ( int labelContacts_nContactsMax,   int labelContacts_two,                                           labels::label* labelContacts_contactingLabels ) };

# %apply (int DIM1, int DIM2, int DIM3,  labels::label* IN_ARRAY3      ) { ( int setVoronoi_volSizeZ1,          int setVoronoi_volSizeY1,       int setVoronoi_volSizeX1,        labels::label* setVoronoi_volLab       ) };
# %apply (int DIM1, int DIM2, int DIM3,          float* IN_ARRAY3      ) { ( int setVoronoi_PoreEDTsizeZ,       int setVoronoi_PoreEDTsizeY, int setVoronoi_PoreEDTsizeX,                float* setVoronoi_volPoreEDT   ) };
# %apply (int DIM1, int DIM2, int DIM3,  labels::label* INPLACE_ARRAY3 ) { ( int setVoronoi_volSizeZ2,          int setVoronoi_volSizeY2,       int setVoronoi_volSizeX2,        labels::label* setVoronoi_volLabOut    ) };

%include "labelToolkitC.hpp"
