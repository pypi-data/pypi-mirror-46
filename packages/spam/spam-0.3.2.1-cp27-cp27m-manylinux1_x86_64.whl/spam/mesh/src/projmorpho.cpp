#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <math.h>
#include <cmath>
#include <string.h>
#include <random>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
//#include <tiffio.h>
#include <algorithm>

#include "projmorpho.hpp"
#include "tetrahedron.hpp"

#define PBSTR "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
#define PBWIDTH 60
#define NEN 4

void projmorpho::print_error( std::string msg, bool ex ) {
  std::cout << "[ERROR] " << msg << std::endl;
  if ( ex ) {
    std::cout << "[ERROR] exit program" << std::endl;
    exit(EXIT_FAILURE);
  }
}


// constructor 

projmorpho::projmorpho( const std::string msh_file,
                        const std::string feap_file,
                        const std::vector< std::string > field_file,
                        const std::vector< double > thresholds ) {
    std::cout << "<projmorpho::projmoprho" << std::endl;

    // string
    _msh_file = msh_file;
    std::cout << ".\t msh: " << _msh_file << std::endl;
    
    // string
    _feap_file = feap_file;
    std::cout << ".\t feap: " << _feap_file << std::endl;
	
	// vector of string
    _field_file = field_file;
    if( _field_file.size() == 1 ) {
        std::cout << ".\t field: " << _field_file[0] << std::endl;
    } else {
        std::cout << ".\t field: " << _field_file.size() << std::endl;
        for( unsigned int f=0; f<_field_file.size(); f++) {
            std::cout << ".\t .\t file " << f+1 << ": " << _field_file[f] << std::endl;
        }
    }
	
	// vector of double
    _thresholds = thresholds;
    if( _thresholds.size() == 1) {
        std::cout << ".\t .\t phase 0: (-inf; " << _thresholds[0] << "]" << std::endl;
        std::cout << ".\t .\t phase 1: ]" << _thresholds[0] << "; +inf)" << std::endl;
    }
    else if( _thresholds.size() == 2) {
        std::cout << ".\t .\t phase 0: (-inf; " << _thresholds[0] << "]" << std::endl;
        std::cout << ".\t .\t phase 1: ]" << _thresholds[0] << "; " << _thresholds[1] << "]" << std::endl;
        std::cout << ".\t .\t phase 2: ]" << _thresholds[1] << "; +inf)" << std::endl;
    }
    else {
        std::string msg = "\t wrong number of threshold: "+std::to_string(_thresholds.size())+" (should be 1 or 2)";
        print_error( msg, true );
    }
  std::cout << ">" << std::endl;
};
  
  
void projmorpho::write_feap(){
  std::cout << "<projmorpho::write_feap" << std::endl;
  std::ofstream feap_file;
  feap_file.open( _feap_file, std::ios::out | std::ios::trunc );  
  std::string sep = ", ";  
  if ( feap_file ) {
    std::cout << ".\t feap file: " << _feap_file << std::endl;
    // write coordinates of nodes
    feap_file << "COORdinates ! " << _n_nodes << " nodes" << std::endl;
    for(unsigned int i=0; i<_n_nodes; i++) {
      feap_file << i+1 << sep
		<< 0 << sep                        
		<< _c_mesh[i][0] << sep
		<< _c_mesh[i][1] << sep
		<< _c_mesh[i][2] << std::endl;
    }
    feap_file << std::endl;
    // write connectivity and elements properties
    feap_file << "ELEMents ! " << _n_elem << " elements" << std::endl;
    for(unsigned int i=0; i<_n_elem; i++) {
      unsigned int it_a=4*i;
      feap_file << i+1 << sep                      // element number
		<< 0 << sep                        // 0
		<< _tetra_mat[i] << sep            // type of material
		<< _a_mesh[it_a] << sep            // connectivity node 1
		<< _a_mesh[it_a+1] << sep          // connectivity node 2
		<< _a_mesh[it_a+2] << sep          // connectivity node 3
		<< _a_mesh[it_a+3] << sep          // connectivity node 4
		<< _tetra_sub_volume[i] << sep     // sub volume (-)
		<< _tetra_orientation[i][0] << sep // interface orientation vector 1
		<< _tetra_orientation[i][1] << sep // interface orientation vector 1
		<< _tetra_orientation[i][2]        // interface orientation vector 1
		<< std::endl;
    }
    feap_file.close();    
  }
  else {
    std::string msg = "can\'t open feap file file \'"+_feap_file+"\'";
    print_error( msg, true );
  }
  std::cout << ">" << std::endl;
};

void projmorpho::write_feap_vtk(){
  std::cout << "<projmorpho::write_feap_vtk" << std::endl;
  std::ofstream vtk_file;
  vtk_file.open( _feap_file+".vtk", std::ios::out | std::ios::trunc );  
  std::string sep = " ";  
  if ( vtk_file ) {
    std::cout << ".\t vtk file: " << _feap_file << ".vtk" << std::endl;
    // STEP 1 - write header
    vtk_file << "# vtk DataFile Version 2.0" << std::endl;
    vtk_file << "VTK file from projmorpho: " << _feap_file << std::endl;
    vtk_file << "ASCII" << std::endl;
    vtk_file << "DATASET UNSTRUCTURED_GRID" << std::endl;
    vtk_file << std::endl;	  
    // STEP 2 - write coordinates of nodes
    vtk_file << "POINTS " << _n_nodes << " float" << std::endl;
    for(unsigned int i=0; i<_n_nodes; i++) {
      vtk_file << _c_mesh[i][0] << sep
	       << _c_mesh[i][1] << sep
	       << _c_mesh[i][2] << std::endl;
    }
    vtk_file << std::endl;
    // STEP 3 - write connectivity and elements properties
    vtk_file << "CELLS " << _n_elem << " " << 5*_n_elem << std::endl;
    for(unsigned int i=0; i<_n_elem; i++) {
      unsigned int it_a=4*i;
      vtk_file << 4 << sep                         // number of nodes / cell
		<< _a_mesh[it_a]-1 << sep            // connectivity node 1
		<< _a_mesh[it_a+1]-1 << sep          // connectivity node 2
		<< _a_mesh[it_a+2]-1 << sep          // connectivity node 3
		<< _a_mesh[it_a+3]-1 << sep          // connectivity node 4
		<< std::endl;
    }    
    // STEP 4 - write type of cell
    vtk_file << "CELL_TYPES " << _n_elem << std::endl;
    for(unsigned int i=0; i<_n_elem; i++) { vtk_file << 10 << std::endl; }
    vtk_file << std::endl;
    // STEP 3 - write cell datas
    vtk_file << "CELL_DATA " << _n_elem << std::endl;
    vtk_file << "SCALARS Material int" << std::endl;
    vtk_file << "LOOKUP_TABLE default" << std::endl;
    for(unsigned int i=0; i<_n_elem; i++) { vtk_file << _tetra_mat[i] << std::endl; }
    vtk_file << std::endl;
    vtk_file << "VECTORS InterfaceVector float" << std::endl;
    for(unsigned int i=0; i<_n_elem; i++) {
      vtk_file << _tetra_orientation[i][0] << sep
	       << _tetra_orientation[i][1] << sep
	       << _tetra_orientation[i][2] << sep
	       << std::endl;
    }
    vtk_file << std::endl;

    vtk_file << "POINT_DATA " << _n_nodes << std::endl;
    for( unsigned int f=0; f<_v_mesh.size(); f++ ) {      
      // STEP 4 - write nodes values (interpolated field)
      vtk_file << "SCALARS InterpolatedField" << f+1 << " float" << std::endl;
      vtk_file << "LOOKUP_TABLE default" << std::endl;
      for(unsigned int i=0; i<_n_nodes; i++) {
	vtk_file << _v_mesh[f][i] << std::endl;
      }
      vtk_file << std::endl;
    }
    
    vtk_file.close();    
  }
  else {
    std::string msg = "can\'t open vtk file file \'"+_feap_file+".vtk\'";
    print_error( msg, true );
  }
  std::cout << ">" << std::endl;
};

void projmorpho::set_materials(){
  std::cout << "<projmorpho::set_materials" << std::endl;
  // LOOP OVER THE TETRAHEDRONS
  // the goal of this loop is to fill the global elementary arrays
  // _tetra_mat
  // _tetra_sub_volumes
  // _tetra_orientation
  _tetra_mat.resize( _n_elem );
  _tetra_sub_volume.resize( _n_elem );
  _tetra_orientation.resize( _n_elem );   // Define global elementary arrays 
  for (unsigned int it=0; it<_n_elem; it++) {
    _tetra_orientation[it].resize(3);
    _tetra_sub_volume[it] = 0.0;
    _tetra_orientation[it][0] = 1.0; _tetra_orientation[it][1] = 0.0;  _tetra_orientation[it][2] = 0.0;
    _tetra_mat[it] = 0;
  }

  // loop on fields
  for( unsigned int f=0; f<_v_mesh.size(); f++ ) {
    std::cout << ".\t field " << f+1 << std::endl;

    double voltot = 0.0;
    for (unsigned int it = 0; it<_n_elem; it++) { // it is the iterator for each tetrahedron
      if( _tetra_mat[it] < 2 ) {
	unsigned int it_a = it*NEN;                  // it_a is the corresponding position in the 1D connectivity table    
	// double percentage = (double) (it+1) / (double) _n_elem;
	// int val = (int) (percentage * 100);
	// int lpad = (int) (percentage * PBWIDTH);
	// int rpad = PBWIDTH - lpad;
	// printf ("\r.\t loop over tetrahedrons: %3d%% [%.*s%*s]", val, lpad, PBSTR, rpad, "");
	// //printf ("\r.\t loop over tetrahedrons: %3d%%", val);
	// fflush (stdout);
    
	// STEP 1 - gives default values to the global elementary arrays
	// coordinates value mesh
	std::vector<std::vector<double> > c_tet(3);
	for(unsigned int k =0 ; k<3 ; k++){
	  c_tet[k].resize(NEN);
	  for(int l=0 ; l<NEN ; l++){
	    c_tet[k][l] = _c_mesh[_a_mesh[it_a+l]-1][k];
	  }
	}
	tetrahedron tet; 
	voltot += tet.get_volume_tet( c_tet );   
	// STEP 2 - fill the local arrays
	// (the following works only for hitting set [threshold, +infty[)
	// STEP 2.0 - Define local arrays
	//  imat and theta for each edge of the current tetrahedron
	std::vector<int> mat_edge(6);  std::vector<double> theta_edge(6);
	for (unsigned int k = 0; k < 6; k++) { mat_edge[k]  = 1; theta_edge[k] = 0.5; } // default values
	// local field value mesh
	std::vector<double> v_tet(4);
	for (unsigned int k = 0; k < 4; k++) { v_tet[k] = _v_mesh[f][_a_mesh[it_a+k]-1]; }
	// local correspondancy array between edges and nodes
	std::vector<std::vector< unsigned > > a_tet(6); 
	for(int k=0; k < 6; k++){ a_tet[k].resize(2); }
	a_tet[0][0]=0; a_tet[0][1]=1; a_tet[1][0]=0; a_tet[1][1]=3;
	a_tet[2][0]=0; a_tet[2][1]=2; a_tet[3][0]=1; a_tet[3][1]=3;
	a_tet[4][0]=1; a_tet[4][1]=2; a_tet[5][0]=3; a_tet[5][1]=2;
	// STEP 2.1 - compute sums
	int sum_t1 = 0;
	int sum_t2 = 0;
	for (int k = 0; k < NEN; k++) {
	  if( _v_mesh[f][_a_mesh[it_a+k]-1] > _thresholds[0] ) { sum_t1++; }
	  if( _thresholds.size() > 1 ) {
	    if( _v_mesh[f][_a_mesh[it_a+k]-1] > _thresholds[1] ) { sum_t2++; }
	  }
	}
	// STEP 2.2 - filling local arrays
	// STEP 2.2 - CASE 1 : one phase
	if( _thresholds.size() == 1 ){
	  // STEP 2.2.1 - define the type of material depending the sum
	  _tetra_mat[it] = 3;
	  if( sum_t1==0 ){ _tetra_mat[it] = 1; }
	  if( sum_t1==4 ){ _tetra_mat[it] = 2; }
	  // case interface
	  if( _tetra_mat[it] == 3 ){
	    // STEP 2.2.2 - filling the arays
	    for (unsigned int k = 0 ; k < 6 ; k++) {   
	      theta_edge[k] = 0.5;
	      if((v_tet[a_tet[k][0]] > _thresholds[0]) && (v_tet[a_tet[k][1]] < _thresholds[0])){
		theta_edge[k] = (v_tet[a_tet[k][0]]-_thresholds[0])/(v_tet[a_tet[k][0]]-v_tet[a_tet[k][1]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < _thresholds[0]) && (v_tet[a_tet[k][1]] > _thresholds[0])){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[0])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < _thresholds[0]) && (v_tet[a_tet[k][1]] < _thresholds[0])){
		//	    theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[0])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 1;
	      }
	      if((v_tet[a_tet[k][0]] > _thresholds[0]) && (v_tet[a_tet[k][1]] > _thresholds[0])){
		// theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[0])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 4;
	      }
	    }
	  }
	}
	// STEP 2.2 - CASE 2 : two phases
	else{
	  if( (sum_t1==0) && (sum_t2==0) ){ _tetra_mat[it] = 1; }
	  else if( (sum_t1==4) && (sum_t2==0) ){ _tetra_mat[it] = 2; }
	  else if( sum_t2==0 ){ _tetra_mat[it] = 3; }
	  else if( (sum_t1==4) && (sum_t2==4) ){ _tetra_mat[it] = 4; }
	  else if( sum_t1==4 ){ _tetra_mat[it] = 5; }
	  else{ _tetra_mat[it] = 6; }
	  // STEP 2.2 - CASE 2.1 : two phases / mat 3
	  if( _tetra_mat[it] == 3 ){
	    for (unsigned int k = 0 ; k < 6 ; k++) {
	      theta_edge[k] = 0.5;
	      if((v_tet[a_tet[k][0]] > _thresholds[0]) && (v_tet[a_tet[k][1]] < _thresholds[0])){
		theta_edge[k] = (v_tet[a_tet[k][0]]-_thresholds[0])/(v_tet[a_tet[k][0]]-v_tet[a_tet[k][1]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < _thresholds[0]) && (v_tet[a_tet[k][1]] > _thresholds[0])){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[0])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < _thresholds[0]) && (v_tet[a_tet[k][1]] < _thresholds[0])){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[0])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 1;
	      }
	      if((v_tet[a_tet[k][0]] > _thresholds[0]) && (v_tet[a_tet[k][1]] > _thresholds[0])){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[0])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 4;
	      }
	    }
	  }      
	  // STEP 2.2 - CASE 2.2 : two phases / mat 5
	  else if( _tetra_mat[it] == 5 ){
	    for (unsigned int k = 0 ; k < 6 ; k++) {   //boucle suer les aretes
	      theta_edge[k] = 0.5;
	      if((v_tet[a_tet[k][0]] > _thresholds[1]) && (v_tet[a_tet[k][1]] < _thresholds[1])){
		theta_edge[k] = (v_tet[a_tet[k][0]]-_thresholds[1])/(v_tet[a_tet[k][0]]-v_tet[a_tet[k][1]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < _thresholds[1]) && (v_tet[a_tet[k][1]] > _thresholds[1])){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[1])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < _thresholds[1]) && (v_tet[a_tet[k][1]] < _thresholds[1])){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[1])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 1;
	      }
	      if((v_tet[a_tet[k][0]] > _thresholds[1]) && (v_tet[a_tet[k][1]] > _thresholds[1])){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-_thresholds[1])/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 4;
	      }
	    }
	  }      
	  // STEP 2.2 - CASE 2.3 : two phases / mat 6
	  else if( _tetra_mat[it] == 6 ){
	    double temp_thresholds = (_thresholds[1] + _thresholds[0]) / 2;
	    for (unsigned int k = 0 ; k < 6 ; k++) {
	      theta_edge[k] = 0.5;
	      if((v_tet[a_tet[k][0]] > temp_thresholds) && (v_tet[a_tet[k][1]] < temp_thresholds)){
		theta_edge[k] = (v_tet[a_tet[k][0]]-temp_thresholds)/(v_tet[a_tet[k][0]]-v_tet[a_tet[k][1]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < temp_thresholds) && (v_tet[a_tet[k][1]] > temp_thresholds)){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-temp_thresholds)/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 3;
	      }
	      if((v_tet[a_tet[k][0]] < temp_thresholds) && (v_tet[a_tet[k][1]] < temp_thresholds)){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-temp_thresholds)/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 1;
	      }
	      if((v_tet[a_tet[k][0]] > temp_thresholds) && (v_tet[a_tet[k][1]] > temp_thresholds)){
		theta_edge[k] = 1 - (v_tet[a_tet[k][1]]-temp_thresholds)/(v_tet[a_tet[k][1]]-v_tet[a_tet[k][0]]);
		mat_edge[k] = 4;
	      }
	    }
	  }
	  // STEP 2.2 - CASE 2.4 : two phases / mat 7
	  else if( _tetra_mat[it] == 7 ){
	    if( (sum_t1==3)&&(sum_t2==1) ){
	      unsigned int node_1 = 0;
	      unsigned int node_2_1 = 0;
	      unsigned int node_2_2 = 0;
	      unsigned int node_3 = 0;
	      for (unsigned int k = 0; k < 4; k++) {
		if(_v_mesh[f][_a_mesh[it_a+k]-1] < _thresholds[0]){node_1=k;}
		else if(_v_mesh[f][_a_mesh[it_a+k]-1] > _thresholds[1]){node_3=k;}
		else if(node_2_1 ==0){node_2_1 = k;}
		else{node_2_2 = k;}
	      }
	      for (unsigned int k = 0 ; k < 6 ; k++) {
		theta_edge[k] = 0.5;
		if((a_tet[k][0] == node_1) && (a_tet[k][1] == node_3)){
		  theta_edge[k] = 1 - (v_tet[a_tet[k][0]]-((_thresholds[1] + _thresholds[1])/2))/(v_tet[a_tet[k][0]]-v_tet[a_tet[k][1]]);
		  mat_edge[k] = 3;
		}
		if((a_tet[k][0] == node_3) && (a_tet[k][1] == node_1)){
		  theta_edge[k] = (v_tet[a_tet[k][0]]-((_thresholds[1] + _thresholds[1])/2))/(v_tet[a_tet[k][0]]-v_tet[a_tet[k][1]]);
		  mat_edge[k] = 3;
		}
		if((a_tet[k][0] == node_1) && ((a_tet[k][1] == node_2_1)||(a_tet[k][1] == node_2_2))){
		  mat_edge[k] = 1;
		}
		if((a_tet[k][1] == node_1) && ((a_tet[k][0] == node_2_1)||(a_tet[k][0] == node_2_2))){
		  mat_edge[k] = 1;
		}
		if(((a_tet[k][0] == node_2_1)||(a_tet[k][0] == node_2_2))&&((a_tet[k][1] == node_2_1)||(a_tet[k][1] == node_2_2))){
		  mat_edge[k] = 1;
		}
		if(((a_tet[k][0] == node_2_1)||(a_tet[k][0] == node_2_2)) && (a_tet[k][1] == node_3)){
		  theta_edge[k] = 0.0;
		  mat_edge[k] = 3;
		}
		if(((a_tet[k][1] == node_2_1)||(a_tet[k][1] == node_2_2)) && (a_tet[k][0] == node_3)){
		  theta_edge[k] = 1.0;
		  mat_edge[k] = 3;
		}
	      } // end for k < 6 
	    } // end if sum 
	  } // end if material 3, 4, 5, 6, or 7
	} // end of STEP 2.2 (closing if case one or two phases)    
	// STEP 2.3 - determine type interface parameters as function of the local variables
	if( (_tetra_mat[it]==3) || (_tetra_mat[it]==5) || (_tetra_mat[it]==6) ){
	  std::vector<double> interface = tet.get_interface( c_tet, theta_edge, mat_edge ); // interface [V-, nx, ny, nz]
	  _tetra_sub_volume[it]     = interface[0];
	  _tetra_orientation[it][0] = interface[1];
	  _tetra_orientation[it][1] = interface[2];
	  _tetra_orientation[it][2] = interface[3];      
	} // end if _tetra_mat == 3, 5 or 6 (ie weak discontinuities)
	// STEP 3 : change material if not first field field
	// f=0: 1 -> 1 = 1
	// f=0: 2 -> 2 = 2+2*f
	// f=0: 3 -> 3 = 3+2*f
	// f=1: 1 -> 1 = 1
	// f=1: 2 -> 4 = 2+2*f
	// f=1: 3 -> 5 = 3+2*f
	// f=2: 1 -> 1 = 1
	// f=2: 2 -> 6 = 2+2*f
	// f=2: 3 -> 7 = 3+2*f
	if( _tetra_mat[it] > 1 ) {
	  _tetra_mat[it] = _tetra_mat[it]+2*f;
	}	
      }// end if _tetra_mat[0] < 2       
    } // end loop over tetrahedrons
    //std::cout << ".\t total volume: " << voltot << std::endl;
    std::cout << ".\t .\t MATE," << 1     << ": background"<< std::endl;
    std::cout << ".\t .\t MATE," << 2+2*f << ": phase " << f+1 << std::endl;
    std::cout << ".\t .\t MATE," << 3+2*f << ": interface phase "<< f+1 << " with background"<< std::endl;    
  } // end loop over fields
  std::cout << ">" << std::endl;
}

void projmorpho::set_field() {
  std::cout << "<projmorpho::set_field" << std::endl;
  std::cout << ".\t number of field: " << _field_file.size() << std::endl;
  _v_field.resize( _field_file.size() );
  for( unsigned int f=0; f<_field_file.size(); f++ ) {
    std::ifstream pFile( _field_file[f].c_str() ); // open input
    if ( pFile ) {
      std::cout << ".\t field file: \'"+_field_file[f]+"\'" << std::endl;
      std::string line, word;
      // get size of the cube in the three dimensions
      _d_field.resize( 3 ); 
      std::getline( pFile, line );
      std::istringstream isline1 ( line );
      for ( unsigned i = 0; i < 4; i++ ) {
	std::getline ( isline1, word, ',' );
	std::istringstream isword ( word );
	if ( i < 3 ) { isword >> _d_field[i]; }
      }
      std::cout << ".\t line 1 field size:\t " << _d_field[0] << " x " << _d_field[1] << " x " << _d_field[2] << std::endl;
      // get cube origin
      _o_field.resize( 3 ); 
      std::getline( pFile, line );
      std::istringstream isline2 ( line );
      for ( unsigned i = 0; i < 4; i++ ) {
	std::getline ( isline2, word, ',' );
	std::istringstream isword ( word );
	if ( i < 3 ) { isword >> _o_field[i]; }
      }
      std::cout << ".\t line 2 field origin:\t " << _o_field[0] << " x " << _o_field[1] << " x " << _o_field[2] << std::endl;
      // get number of nodes of the cube in the three directions
      _n_field.resize( 3 ); 
      std::getline( pFile, line );
      std::istringstream isline3 ( line );
      for ( unsigned i = 0; i < 4; i++ ) {
	std::getline ( isline3, word, ',' );
	std::istringstream isword ( word );
	if ( i < 3 ) { isword >> _n_field[i]; }
      }
      std::cout << ".\t line 3 field nodes:\t " << _n_field[0] << " x " << _n_field[1] << " x " << _n_field[2] << " = " << _n_field[0]*_n_field[1]*_n_field[2] << std::endl;
      // read field values
      _v_field[f].resize( _n_field[0]*_n_field[1]*_n_field[2] );
      unsigned j = 0;
      while( std::getline( pFile, line ) ) {
	std::istringstream isline3 ( line );
	double scratch=0; // tmp value values
	for ( unsigned i = 0; i < 4; i++ ) {
	  std::getline ( isline3, word, ',' );
	  std::istringstream isword ( word );
	  if ( i == 0 ) { isword >> scratch; }
	}
	if( j < _v_field[f].size() ) {
	  _v_field[f][j] = scratch;
	}
	j++;
      } //  end read field on lines
      std::cout << ".\t line 4 to " << j+3 << ": field values" << std::endl;    
      std::cout << ".\t .\t node 0: " << _v_field[f][0] << std::endl;
      std::cout << ".\t .\t node 1: " << _v_field[f][1] << std::endl;
      std::cout << ".\t .\t [...] " << std::endl;
      std::cout << ".\t .\t node " << j-2 << ": " << _v_field[f][j-2] << std::endl;
      std::cout << ".\t .\t node " << j-1 << ": " << _v_field[f][j-1] << std::endl;
      // check if the product of number of nodes equal size the field
      if ( j != _v_field[f].size() ) {
	std::string msg = "number of field values read ("+ std::to_string(j) +") does not match number of nodes ("+ std::to_string(_v_field[f].size()) +")";
	if ( j > _v_field[f].size() ) {
	  print_error( msg, false );
	  msg = "check if there is no extra blank lines at the end of \'"+_field_file[f]+"\'";
	  print_error( msg, true );
	} else {
	  print_error( msg, true );
	}
      }
      // create coordinates vector (the first time only)
      if( f==0 ) { fill_c_field(); }
    } // end test isfile
    else {
      std::string msg = "can\'t open input file \'"+_field_file[f]+"\'";
      print_error( msg, true );
    }
  }
  std::cout << ">" << std::endl;
}

void projmorpho::fill_c_field() {
  _c_field.resize( _v_field[0].size() ); for( unsigned i=0; i<_c_field.size(); i++) { _c_field[i].resize( 3 ); }     
  unsigned n = 0;
  double dx = _d_field[0]/double(_n_field[0]-1);
  double dy = _d_field[1]/double(_n_field[1]-1);
  double dz = _d_field[2]/double(_n_field[2]-1);
  for( unsigned k=0; k < _n_field[2] ; k++ ) {
    for( unsigned j=0; j < _n_field[1] ; j++ ) {
      for( unsigned i=0; i < _n_field[0] ; i++ ) {	  
	_c_field[n][0] = i*dx + _o_field[0];
	_c_field[n][1] = j*dy + _o_field[1];
	_c_field[n][2] = k*dz + _o_field[2];
	n++;
      }
    }
  }
}

void projmorpho::set_mesh(unsigned int n_skip) {
    // n_skip: number of int to skip between 4 and and beginning of connectivity
  std::cout << "<projmoprho::set_mesh" << std::endl;
  std::ifstream MSHfile( _msh_file.c_str() );   // open input file
  if (MSHfile) { // test if there is a file f
    // STEP 1 of the function : get coordinates of the unstructured mesh from the msh file
    std::string line,PartOfLine;
    std::vector<std::vector<double> > c_tmp;
    while ( std::getline(MSHfile,line) and (line!="$Nodes") ) {} // this while stop when an error occurs
    c_tmp.resize( 3 );
    bool Premierelignesautee =false;
    while ( std::getline(MSHfile,line) and (line!="$EndNodes") ) {
      if (Premierelignesautee) {
	std::istringstream issline (line);
	std::getline (issline, PartOfLine, ' '); 
	double tmp;
	for (int i=0;i<3;i++){
	  std::getline (issline, PartOfLine, ' ');
	  std::istringstream issPOL (PartOfLine);
	  issPOL >> tmp;
	  c_tmp[i].push_back(tmp);
	}
      }
      else{Premierelignesautee = true;}
    }
    // transpose vector
    _c_mesh.resize( c_tmp[0].size() );
    for( unsigned int i=0; i<c_tmp[0].size(); i++ ) {
      _c_mesh[i].resize( 3 );
      for( unsigned int j=0; j<3; j++ ) {
	_c_mesh[i][j] = c_tmp[j][i];
      }
    }
    _n_nodes = _c_mesh.size();
  } else {
    std::string msg = "can\'t open input file \'"+_msh_file+"\'";
    print_error( msg, true );    
  }
  std::ifstream MSHfile2( _msh_file.c_str() );   // open input file
  if (MSHfile2) { // test if there is a file f
    std::string line,PartOfLine;    
    while ( std::getline(MSHfile2,line) and (line!="$EndMeshFormat") ) {
      if ((line!="$MeshFormat")and(line!="$EndMeshFormat") ){
	char* cstr; char* PartOfLine;
	cstr = new char [line.size()+1];
	strcpy (cstr, line.c_str());
	PartOfLine = strtok (cstr , " ");
	if (strcmp(PartOfLine,"2.1")==0) {
	  std::cout << ".\t gmsh version 2.1" << std::endl;
	}
	else if(strcmp(PartOfLine,"2.2")==0) {
	  std::cout << ".\t gmsh version 2.2" << std::endl;
	}
	else{
	  std::string msg = "wrong msh file format (use 2.1 or 2.2)";
	  print_error( msg, true );    
	}
      }
    }
    while ( std::getline(MSHfile2,line) and (line!="$Elements") ){ }
    bool Premierelignesautee = false; //_a_mesh.resize(1); ??? 
    while ( std::getline(MSHfile2,line) and (line!="$EndElements") ) {
        if (Premierelignesautee) {
            char* cstr; char* PartOfLine;
            cstr = new char [line.size()+1];
            strcpy (cstr, line.c_str());
            PartOfLine = strtok (cstr , " ");
            PartOfLine = strtok (NULL, " ");
            int tmp;
            std::istringstream iss( PartOfLine ); iss >> tmp;
            if (tmp==NEN) {
                for (int j=0;j<(int(n_skip)+1);j++){
                    PartOfLine = strtok (NULL, " ");
                }
                while (PartOfLine != NULL){
                    std::istringstream iss( PartOfLine ); iss >> tmp;
                    _a_mesh.push_back( tmp ) ;
                    PartOfLine = strtok (NULL, " ");
                }
            }
        } else { Premierelignesautee = true; }
    }
    _n_elem  = _a_mesh.size()/NEN;
    std::cout << ".\t number of nodes: " << _c_mesh.size() << std::endl;
    std::cout << ".\t number of elements: " << _n_elem << std::endl;
  } else {
    std::string msg = "can\'t open input file \'"+_msh_file+"\'";
    print_error( msg, true );    
  }  
  std::cout << ">" << std::endl;
}

void projmorpho::dilate_field( double factor ) {
  for( unsigned int i=0; i<_c_field.size(); i++ ) {
    for( unsigned int j=0; j<_c_field[j].size(); j++ ) {
      _c_field[i][j] = factor*_c_field[i][j];
    }
  }
}

void projmorpho::interpolate_field() {
  std::cout << "<projmorpho::interpolate_field" << std::endl;
  std::cout << ".\t lengths: " << _d_field[0] << " x " << _d_field[1] << " x " << _d_field[2] << std::endl;
  std::cout << ".\t number of nodes: "    << _n_field[0] << " x " << _n_field[1] << " x " << _n_field[2] << std::endl;
  std::cout << ".\t number of elements: " << _n_field[0]-1 << " x " << _n_field[1]-1 << " x " << _n_field[2]-1 << std::endl;
  _v_mesh.resize( _v_field.size() ); for( unsigned int f=0; f<_v_mesh.size(); f++) { _v_mesh[f].resize( _n_nodes ); }
  // WARNING: if unstructured and sutrctured mesh does not have the same size a segmentation fault arises.
  // size of an field element
  std::vector<double> dx; dx.resize( 3 );
  for( unsigned i=0; i<3; i++) {
    dx[i] = _d_field[i]/double(_n_field[i]-1);
  }
  std::cout << ".\t size of elements: " << dx[0] << " x " << dx[1] << " x " << dx[2] << std::endl;

  // check if mesh inside field
  // get field boundaries
  double max_field_x = -1e10; double min_field_x = 1e10;
  double max_field_y = -1e10; double min_field_y = 1e10;
  double max_field_z = -1e10; double min_field_z = 1e10;
  for ( unsigned int i=0; i<_c_field.size(); i++ ) {
    max_field_x = (_c_field[i][0]>max_field_x) ? _c_field[i][0] : max_field_x;
    min_field_x = (_c_field[i][0]<min_field_x) ? _c_field[i][0] : min_field_x;
    max_field_y = (_c_field[i][1]>max_field_y) ? _c_field[i][1] : max_field_y;
    min_field_y = (_c_field[i][1]<min_field_y) ? _c_field[i][1] : min_field_y;
    max_field_z = (_c_field[i][2]>max_field_z) ? _c_field[i][2] : max_field_z;
    min_field_z = (_c_field[i][2]<min_field_z) ? _c_field[i][2] : min_field_z;
  }
  std::cout << ".\t field box: " << std::endl;
  std::cout << ".\t .\t x = [" << min_field_x << " " << max_field_x << "]" << std::endl;
  std::cout << ".\t .\t y = [" << min_field_y << " " << max_field_y << "]" << std::endl;
  std::cout << ".\t .\t z = [" << min_field_z << " " << max_field_z << "]" << std::endl;

  // get mesh boundaries
  double max_mesh_x = -1e10; double min_mesh_x = 1e10;
  double max_mesh_y = -1e10; double min_mesh_y = 1e10;
  double max_mesh_z = -1e10; double min_mesh_z = 1e10;
  for ( unsigned int i=0; i<_c_mesh.size(); i++ ) {
    max_mesh_x = (_c_mesh[i][0]>max_mesh_x) ? _c_mesh[i][0] : max_mesh_x;
    min_mesh_x = (_c_mesh[i][0]<min_mesh_x) ? _c_mesh[i][0] : min_mesh_x;
    max_mesh_y = (_c_mesh[i][1]>max_mesh_y) ? _c_mesh[i][1] : max_mesh_y;
    min_mesh_y = (_c_mesh[i][1]<min_mesh_y) ? _c_mesh[i][1] : min_mesh_y;
    max_mesh_z = (_c_mesh[i][2]>max_mesh_z) ? _c_mesh[i][2] : max_mesh_z;
    min_mesh_z = (_c_mesh[i][2]<min_mesh_z) ? _c_mesh[i][2] : min_mesh_z;
  }
  std::cout << ".\t mesh box: " << std::endl;
  std::cout << ".\t .\t x = [" << min_mesh_x << " " << max_mesh_x << "]" << std::endl;
  std::cout << ".\t .\t y = [" << min_mesh_y << " " << max_mesh_y << "]" << std::endl;
  std::cout << ".\t .\t z = [" << min_mesh_z << " " << max_mesh_z << "]" << std::endl;

  if(  ( max_mesh_x > max_field_x ) ||
       ( max_mesh_y > max_field_y ) ||
       ( max_mesh_z > max_field_z ) ||
       ( min_mesh_x < min_field_x ) ||
       ( min_mesh_y < min_field_y ) ||
       ( min_mesh_z < min_field_z ) ) {
    std::string msg = "mesh is ouside the boundaries of the field";
    print_error( msg, true );
  }


  // LOOP OVER ALL NODES OF THE MESH
  for (unsigned int i = 0 ; i < _n_nodes ; i++) {
    double x1 = _c_mesh[i][0]; double y1 = _c_mesh[i][1]; double z1 = _c_mesh[i][2];
    // get the node correpsonding to the regular mesh of the field
    int nodex1; int nodey1; int nodez1;
    //    std::cout << "**** mesh node\t" << i << ":\t" << x1 << "\t" << y1 << "\t" << z1 << std::endl;
    // std::cout << std::abs( x1 - _d_field[0] - _o_field[0] ) << std::endl;
    // std::cout << std::abs( y1 - _d_field[1] - _o_field[1] ) << std::endl;
    // std::cout << std::abs( z1 - _d_field[2] - _o_field[2] ) << std::endl;

    if ( std::abs( x1 - _d_field[0] - _o_field[0] ) > 1e-8 ) {
      nodex1 = (int) ((x1-_o_field[0])/dx[0]);
    } else {
      nodex1 = (int) _n_field[0]-2; // number of nodes -1 (for the previous node) and -1 (for the initial 0)
      //      std::cout << ".\t x" << std::endl;
    } 
    if ( std::abs( y1 - _d_field[1] - _o_field[1] ) > 1e-8 ) {
      nodey1 = (int) ((y1-_o_field[1])/dx[1]);
    } else {
      nodey1 = (int) _n_field[1]-2;
      //      std::cout << ".\t y" << std::endl;
    }
    if ( std::abs( z1 - _d_field[2] - _o_field[2] ) > 1e-8 ) {
      nodez1 = (int) ((z1-_o_field[2])/dx[2]);
    } else {
      nodez1 = (int) _n_field[2]-2;
      //      std::cout << ".\t z" << std::endl;
    }

    //    std::cout << "\t\t\t" << nodex1 << "\t" << nodey1 << "\t" << nodez1 << std::endl;
    int node1 = nodex1+_n_field[0]*nodey1+_n_field[0]*_n_field[1]*nodez1; //numero du node (voir schema ci dessous)    
    //    std::cout << ".\t .\t field node1: " << node1 << std::endl;
    // ********* /
    // _V_MESH EF /
    // ********* /
    //Cube elementaire du RF
    // ^      ^
    // |y    /z     
    //   ____
    //  /|* /|
    // /_|_/_|
    // | / | /  x
    // |/__|/   ->
    // ^
    // * point du maillage mecanique dans un cube elementaire
    // ^ int node

    //Passage des x1,y1,z1 en coord local : 0<x1,y1,z1<1
    // std::cout << _c_field.size() << std::endl;
    // std::cout << "coord of field node1: " << _c_field[node1][0] << ", " << _c_field[node1][1] << ", " << _c_field[node1][2] << std::endl;
    // std::cout << "global coord " << x1 << ", " << y1 << ", " << z1 << std::endl;
    x1 = 2*( x1-(_c_field[node1][0]+dx[0]/2) )/dx[0];
    y1 = 2*( y1-(_c_field[node1][1]+dx[1]/2) )/dx[1];
    z1 = 2*( z1-(_c_field[node1][2]+dx[2]/2) )/dx[2];
    // x1 = ( x1-_c_field[node1][0] )/dx[0];
    // y1 = ( y1-_c_field[node1][1] )/dx[1];
    // z1 = ( z1-_c_field[node1][2] )/dx[2];
    // std::cout << ".\t .\t local coord " << x1 << ", " << y1 << ", " << z1 << std::endl;
    // std::cout << std::endl;
    //fonctions de forme
    std::vector< double > N;
    N.resize( 8 );
    N[0] = (1-x1)*(1-y1)*(1-z1)/8;
    N[1] = (1+x1)*(1-y1)*(1-z1)/8;
    N[2] = (1-x1)*(1+y1)*(1-z1)/8;
    N[3] = (1+x1)*(1+y1)*(1-z1)/8;
    N[4] = (1-x1)*(1-y1)*(1+z1)/8;
    N[5] = (1+x1)*(1-y1)*(1+z1)/8;
    N[6] = (1-x1)*(1+y1)*(1+z1)/8;
    N[7] = (1+x1)*(1+y1)*(1+z1)/8;
    //deduction des autres nodes du cube elementaire Å‡ l'aide de int node1
    std::vector< int > Summit_Nodes;
    Summit_Nodes.resize( 8 );                        // x;y;z
                                                     // -----
    Summit_Nodes[0] = node1;                         // 0;0;0
    Summit_Nodes[1] = node1+1;                       // 1;0;0
    Summit_Nodes[2] = node1+_n_field[0];             // 0;1;0
    Summit_Nodes[3] = Summit_Nodes[2]+1;             // 1;1;0
    Summit_Nodes[4] = node1+_n_field[0]*_n_field[1]; // 0;0;1
    Summit_Nodes[5] = Summit_Nodes[4]+1;             // 1;0;1
    Summit_Nodes[6] = Summit_Nodes[4]+_n_field[0];   // 0;1;1
    Summit_Nodes[7] = Summit_Nodes[6]+1;             // 1;1;1
    // valeur du champ aleatoire aux nodes MEF
    for( unsigned int f=0; f<_v_mesh.size(); f++) {
      _v_mesh[f][i] = 0.0;
      for (int j=0 ; j<8 ; j++) {
	_v_mesh[f][i] += N[j]*_v_field[f][Summit_Nodes[j]];
      }
      // if( _v_mesh[f][i] > 1.0 ) {
      // 	std::cout << "phase " << f << " node " << i << " value " << _v_mesh[f][i] << std::endl;
      // 	std::string msg = "TO BiG";
      // 	print_error( msg, true );
      // }
      //      std::cout << std::endl;
    }    
  }
  std::cout << ">" << std::endl;
}

void projmorpho::parser( const std::string& config ) {
  std::cout << "<projmorpho::parser" << std::endl;
  std::ifstream file( config );
  if( file ) {
    std::string line;  
    while( std::getline( file, line ) ) {
      line.erase( std::remove( line.begin(), line.end(), ' ' ), line.end() ); // remove spaces
      std::istringstream iss( line );
      std::string key; std::string value;
      if( std::getline( iss, key , '=') ) { // read key 
	if( key == "msh" )   {
	  std::getline( iss, value );
	  _msh_file = value;
	  std::cout << ".\t msh: " << _msh_file << std::endl;
	}
	if( key == "feap" )  {
	  std::getline( iss, value );
	  _feap_file = value;
	  std::cout << ".\t feap: " << _feap_file << std::endl;
	}
	if( key == "field" ) {
	  while( std::getline( iss, value, ',' ) ) {
	    _field_file.push_back( value );
	  }
	  if( _field_file.size() == 1 ) {
	    std::cout << ".\t field: " << _field_file[0] << std::endl;
	  } else {
	    std::cout << ".\t field: " << _field_file.size() << std::endl;
	    for( unsigned int f=0; f<_field_file.size(); f++) {
	      std::cout << ".\t .\t file " << f+1 << ": " << _field_file[f] << std::endl;
	    }
	  }
	}
	if( key == "thresholds" ) {
	  while( std::getline( iss, value, ',' ) ) {
	    _thresholds.push_back( std::stod( value ) );
	  }
	  std::cout << ".\t thresholds: " << _thresholds.size() << std::endl;
	  if( _thresholds.size() == 1) {
	    std::cout << ".\t .\t phase 0: (-inf; " << _thresholds[0] << "]" << std::endl;
	    std::cout << ".\t .\t phase 1: ]" << _thresholds[0] << "; +inf)" << std::endl;
	  }
	  else if( _thresholds.size() == 2) {
	    std::cout << ".\t .\t phase 0: (-inf; " << _thresholds[0] << "]" << std::endl;
	    std::cout << ".\t .\t phase 1: ]" << _thresholds[0] << "; " << _thresholds[1] << "]" << std::endl;
	    std::cout << ".\t .\t phase 2: ]" << _thresholds[1] << "; +inf)" << std::endl;
	  }
	  else {
	    std::string msg = "\t wrong number of threshold: "+std::to_string(_thresholds.size())+" (should be 1 or 2)";
	    print_error( msg, true );
	  }
	}	
      }
    }
  } else {
    std::string msg = "can\'t open feap file file \'"+config+"\'";
    print_error( msg, true );
  }
  std::cout << ">" << std::endl;
}


/* ******* */
/*  USERS  */
/* ******* */
void projmorpho::set_field_vectors( std::vector<std::vector<float> > v_field, std::vector< double > d_field, std::vector< unsigned > n_field, std::vector< double > o_field ) {
  std::cout << "<projmorpho::set_field_vectors" << std::endl;
  _o_field = o_field; // origin
  _n_field = n_field; // number of nodes
  _d_field = d_field; // total length of the cube
  _v_field = v_field; // fields values
  fill_c_field();

  std::cout << ".\t field size:\t " << _d_field[0] << " x " << _d_field[1] << " x " << _d_field[2] << std::endl;
  std::cout << ".\t field origin:\t " << _o_field[0] << " x " << _o_field[1] << " x " << _o_field[2] << std::endl;
  std::cout << ".\t field nodes:\t " << _n_field[0] << " x " << _n_field[1] << " x " << _n_field[2] << " = " << _n_field[0]*_n_field[1]*_n_field[2] << std::endl;

  unsigned n = _v_field[0].size();
  for( unsigned int f=0; f<_v_field.size(); f++ ) {
    std::cout << ".\t field " << f+1 << std::endl;
    std::cout << ".\t .\t node 0: " << _v_field[f][0] << std::endl;
    std::cout << ".\t .\t node 1: " << _v_field[f][1] << std::endl;
    std::cout << ".\t .\t [...] " << std::endl;
    std::cout << ".\t .\t node " << n-2 << ": " << _v_field[f][n-2] << std::endl;
    std::cout << ".\t .\t node " << n-1 << ": " << _v_field[f][n-1] << std::endl;
  }

  
  std::cout << ">" << std::endl;
};

void projmorpho::set_mesh_vectors( std::vector<std::vector<float> > c_mesh, std::vector<unsigned> a_mesh ) {
  _c_mesh = c_mesh;
  _a_mesh = a_mesh;
  _n_elem = _a_mesh.size()/NEN;
  _n_nodes = _c_field.size();
};

void projmorpho::set_thresholds( std::vector<double> thresholds ) {
  _thresholds=thresholds;
};

std::vector< std::vector< float > > projmorpho::get_field_coordinates() { return _c_field; };
std::vector< std::vector< float > > projmorpho::get_mesh_coordinates()  { return _c_mesh; };
std::vector< std::vector< float > > projmorpho::get_field_values() { return _v_field; };
std::vector< std::vector< float > > projmorpho::get_mesh_values()  { return _v_mesh; };
std::vector< unsigned > projmorpho::get_mesh_connectivity() { return _a_mesh; };
