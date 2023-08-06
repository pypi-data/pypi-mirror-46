/* File: meshToolkit.i */

%module meshToolkit

%{
    #define SWIG_FILE_WITH_INIT
    #include "meshToolkit.hpp"
%}


%include "numpy.i"
%include "std_string.i"
%include "std_vector.i"

%template(VectorDouble)   std::vector<double>;
%template(VectorVectorDouble)   std::vector<std::vector<double> >;
%template(VectorString)   std::vector<std::string>;
%template(VectorUnsigned) std::vector<unsigned int>;

%init %{
    import_array();
%}

%include "meshToolkit.hpp"
