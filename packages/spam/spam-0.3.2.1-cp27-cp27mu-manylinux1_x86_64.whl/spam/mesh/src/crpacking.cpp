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
#include <iomanip>
#include <algorithm>

#include "crpacking.hpp"

#define PBSTR "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
#define PBWIDTH 60

void crpacking::print_error( std::string msg, bool ex ) {
  std::cout << "[ERROR] " << msg << std::endl;
  if ( ex ) {
    std::cout << "[ERROR] exit program" << std::endl;
    exit(EXIT_FAILURE);
  }
}


/***********************************/
/*             PUBLIC              */
/***********************************/


/* CONSTRUCTOR */

crpacking::crpacking( std::vector<double> param,
                      std::vector<double> delta,
                      std::vector<double> origi,
                      std::vector<unsigned int> cells,
                      unsigned int i,
                      std::string field_file,
                      std::string object_file,
                      std::string domain) {
  std::cout << "<crpacking::crpacking" << std::endl;
  // set default values to the variables
  _delta = delta;
  _origi = origi;
  if( i )
    _inside = true;
  else
    _inside = false;
  _field_file   = field_file;
  _objects_file = object_file;
  _domain_type  = domain;
  _n_elem = cells;
  _n_nodes.resize( 3 );
  _n_nodes[0] = cells[0]+1;
  _n_nodes[1] = cells[1]+1;
  _n_nodes[2] = cells[2]+1;
  // note: no default values for _param since shape depend on type of object
  // read configuration to change the default values
    //   parser( config );
  _param = param;
  _elem_size.resize( 3 );
  _elem_size[0] = _delta[0]/_n_elem[0];
  _elem_size[1] = _delta[1]/_n_elem[1];
  _elem_size[2] = _delta[2]/_n_elem[2];

  // output
  std::cout << ".\t field file: " << _field_file << std::endl;
  std::cout << ".\t object file: " << _objects_file << std::endl;
  std::cout << ".\t domain type: " << _domain_type << std::endl;
  std::cout << ".\t field size: " << _delta[0] << ", " << _delta[1] << ", " << _delta[2] << std::endl;
  std::cout << ".\t element size: " << _elem_size[0] << ", " << _elem_size[1] << ", " << _elem_size[2] << std::endl;
  std::cout << ".\t field origin: " << _origi[0] << ", " << _origi[1] << ", " << _origi[2] << std::endl;
  std::string msg = ( _inside ) ? "True" : "False";
  std::cout << ".\t objects inside: " << msg << std::endl;
  if( _param.size()>2 ) {
    if( (_param.size()-2)%4==0 ) { // spheres
      std::cout << ".\t parameters for spheres" << std::endl;
      for( unsigned int i=0; i<_param.size(); i++) {
	std::cout << ".\t .\t ";
	if( i==0 ) {
	  std::cout << "total volume fraction:\t";
	} else if ( i==1 ) {
	  std::cout << "rejection length:\t";
	} else if ( (i-2)%4==0 ) {
	  std::cout << "phase " << (int) ((i-2)/4) << " rmin:\t\t";
	} else if ( (i-2)%4==1 ) {
	  std::cout << "phase " << (int) ((i-2)/4) << " rmax:\t\t";
	} else if ( (i-2)%4==2 ) {
	  std::cout << "phase " << (int) ((i-2)/4) << " volf:\t\t";
	} else if ( (i-2)%4==3 ) {
	  std::cout << "phase " << (int) ((i-2)/4) << " valu:\t\t";
	}
	std::cout << _param[i] << std::endl;
      }
    } else if( (_param.size()-2)%5==0 ) { // ellipsoids
      std::cout << ".\t parameters for ellipsoids" << std::endl;
      for( unsigned int i=0; i<_param.size(); i++) {
	std::cout << ".\t .\t ";
	if( i==0 ) {
	  std::cout << "total volume fraction:\t";
	} else if ( i==1 ) {
	  std::cout << "rejection length:\t";
	} else if ( (i-2)%5==0 ) {
	  std::cout << "phase " << (int) ((i-2)/5) << " rx:\t\t";
	} else if ( (i-2)%5==1 ) {
	  std::cout << "phase " << (int) ((i-2)/5) << " ry:\t\t";
	} else if ( (i-2)%5==2 ) {
	  std::cout << "phase " << (int) ((i-2)/5) << " rz:\t\t";
	} else if ( (i-2)%5==3 ) {
	  std::cout << "phase " << (int) ((i-2)/5) << " volf:\t\t";
	} else if ( (i-2)%5==4 ) {
	  std::cout << "phase " << (int) ((i-2)/5) << " valu:\t\t";
	}
	std::cout << _param[i] << std::endl;
      }
    } else {
      std::string msg = "param size does not fit any objects ("+std::to_string( _param.size() )+")";
      print_error( msg, true );
    }
  } else {
    _param.resize(1);
    // std::string msg = "param needs to be initiated";
    // print_error( msg, true );
  }
  std::cout << ">" << std::endl;
}


/***************************/
/* CREATE OBJECTS          */
/*   create_spheres()      */
/*   create_ellipsoids()  */
/***************************/

void crpacking::create_spheres() {
  std::cout << "<crpacking::create_spheres" << std::endl;
  // STEP 1: INITIATE VARIABLES
  std::random_device r;
  std::default_random_engine generator( r() );
  double dx = _delta[0]; double dy = _delta[1]; double dz = _delta[2];
  double ox = _origi[0]; double oy = _origi[1]; double oz = _origi[2];
  //param[0] -> total volume fraction
  //param[1] -> rejection length
  //param[2+4*p+0] -> rmin of phase p
  //param[2+4*p+1] -> rmax of phase p
  //param[2+4*p+2] -> relative volume fraction of the phase
  //param[2+4*p+3] -> field value of the phase
  double volf_tot = _param[0];
  double reje_len = _param[1];
  if( (_param.size()-2)%4 ) {
    std::string msg = "param size = "+std::to_string( _param.size() )+": size of param vector should be ( 2 + 4n ) with n the number of phase";
    print_error( msg, true );
  }
  _n_phases = (_param.size()-2)/4;
  _phases_values.resize( _n_phases );
  std::cout << ".\t total volume fraction: " << volf_tot << std::endl;
  std::cout << ".\t rejection length: " << reje_len << std::endl;
  std::cout << ".\t number of phases: " << _n_phases << std::endl;
  std::vector<unsigned int> n_spheres_per_phase( _n_phases );
  std::vector<double> volf_per_phase( _n_phases );       // just for the record in order to plot summary at the end of the function
  _n_objects = 0;
  // STEP 2: LOOP 1 OVER THE PHASES (compute the number of spheres)
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double rmin = _param[4*p+2];
    double rmax = _param[4*p+3];
    double volf = _param[4*p+4]*volf_tot;
    unsigned int valu = (unsigned int) _param[4*p+5];
    _phases_values[p] = _param[4*p+5];
    volf_per_phase[p] = volf;
    double ra = 0.0; if( !_inside ) { ra = 4.*rmax/3.; } // radius added in case  inside == False
    double vol_domain = 0.0;
    if( _domain_type == "cube" ) {
        vol_domain = (dx+ra)*(dy+ra)*(dz+ra);
    } else if ( _domain_type == "cylinder" ) {
        vol_domain = M_PI*pow(0.5*(dx+ra), 2)*(dz+ra);
    } else {
        std::string msg = "unkown domain type \'"+_domain_type+"\'";
        print_error( msg, true );
    }
    if(rmin!=rmax) {
      n_spheres_per_phase[p] = volf*( vol_domain ) * 3.*(rmax-rmin)/(M_PI*(pow(rmax,4)-pow(rmin,4))); // compute the number of spheres
    }
    else {
      n_spheres_per_phase[p] = volf*( vol_domain ) * 3./(4*M_PI*(pow(rmax,3))); // compute the number of spheres
    }
    _n_objects += n_spheres_per_phase[p];
    std::cout << ".\t phase number: " << p << std::endl;
    std::cout << ".\t .\t rmin: " << rmin << std::endl;
    std::cout << ".\t .\t rmax: " << rmax << std::endl;
    std::cout << ".\t .\t volf: " << volf << std::endl;
    std::cout << ".\t .\t valu: " << valu << std::endl;
    // test if minimal radius rmin > rejection length
    if( rmin < reje_len ) {
      std::string msg = "minimal radius lower than rejection length for phase "+std::to_string(p)+": "+std::to_string(rmin)+" < "+std::to_string(reje_len);
      print_error( msg, true );
    }
    if( rmax < rmin ) {
      std::string msg = "maximal radius lower than minimal radius for phase "+std::to_string(p)+": "+std::to_string(rmax)+" < "+std::to_string(rmin);
      print_error( msg, true );
    }
  } // end loop 1 over phases
  // STEP 3: CREATION OF THE _objects vector
  _objects.resize( _n_objects ); for( unsigned int i=0; i<_n_objects; i++ ) { _objects[i].resize( 5 ); }
  // LOOP 2 OVER THE PHASES (put the spheres randomly)
  // keep track of the indice in the global _objects vector
  unsigned int pi = 0;
  std::vector<double> volf_per_phase_real( _n_phases );  // just for the record in order to plot summary at the end of the function
  double volf_tot_real = 0.0;
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double rmin = _param[4*p+2];
    double rmax = _param[4*p+3];
    unsigned int valu = (unsigned int) _param[4*p+5];
    volf_per_phase_real[p] = 0.0;
    std::uniform_real_distribution<double> u_distr_r( rmin, rmax );
    double add_r = 0.0; if( _inside ) { add_r = rmax; }
    if( _domain_type == "cube" ) {
        std::uniform_real_distribution<double> u_distr_x( ox+add_r, ox+dx-add_r );
        std::uniform_real_distribution<double> u_distr_y( oy+add_r, oy+dy-add_r );
        std::uniform_real_distribution<double> u_distr_z( oz+add_r, oz+dz-add_r );
        // to compare the resulting volume fraction with the input
        double rmin_real = rmax; double rmax_real = rmin;
        // LOOP OVER THE SPHERES (set radius, x, y, z and field value)
        for( unsigned int i=0; i<n_spheres_per_phase[p]; i++ ) {
            _objects[pi][0] = u_distr_r( generator ); // radius
            _objects[pi][1] = u_distr_x( generator ); // position x
            _objects[pi][2] = u_distr_y( generator ); // position y
            _objects[pi][3] = u_distr_z( generator ); // position z
            _objects[pi][4] = valu;                   // value of the field
            if( _objects[pi][0] < rmin_real ) rmin_real = _objects[pi][0];
            if( _objects[pi][0] > rmax_real ) rmax_real = _objects[pi][0];
            volf_per_phase_real[p] += 4.*M_PI*pow(_objects[pi][0],3)/(3.*(dx*dy*dz));
            pi++;
        }
        volf_tot_real += volf_per_phase_real[p];
    } else if( _domain_type == "cylinder" ) {
        std::uniform_real_distribution<double> u_distr_z( oz+add_r, oz+dz-add_r );
        std::uniform_real_distribution<double> u_distr_d( 0.0, 0.5*dx-add_r );
        std::uniform_real_distribution<double> u_distr_theta( 0.0, 2.0*M_PI );
        // to compare the resulting volume fraction with the input
        double rmin_real = rmax; double rmax_real = rmin;
        // LOOP OVER THE SPHERES (set radius, x, y, z and field value)
        for( unsigned int i=0; i<n_spheres_per_phase[p]; i++ ) {
            _objects[pi][0] = u_distr_r( generator ); // radius
            double d = u_distr_d( generator );  double theta = u_distr_theta( generator );
            _objects[pi][1] = sqrt(d*(0.5*dx-add_r))*cos(theta)+0.5*dx+ox; // position x
            _objects[pi][2] = sqrt(d*(0.5*dx-add_r))*sin(theta)+0.5*dy+oy; // position y
            _objects[pi][3] = u_distr_z( generator ); // position z
            _objects[pi][4] = valu;                   // value of the field
            if( _objects[pi][0] < rmin_real ) rmin_real = _objects[pi][0];
            if( _objects[pi][0] > rmax_real ) rmax_real = _objects[pi][0];
            volf_per_phase_real[p] += 4.*M_PI*pow(_objects[pi][0],3)/(3.*(M_PI*pow(0.5*dx,2)*dz)); // divided by pi*r^2*h
            pi++;
        }
        volf_tot_real += volf_per_phase_real[p];
    } else {
        std::string msg = "unkown domain type \'"+_domain_type+"\'";
        print_error( msg, true );
    }


  }
  // Output VOLUME FRACTION
  std::cout << ".\t volume fraction" << std::endl;
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double a = volf_per_phase[p];
    double b = volf_per_phase_real[p];
    std::cout << std::fixed << std::setprecision(4) << ".\t .\t phase " << p << " --- target: " << a << " actual: " << b << " error: "  << std::setprecision(0) << std::abs(a-b)/a*100. << "%" << std::endl;
  }
  double a = volf_tot;
  double b = volf_tot_real;
  std::cout << std::fixed << std::setprecision(4) << ".\t .\t total ----- target: " << a << " actual: " << b << " error: "  << std::setprecision(0) << std::abs(a-b)/a*100. << "%" << std::endl;
  // Output VOLUME FRACTION
  std::cout << ".\t number of objects" << std::endl;
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double a = n_spheres_per_phase[p];
    std::cout << ".\t .\t phase " << p << ": " << a << std::endl;
  }
  std::cout << ".\t .\t total: " << _n_objects << std::endl;
  std::cout << ">" << std::endl;
}

void crpacking::create_ellipsoids(){
  std::cout << "<crpacking::create_ellipsoids" << std::endl;
  // STEP 1 : INITIATE VARIABLES
  //  std::random_device r;
  //  std::default_random_engine generator( r() );
  double dx = _delta[0]; double dy = _delta[1]; double dz = _delta[2];
  double ox = _origi[0]; double oy = _origi[1]; double oz = _origi[2];
  //param[0] -> total volume fraction
  //param[1] -> rejection length
  //param[2+5*p+0] -> rx
  //param[2+5*p+1] -> ry
  //param[2+5*p+2] -> rz
  //param[2+5*p+3] -> relative volume fraction of the phase
  //param[2+5*p+4] -> field value of the phase
  double volf_tot = _param[0];
  double reje_len = _param[1];
  if( (_param.size()-2)%5 ) {
    std::string msg = "param for ellipsoids: size of param vector should be 5.n+2 with n the number of phase. Here param size = "+std::to_string( _param.size() );
    print_error( msg, true );
  }
  _n_phases = (_param.size()-2)/5;
  _phases_values.resize( _n_phases );
  std::cout << ".\t total volume fraction: " << volf_tot << std::endl;
  std::cout << ".\t rejection length: " << reje_len << std::endl;
  std::cout << ".\t number of phases: " << _n_phases << std::endl;
  std::vector<unsigned int> n_spheres_per_phase( _n_phases );
  std::vector<double> volf_per_phase( _n_phases );       // just for the record in order to plot summary at the end of the function
  _n_objects = 0;
  // STEP 2 : LOOP 1 OVER THE PHASES (compute the number of spheres)
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double rx = _param[2+5*p+0];
    double ry = _param[2+5*p+1];
    double rz = _param[2+5*p+2];
    std::cout << ".\t rays of phase " << p << std::endl;
    std::cout << ".\t .\t rx = " << rx << std::endl;
    std::cout << ".\t .\t ry = " << ry << std::endl;
    std::cout << ".\t .\t rz = " << rz << std::endl;
    double volf = _param[2+5*p+3]*volf_tot;
    volf_per_phase[p] = volf;
    double rax = 0.0; if( !_inside ) { rax = 4.*rx/3.; } // radius added in case  inside == False
    double ray = 0.0; if( !_inside ) { ray = 4.*ry/3.; } // radius added in case  inside == False
    double raz = 0.0; if( !_inside ) { raz = 4.*rz/3.; } // radius added in case  inside == False
    n_spheres_per_phase[p] = volf*( (dx+rax)*(dy+ray)*(dz+raz) ) * 3./(4*M_PI*(rx*ry*rz)); // compute the number of spheres
    _n_objects += n_spheres_per_phase[p];
    // test if minimal radius rmin > rejection length
    if( (rx < reje_len)|| (ry < reje_len)||(rz < reje_len)) {
      std::string msg = "minimal radius lower than rejection length";
      print_error( msg, true );
    }
  } // end loop 1 over phases
  // STEP 3 : CREATION OF THE _objects vector
  _objects.resize( _n_objects ); for( unsigned int i=0; i<_n_objects; i++ ) { _objects[i].resize( 7 ); }
  // LOOP 2 OVER THE PHASES (put the spheres randomly)
  // keep track of the indice in the global _objects vector
  unsigned int pi = 0;
  std::vector<double> volf_per_phase_real( _n_phases );  // just for the record in order to plot summary at the end of the function
  double volf_tot_real = 0.0;
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double rx = _param[5*p+2+0];
    double ry = _param[5*p+2+1];
    double rz = _param[5*p+2+2];
    double valu = _param[5*p+2+4];  _phases_values[p] = valu;
    volf_per_phase_real[p] = 0.0;
    // to compare the resulting volume fraction with the input
    std::random_device r;
    std::default_random_engine generator( r() );
    std::uniform_real_distribution<double> u_distr_x( ox+rx, ox+dx-rx );
    std::uniform_real_distribution<double> u_distr_y( oy+ry, oy+dy-ry );
    std::uniform_real_distribution<double> u_distr_z( oz+rz, oz+dz-rz );
    // LOOP OVER THE SPHERES (set radius, x, y, z and field value)
    for( unsigned int i=0; i<n_spheres_per_phase[p]; i++ ) {
      _objects[pi][0] = u_distr_x( generator ); // position x
      _objects[pi][1] = u_distr_y( generator ); // position y
      _objects[pi][2] = u_distr_z( generator ); // position z
      _objects[pi][3] = rx; // radius
      _objects[pi][4] = ry; // radius
      _objects[pi][5] = rz; // radius
      _objects[pi][6] = valu;                   // value of the field
      volf_per_phase_real[p] += 4.*M_PI*_objects[pi][3]*_objects[pi][4]*_objects[pi][5]/(3.*(dx*dy*dz));
      pi++;
    }
    volf_tot_real += volf_per_phase_real[p];
  }
  // Output VOLUME FRACTION
  std::cout << ".\t volume fraction" << std::endl;
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double a = volf_per_phase[p];
    double b = volf_per_phase_real[p];
    std::cout << std::fixed << std::setprecision(4) << ".\t .\t phase " << p << " --- target: " << a << " actual: " << b << " error: "  << std::setprecision(0) << std::abs(a-b)/a*100. << "%" << std::endl;
  }
  double a = volf_tot;
  double b = volf_tot_real;
  std::cout << std::fixed << std::setprecision(4) << ".\t .\t total ----- target: " << a << " actual: " << b << " error: "  << std::setprecision(0) << std::abs(a-b)/a*100. << "%" << std::endl;
  // Output VOLUME FRACTION
  std::cout << ".\t number of ellipsoids" << std::endl;
  for( unsigned int p=0; p<_n_phases; p++ ) {
    double a = n_spheres_per_phase[p];
    std::cout << ".\t .\t phase " << p << ": " << a << std::endl;
  }
  std::cout << ".\t .\t total  : " << _n_objects << std::endl;
  std::cout << ">" << std::endl;
}


/***************************/
/* PACK OBJECTS            */
/*   pack_spheres()        */
/*   pack_ellipsoids()     */
/***************************/

void crpacking::pack_spheres() {
  // Output
  std::cout << "<crpacking::pack_spheres" << std::endl;
  // STEP: increase sphere radii by reje_len
  double reje_len = _param[1];
  for( unsigned int i=0; i<_n_objects; i++ ) { _objects[i][0] += reje_len; }
  // WHILE
  __int_n = 1; // number of intersections
  unsigned int wit = 0; // while iteration (start at 1)
  if( do_write_objects_vtk ) {
    std::stringstream ss;  ss << std::setw(5) << std::setfill('0') << wit;
    std::string vtk_file = _field_file+"_"+ss.str()+".vtk";
    write_sphere_vtk( vtk_file );
  }
  // variable for the iteratif process
  double ener_o = 1.0;
  double ener_i = 1.0;
  double phi = 1.0;
  double err = 0.0001;
  unsigned int wit_max = 2000;
  unsigned int wit_min = 1;
  std::cout << ".\t iterations" << std::endl;
  while( ( phi > err && wit < wit_max ) || wit < wit_min  ) {
    wit++;
    double volu_tot_moving = 0.0;
    double dist_tot_moving = 0.0;
    // computes distances if intersection
    set_intersections( 0 ); // 0 for spheres
    // LOOP OVER INTERSECTED SPHERES
    for( unsigned int i=0; i<__int_s.size(); i++ ) {
      _objects[__int_s[i]][1] += __int_p[i][0];
      _objects[__int_s[i]][2] += __int_p[i][1];
      _objects[__int_s[i]][3] += __int_p[i][2];
      // check if it does not go out of the domain
      double add_r = 0.0;
      if( _inside ) { add_r = _objects[__int_s[i]][0]; } // add radius if inside


      // in case of a cube
      if( _domain_type == "cube" ) {
        for( unsigned int j=0; j<3; j++ ) {
          if( ( _objects[__int_s[i]][j+1]+add_r ) > (_origi[j]+_delta[j]) ) {
            _objects[__int_s[i]][j+1] = _origi[j]+_delta[j]-add_r;
          }
          else if( ( _objects[__int_s[i]][j+1]-add_r ) < _origi[j] ) {
            _objects[__int_s[i]][j+1] = _origi[j]+add_r;
          }
        }
      } else if ( _domain_type == "cylinder" ) { // in case of a cylinder
            double x = _objects[__int_s[i]][1]; // x of center of sphere
            double y = _objects[__int_s[i]][2]; // y of center of sphere
            double z = _objects[__int_s[i]][3]; // z of center of sphere
            double r  = 0.5*_delta[0]; // radius of the circle
            double x0 = r + _origi[0]; // x center of circle
            double y0 = r + _origi[1]; // y center of circle
            double h = _delta[2];                  // height of the cylinder
            double d  = sqrt( pow(x-x0, 2) + pow(y-y0, 2) ); // initial distance between center of circle and sphere
            // test over height (z direction)
            if( z+add_r > _origi[2]+h ) {
            _objects[__int_s[i]][3] = _origi[2]+h-add_r;
            }
            else if( z-add_r < _origi[2] ) {
            _objects[__int_s[i]][3] = _origi[2]+add_r;
            }
            if( d+add_r > r ) {             // test > radius
                _objects[__int_s[i]][1] = (x-x0)*(r-add_r)/d + x0;
                _objects[__int_s[i]][2] = (y-y0)*(r-add_r)/d + y0;
            }
      } else {
        std::string msg = "unkown domain type \'"+_domain_type+"\'";
        print_error( msg, true );
      }
      // compute a kind of total energy E = \sum volume_i*distance_i / volume_domaine
      dist_tot_moving += sqrt( pow( __int_p[i][0], 2) +
			       pow( __int_p[i][1], 2) +
			       pow( __int_p[i][2], 2) );
      volu_tot_moving += 4.*M_PI*pow( _objects[i][0]-reje_len ,3)/3.;
    } // END LOOP OVER INTERSECTED SPHERES
    if( wit == 1 ) {
      ener_o = dist_tot_moving * volu_tot_moving;
    }
    ener_i = dist_tot_moving * volu_tot_moving;
    if( ener_o < 1e-16 ) {
      phi = 0.0;
    } else {
      phi = ener_i/ener_o;
    }
    std::cout << ".\t .\t";
    std::cout << " iter: "  << std::setw(5) << std::setfill('0')    << wit;
    std::cout << " phi: "   << std::fixed   << std::setprecision(5) << phi;
    std::cout << " n_int: " << std::setw(5) << std::setfill('0')    << __int_n;
    std::cout << std::endl;
    if( do_write_objects_vtk ){
      std::stringstream ss;  ss << std::setw(5) << std::setfill('0') << wit;
      std::string vtk_file = _field_file+"_"+ss.str()+".vtk";
      write_sphere_vtk( vtk_file );
    }
  }
  wit++;
  // STEP: decrease sphere radii by reje_len
  for( unsigned int i=0; i<_n_objects; i++ ) { _objects[i][0] -= reje_len; }
  set_intersections( 0 ); // 0 for spheres
  std::cout << ".\t radius reduction                 n_int: " << __int_n << std::endl;
  if( do_write_objects_vtk ){
    std::string vtk_file = _field_file+"_final.vtk";
    write_sphere_vtk( vtk_file );
  }
  std::cout << ">" << std::endl;
}

void crpacking::pack_ellipsoids(){
  // Output
  std::cout << "<crpacking::pack_ellipsoids" << std::endl;
  // STEP : increase sphere radii by reje_len
  double reje_len = _param[1];
  for( unsigned int i=0; i<_n_objects; i++ ) {
    _objects[i][3] += reje_len/2.0;
    _objects[i][4] += reje_len/2.0;
    _objects[i][5] += reje_len/2.0;
  }
  // WHILE
  __int_n = 1; // number of intersections
  unsigned int wit = 0; // while iteration (start at 1)
  // variable for the iteratif process
  double ener_o = 1.0;
  double ener_i = 1.0;
  double phi = 1.0;
  double err = 0.00001;
  unsigned int wit_max = 2000;
  unsigned int wit_min = 1;
  std::cout << ".\t iterations" << std::endl;
  while( ( phi > err && wit < wit_max ) || wit < wit_min  ) {
    wit++;
    double volu_tot_moving = 0.0;
    double dist_tot_moving = 0.0;
    // computes distances if intersection
    set_intersections( 1 ); // 1 for ellipsoids
    // LOOP OVER INTERSECTED SPHERES
    for( unsigned int i=0; i<__int_s.size(); i++ ) {
      _objects[__int_s[i]][0] += __int_p[i][0];
      _objects[__int_s[i]][1] += __int_p[i][1];
      _objects[__int_s[i]][2] += __int_p[i][2];
      // check if it does not go out of the domain
      std::vector<double> add_r(3,0.0);
      if( _inside ) {
        add_r[0] = _objects[__int_s[i]][3]-reje_len/2.0;
        add_r[1] = _objects[__int_s[i]][4]-reje_len/2.0;
        add_r[2] = _objects[__int_s[i]][5]-reje_len/2.0;
      } // add radius if inside
      for( unsigned int j=0; j<3; j++ ) {
	if( ( _objects[__int_s[i]][j]+(add_r[j]) ) > (_origi[j]+_delta[j]) ) {
	  _objects[__int_s[i]][j] = _origi[j]+_delta[j]-add_r[j];
	}
	else if( ( _objects[__int_s[i]][j]-add_r[j] ) < _origi[j] ) {
	  _objects[__int_s[i]][j] = _origi[j]+add_r[j];
	}
      }
      // compute a kind of total energy E = \sum volume_i*distance_i / volume_domaine
      dist_tot_moving += sqrt( pow( __int_p[i][0], 2) +
			       pow( __int_p[i][1], 2) +
			       pow( __int_p[i][2], 2) );
      volu_tot_moving += 4.*M_PI*( _objects[i][3]-reje_len/2.0)*(_objects[i][4]-reje_len/2.0)*(_objects[i][5]-reje_len/2.0)/3.;
    } // END LOOP OVER INTERSECTED SPHERES
    if( wit == 1 ) {
      ener_o = dist_tot_moving * volu_tot_moving;
    }
    ener_i = dist_tot_moving * volu_tot_moving;
    if( ener_o < 1e-16 ) {
      phi = 0.0;
    } else {
      phi = ener_i/ener_o;
    }
    std::cout  << ".\t .\t iter: ";
    std::cout << std::setw(5) << std::setfill('0') << wit;
    std::cout << std::fixed << std::setprecision(5) << " phi: " << phi << " n_int: " << __int_n << std::endl;
  }
  wit++;
  // STEP : decrease sphere radii by reje_len
  for( unsigned int i=0; i<_n_objects; i++ ) {
    _objects[i][3] -= reje_len/2.0;
    _objects[i][4] -= reje_len/2.0;
    _objects[i][5] -= reje_len/2.0;
  }
  set_intersections( 1 ); // 1 for ellipsoids
  std::cout << ".\t radius reduction           n_int: " << __int_n << std::endl;
  std::cout << ">" << std::endl;
}


/***************************/
/* READ OBJECTS            */
/*   read_spheres()        */
/*   read_ellipsoids()     */
/***************************/

void crpacking::read_objects() {
  std::cout << "<crpacking::read_objects" << std::endl;
  _n_objects=0;
  std::ifstream file( _objects_file );
  if ( file ) {
    std::cout << ".\t objects file: " << _objects_file << std::endl;
    std::string line;
    while( std::getline( file, line ) ) {
      line.erase(std::remove(line.begin(),line.end(),' '),line.end()); // remove spaces
      if( line.compare( 0, 1, "#" ) ) {
	std::string::size_type stTemp = line.find(",");
	std::vector<double> vecTemp; int i = 0;
	while(stTemp != std::string::npos) {
	  vecTemp.push_back( std::stod( line.substr(0, stTemp) ) );
	  line = line.substr(stTemp + 1);
	  stTemp = line.find(',');
	  i++;
	}
	vecTemp.push_back( std::stod( line ) );
	if( std::find(_phases_values.begin(), _phases_values.end(), vecTemp.back()) == _phases_values.end() ) {
	  _phases_values.push_back( vecTemp.back() );
	}
	_n_objects++;  _objects.push_back( vecTemp );
      }
    }
    _n_phases = _phases_values.size();
    std::cout << ".\t number of objects: " << _n_objects << std::endl;
    std::cout << ".\t number of parameters: " << _objects[0].size() << std::endl;
    std::cout << ".\t number of phases: " << _n_phases << std::endl;
    for( unsigned int i=0; i<_phases_values.size(); i++ ) {
      std::cout << ".\t .\t value of phase " << i+1 << ": " << _phases_values[i] << std::endl;
    }
  } else {
    std::string msg = "can\'t open vtk file file \'"+_objects_file+"\'";
    print_error( msg, true );
  }
  std::cout << ">" << std::endl;
}

void crpacking::set_objects( std::vector<std::vector<double> > objects, std::vector<unsigned int> phases_values ) {
  std::cout << "<crpacking::set_objects" << std::endl;
  _objects = objects;
  _phases_values = phases_values;
  _n_objects = _objects.size();
  _n_phases = _phases_values.size();
  std::cout << ">" << std::endl;
}

/***************************/
/* FIELD                   */
/*   convert_to_field()    */
/*   write_vtk()           */
/*   write_field_vtk()     */
/***************************/

void crpacking::convert_to_field() {
  std::cout << "<crpacking::convert_to_field"  << std::endl;
  // get the actual number of phase (merging phases with same values)
  unsigned int n_phases_tmp = _n_phases;
  std::sort(_phases_values.begin(), _phases_values.end());
  auto last = std::unique(_phases_values.begin(), _phases_values.end());
  _phases_values.erase(last, _phases_values.end());
  _n_phases = _phases_values.size();
  if( _n_phases != n_phases_tmp ) {
    std::cout << ".\t merge phases with same values (" << n_phases_tmp << " -> " << _n_phases << ")" << std::endl;
  }
  // resize and fill the vector _v_field
  _v_field.resize( _n_phases );
  for( unsigned int p=0; p<_n_phases; p++ ) {
    _v_field[p].resize( _n_nodes[0]*_n_nodes[1]*_n_nodes[2] );
    for( unsigned int i=0; i<_v_field[p].size(); i++ ) {
      _v_field[p][i] = 0;
    }
  }
  std::cout << ".\t number of nodes: " << _n_nodes[0] << "x" << _n_nodes[1] << "x" << _n_nodes[2] << " = " << _v_field[0].size() << std::endl;
  if( std::any_of(_n_nodes.begin(), _n_nodes.end(), [](int i){return i==0;}) ){
    std::string msg = "number of nodes <=0";
    print_error( msg, true );
  }

  // determine type of object based on _object[0].size()
  // _object[0].size() == 5 -> spheres
  // _object[0].size() == 7 -> ellipsoids
  if( _objects[0].size() == 5 ) {
    std::cout << ".\t type of objects: spheres" << std::endl;
    // Triple nested loop overs mesh nodes and fourth nested loop over objects
    for( unsigned int p=0; p<_n_phases; p++ ) {
      std::cout << ".\t .\t value of phase " << p << ": " << _phases_values[p] << std::endl;
      unsigned int i_nodes=0;
      for( unsigned iz=0; iz<_n_nodes[2]; iz++ ) {
	double z = double(iz)*_elem_size[2]+_origi[2];

	if( do_print_progress ) {
	  double percentage = (double) (iz+1) / (double) _n_nodes[2];
	  int val = (int) (percentage * 100);
	  int lpad = (int) (percentage * PBWIDTH);
	  int rpad = PBWIDTH - lpad;
	  printf ("\r.\t .\t progress: %3d%% [%.*s%*s]", val, lpad, PBSTR, rpad, "");
	  fflush (stdout);
	}

	for( unsigned iy=0; iy<_n_nodes[1]; iy++ ) {
	  double y = double(iy)*_elem_size[1]+_origi[1];
	  for( unsigned ix=0; ix<_n_nodes[0]; ix++ ) {
	    double x = double(ix)*_elem_size[0]+_origi[0];
	    double dsmallest = 1e100;
	    unsigned int iosmallest = 0;
	    // loop over all spheres for one node
	    for( unsigned int io=0; io<_n_objects; io++ ) {
	      if( _phases_values[p] == (unsigned int)(_objects[io][4]) ){
		// compute distance between node and sphere radius
		double d = sqrt(    pow( _objects[io][1] - x, 2 ) +
				    pow( _objects[io][2] - y, 2 ) +
				    pow( _objects[io][3] - z, 2 ) );
		// record the closest object
		if ( (d-_objects[io][0]) < (dsmallest-_objects[iosmallest][0]) ) {
		  dsmallest = d;
		  iosmallest = io;
		}
	      }
	    } // end loop objects
	    _v_field[p][i_nodes] = (double)(_objects[iosmallest][4])*(1.0-dsmallest/_objects[iosmallest][0]);
	    i_nodes++;
	  } // end loop x
	} // end loop y
      } // end loop z

      if( do_print_progress ) { std::cout << std::endl; }
    } // end loop phase
  } else if( _objects[0].size() == 7 ) {
    std::cout << ".\t type of objects: ellipsoids" << std::endl;
    // Triple nested loop overs mesh nodes and fourth nested loop over objects
    for( unsigned int p=0; p<_n_phases; p++ ) {
      std::cout << ".\t .\t value of phase " << p << ": " << _phases_values[p] << std::endl;
      unsigned int i_nodes=0;
      for( unsigned iz=0; iz<_n_nodes[2]; iz++ ) {
	double z = double(iz)*_elem_size[2];
	for( unsigned iy=0; iy<_n_nodes[1]; iy++ ) {
	  double y = double(iy)*_elem_size[1];
	  for( unsigned ix=0; ix<_n_nodes[0]; ix++ ) {
	    double x = double(ix)*_elem_size[0];
	    double dsmallest = 1e100;
	    unsigned int iosmallest = 0;
	    // loop over all spheres for one node
	    for( unsigned int io=0; io<_n_objects; io++ ) {
	      if( _phases_values[p] == (unsigned int)(_objects[io][6]) ){
		// compute distance between node and sphere radius
		double d = sqrt(    pow( (_objects[io][0] - x)/_objects[io][3], 2 ) +
				    pow( (_objects[io][1] - y)/_objects[io][4], 2 ) +
				    pow( (_objects[io][2] - z)/_objects[io][5], 2 ) );
		// record the closest object
		if ( d < dsmallest ) {
		  dsmallest = d;
		  iosmallest = io;
		}
	      }
	    } // end loop objects
	    _v_field[p][i_nodes] = (double)(_objects[iosmallest][6])*(1.0-dsmallest);
	    i_nodes++;
	  } // end loop x
	} // end loop y
      } // end loop z
    } // end loop phase
  }
  if( do_print_progress ) { std::cout << std::endl; }
  std::cout << ">" << std::endl;
}

void crpacking::write_field(){
  std::cout << "<crpacking::write_field" << std::endl;
  for( unsigned int p=0; p<_n_phases; p++) {
    std::ofstream pfile;
    std::string file_name = _field_file+"_phase_"+std::to_string( p )+".dat";
    pfile.open( file_name, std::ios::out | std::ios::trunc );
    std::string sep = ", ";
    if ( pfile ) {
      std::cout << ".\t field file: " << file_name << std::endl;
      std::cout << ".\t .\t line 1 field size:\t" << _delta[0] << ", " << _delta[1] << ", " << _delta[2] << std::endl;
      pfile << _delta[0] << ", " << _delta[1] << ", " << _delta[2] << std::endl;
      std::cout << ".\t .\t line 2 field origin:\t" << _origi[0] << ", " << _origi[1] << ", " << _origi[2] << std::endl;
      pfile << _origi[0] << ", " << _origi[1] << ", " << _origi[2] << std::endl;
      std::cout << ".\t .\t line 3 field nodes:\t" << _n_nodes[0] << ", " << _n_nodes[1] << ", " << _n_nodes[2] << std::endl;
      pfile << _n_nodes[0] << ", " << _n_nodes[1] << ", " << _n_nodes[2] << std::endl;
      std::cout << ".\t .\t line 4 to " <<  3+_v_field[p].size() << ": field values" << std::endl;
      for(unsigned int i=0; i<_v_field[p].size(); i++) {
	pfile << _v_field[p][i] << std::endl;
      }
      pfile.close();
    } else {
      std::string msg = "can\'t open field file \'"+file_name+"\'";
      print_error( msg, true );
    }
  }
  std::cout << ">" << std::endl;
}

void crpacking::write_field_vtk(){
  std::cout << "<crpacking::write_field_vtk" << std::endl;
  for( unsigned int p=0; p<_n_phases; p++) {
    std::ofstream vtk_file;
    std::string file_name = _field_file+"_phase_"+std::to_string( p )+".vtk";
    vtk_file.open( file_name, std::ios::out | std::ios::trunc );
    std::string sep = " ";
    std::vector<unsigned int> _n_nodes( 3 );
    for( unsigned int i=0; i<3; i++ ) {
      _n_nodes[i] = _n_elem[i]+1;
    }
    const unsigned int _n_nodes_c = _n_nodes[0]*_n_nodes[1]*_n_nodes[2];
    if ( vtk_file ) {
      std::cout << ".\t write vtk file: " << file_name << std::endl;
      // STEP 1 - write header
      vtk_file << "# vtk DataFile Version 2.0" << std::endl;
      vtk_file << "VTK file from projmorpho: " << file_name << std::endl;
      vtk_file << "ASCII" << std::endl;
      vtk_file << "DATASET STRUCTURED_POINTS" << std::endl;
      vtk_file << "DIMENSIONS "   << _n_nodes[0]    << " " << _n_nodes[1]    << " " << _n_nodes[2]    << std::endl;
      vtk_file << "ASPECT_RATIO " << _elem_size[0] << " " << _elem_size[1] << " " << _elem_size[2] << std::endl;
      vtk_file << "ORIGIN "       << _origi[0]     << " " << _origi[1]     << " " << _origi[2]     << std::endl;
      vtk_file << std::endl;
      // STEP 5 - write point data
      vtk_file << "POINT_DATA " <<_n_nodes_c << std::endl;
      vtk_file << "SCALARS Field float" << std::endl;
      vtk_file << "LOOKUP_TABLE default" << std::endl;
      for(unsigned int i = 0; i < _n_nodes_c;i++){
	vtk_file << _v_field[p][i] << std::endl;
      }
      vtk_file << std::endl;
      vtk_file.close();
    } // End if(vtk_file)
    else {
      std::string msg = "can\'t open vtk file \'"+_field_file+".vtk\'";
      print_error( msg, true );
    }
  }
  std::cout << ">" << std::endl;
}

/***************************/
/* GET                     */
/*   get_field()           */
/***************************/

std::vector< std::vector< float > >    crpacking::get_field()   { return _v_field; }
std::vector< double >   crpacking::get_origin()  { return _origi; }
std::vector< double >   crpacking::get_length()  { return _delta; }
std::vector< unsigned > crpacking::get_n_nodes() { return _n_nodes; }


/***********************************/
/*             PRIVATE             */
/***********************************/

void crpacking::parser( const std::string& config ) {
  std::ifstream file( config );
  if( file ) {
    std::string line;
    while( std::getline( file, line ) ) {
      line.erase(std::remove(line.begin(),line.end(),' '),line.end()); // remove spaces
      line.erase(std::remove(line.begin(),line.end(),')'),line.end()); // remove (
      line.erase(std::remove(line.begin(),line.end(),'('),line.end()); // remove )
      std::istringstream iss( line );
      std::string key; std::string value;
      if( std::getline( iss, key , '=') ) { // read key
	if( key == "field" ) { // field file name
	  std::getline( iss, value );
	  _field_file = value;
	}
    if( key == "domaintype" ) { // domain type
	  std::getline( iss, value );
	  _domain_type = value;
	}
	if( key == "objects" ) { // sphere file name
	  std::getline( iss, value );
	  _objects_file = value;
	}
	if( key == "inside" ) { // delta
	  std::getline( iss, value );
	  _inside = std::stoi( value );
	}
	if( key == "delta" ) { // delta
	  unsigned int i = 0;
	  while( std::getline( iss, value, ',' ) ) {
	    _delta[i] = std::stod( value ); i++;
	  }
	  if( i == 1 ) { // if only one given assume its a cube
	    _delta[1] = ( _delta[0] );
	    _delta[2] = ( _delta[0] );
	  }
	  else if( i == 2 || i > 3 ) {
	    std::string msg = "delta:  1 or 3 dimensions needed ("+std::to_string( i )+" given)";
	    print_error( msg, true );
	  }
	} // end delta
	if( key == "origin" ) { // origi
	  unsigned int i = 0;
	  while( std::getline( iss, value, ',' ) ) {
	    _origi[i] = std::stod( value ); i++;
	  }
	  if( i == 1 ) { // if only one given assume its a cube
	    _origi[1] = ( _origi[0] );
	    _origi[2] = ( _origi[0] );
	  }
	  else if( i == 2 || i > 3 ) {
	    std::string msg = "origi:  1 or 3 dimensions needed ("+std::to_string( i )+" given)";
	    print_error( msg, true );
	  }
	} // end origi
	if( key == "numberelem" ) { // elem_size
	  unsigned int i = 0;
	  while( std::getline( iss, value, ',' ) ) {
	    _n_elem[i] = std::stoi( value );
	    _n_nodes[i] = _n_elem[i]+1;
	    if( _n_elem[i] == 0 ) {
	      std::string msg = "number of element = 0 in direction ("+std::to_string( i )+")";
	      print_error( msg, true );
	    }
	    i++;
	  }
	  if( i == 1 ) { // if only one given assume its a cube
	    _n_elem[1] = ( _n_elem[0] );
	    _n_elem[2] = ( _n_elem[0] );
	    _n_nodes[1] = ( _n_elem[0]+1 );
	    _n_nodes[2] = ( _n_elem[0]+1 );
	  }
	  else if( i == 2 || i > 3 ) {
	    std::string msg = "elem_size:  1 or 3 dimensions needed ("+std::to_string( i )+" given)";
	    print_error( msg, true );
	  }
	} // end elem_size
	if( key == "param" ) { // param
	  while( std::getline( iss, value, ',' ) ) {
	    _param.push_back( std::stod( value ) );
	  }
	} // end param
      }
    }
  } else {
    std::string msg = "can\'t open config file \'"+config+"\'";
    print_error( msg, true );
  }
}

/* used in packing algo */
void crpacking::set_intersections( unsigned int type ) {
  __int_s.clear();
  __int_p.clear();
  __int_n = 0;
  // type == 0 -> spheres
  // type == 1 -> ellipsoids
  if( type == 0 ) {
    // computes distances if intersection
    for( unsigned int i=0; i<_n_objects; i++ ) {
      std::vector<double> push(3);
      push[0] = 0.0; push[1] = 0.0; push[2] = 0.0;
      bool intersect = false;
      for( unsigned int j=0; j<_n_objects; j++ ) {
	if( i != j ) {
	  double d = sqrt( pow( _objects[i][1] - _objects[j][1], 2 ) +
			   pow( _objects[i][2] - _objects[j][2], 2 ) +
			   pow( _objects[i][3] - _objects[j][3], 2 ) );
	  double rpr = _objects[i][0]+_objects[j][0];
	  if( d < rpr ) { 	// intersection between i and j
	    intersect = true;
	    double alpha = _objects[j][0]*( pow( d/rpr , 2 )  - 1. );
	    std::vector<double> beta( 3 );
	    for( unsigned int k=0; k<3; k++ ) {
	      if( d>0.0000001 ) { beta[k] = ( _objects[j][k+1] - _objects[i][k+1] )/d; }
	      else { beta[k] = 1.0; }
	      push[k] += alpha*beta[k];
	    }
	    // std::cout << d << " " << alpha << " " << push[0] << " "  << push[1] << " "  << push[2] << std::endl;
	  }
	}
      }
      if( intersect ) {
	__int_n++;
	__int_s.push_back( i ); // record sphere to move
	__int_p.push_back( push ); // record how to move it
      }
    }
  } else if( type == 1 ) {
    std::vector<double> tmp_res;
    std::vector<double> tmp_res2;
    double coeff;
    // computes distances if intersection
    for( unsigned int i=0; i<_n_objects; i++ ) {
      std::vector<double> push(3,0.0);
      bool intersect = false;
      for( unsigned int j=0; j<_n_objects; j++ ) {
	if((i!=j)&&(_objects[i][3]==_objects[j][3])&&(_objects[i][4]==_objects[j][4])&&(_objects[i][5]==_objects[j][5])){
	  tmp_res = determine_sphero(_objects[j],_objects[i]);
	  if((tmp_res[0] >0)){
	    intersect = true;
	    coeff = tmp_res[1]*(pow((tmp_res[3]/(tmp_res[1] + tmp_res[2])),2) - 1);
	    if((_objects[j][0] != _objects[i][0]) || (_objects[i][1] != _objects[j][1]) || (_objects[i][2] != _objects[j][2])){
	      for(unsigned k=0;k<3;k++){
		push[k]+=(_objects[j][k] - _objects[i][k])/tmp_res[3]*coeff*_objects[j][k+3]/tmp_res[1];
	      }
	    }
	    else{
	      if(i>j){
		for(unsigned k=0;k<3;k++){
		  push[k]+=tmp_res[2];
		}
	      }
	      else{
		for(unsigned k=0;k<3;k++){
		  push[k]+=(-1*tmp_res[2]);
		}
	      }
	    }
	  }
	}
	else if(i!=j){
	  tmp_res = determine_sphero(_objects[i],_objects[j]);
	  if((tmp_res[0]>0)){
	    intersect = true;
	    coeff = tmp_res[1]*(pow((tmp_res[3]/(tmp_res[1] + tmp_res[2])),2) - 1);
	    if((_objects[i][0] != _objects[j][0]) || (_objects[i][1] != _objects[j][1]) || (_objects[i][2] != _objects[j][2])){
	      for(unsigned k=0;k<3;k++){
		push[k]+=(_objects[j][k] - _objects[i][k])/tmp_res[3]*coeff*_objects[j][k+3]/tmp_res[1];
	      }
	    }
	    else{
	      if(i>j){
		for(unsigned k=0;k<3;k++){
		  push[k]+=tmp_res[2];
		}
	      }
	      else{
		for(unsigned k=0;k<3;k++){
		  push[k]+=(-1*tmp_res[2]);
		}
	      }
	    }
	  }
	  else{
	    double rsphere=0;
	    if((_objects[i][3] == _objects[i][4])&&(_objects[i][3] == _objects[i][5])){
	      tmp_res2 = inter_sphero(_objects[j],_objects[i]);
	      tmp_res[1] = tmp_res2[0];
	      tmp_res[2] = _objects[i][4];
	      rsphere = _objects[i][4];
	    }
	    else if((_objects[j][3] == _objects[j][4])&&(_objects[j][3] == _objects[j][5])){
	      tmp_res2 = inter_sphero(_objects[i],_objects[j]);
	      tmp_res[1] = _objects[j][4];
	      tmp_res[2] = tmp_res2[0];
	      rsphere = _objects[j][4];
	    }
	    else{
	      std::string msg = "ellipsoids packing: case with two ellipsoids of different parameters not taken into account";
	      print_error( msg, true );
	    }
	    if(rsphere>tmp_res2[4]){
	      intersect = true;
	      coeff = tmp_res[1]*(pow((tmp_res[3]/(tmp_res[1] + tmp_res[2])),2) - 1);
	      if((_objects[j][0] != _objects[i][0]) || (_objects[i][1] != _objects[j][1]) || (_objects[i][2] != _objects[j][2])){
		for(unsigned k=0;k<3;k++){
		  push[k]+=(_objects[j][k] - _objects[i][k])/tmp_res[3]*coeff*_objects[j][k+3]/tmp_res[1];
		}
	      }
	      else{
		if(i>j){
		  for(unsigned k=0;k<3;k++){
		    push[k]+=tmp_res[2];
		  }
		}
		else{
		  for(unsigned k=0;k<3;k++){
		    push[k]+=(-1*tmp_res[2]);
		  }
		}
	      }
	    }
	  }
	}
      }
      if( intersect ) {
	__int_n++;
	__int_s.push_back( i ); // record sphere to move
	__int_p.push_back( push ); // record how to move it
      }
    }
  } else {
    std::string msg = "no type \'"+std::to_string( type )+"\' implemented in crpacking::set_intersections( unsigned int type )";
    print_error( msg, true );
  }
}

/* specific functions for ellipsoids */
std::vector<double> crpacking::determine_sphero(const std::vector<double> &s1,const std::vector<double> &s2){
  double k1 = 1.0/sqrt(pow((s1[0]-s2[0])/s1[3],2)+pow((s1[1]-s2[1])/s1[4],2)+pow((s1[2]-s2[2])/s1[5],2));
  double k2 = 1.0/sqrt(pow((s1[0]-s2[0])/s2[3],2)+pow((s1[1]-s2[1])/s2[4],2)+pow((s1[2]-s2[2])/s2[5],2));
  double d1=sqrt(pow(s1[0]-((s2[0]-s1[0])*k1+s1[0]),2)+pow(s1[1]-((s2[1]-s1[1])*k1+s1[1]),2)+pow(s1[2]-((s2[2]-s1[2])*k1+s1[2]),2));
  double d2=sqrt(pow(s2[0]-((s1[0]-s2[0])*k2+s2[0]),2)+pow(s2[1]-((s1[1]-s2[1])*k2+s2[1]),2)+pow(s2[2]-((s1[2]-s2[2])*k2+s2[2]),2));
  double d3 = sqrt(pow(s1[0]-s2[0],2)+pow(s1[1]-s2[1],2)+pow(s1[2]-s2[2],2));
  double dist=0;
  if(d1+d2>d3){
    dist = sqrt(pow((s2[0]-s1[0])*k1+s1[0]-(s1[0]-s2[0])*k2-s2[0],2)+pow((s2[1]-s1[1])*k1+s1[1]-(s1[1]-s2[1])*k2-s2[1],2)+pow((s2[2]-s1[2])*k1+s1[2]-(s1[2]-s2[2])*k2-s2[2],2));
  }
  std::vector<double> result(4);
  result[0] = dist;
  result[1] = d1;
  result[2] = d2;
  result[3] = d3;
  return result;
}

/* specific functions for ellipsoids */
std::vector<double> crpacking::inter_sphero(const std::vector<double> &s1,const  std::vector<double> &s2){
  double x0 = 0;
  double x1 = 0.1;
  int count =0;
  while(fabs((x1-x0)/x1)>0.001){
    x0=x1;
    double sum1 = pow(1.0/s1[3],2)*(s2[0]-s1[0])*(s2[0]-s1[0])/pow(1+x0*pow(1.0/s1[3],2),2);
    sum1+=pow(1.0/s1[4],2)*(s2[1]-s1[1])*(s2[1]-s1[1])/pow(1+x0*pow(1.0/s1[4],2),2);
    sum1+=pow(1.0/s1[5],2)*(s2[2]-s1[2])*(s2[2]-s1[2])/pow(1+x0*pow(1.0/s1[5],2),2);
    double sum2 = pow(1.0/s1[3],4)*(s2[0]-s1[0])*(s2[0]-s1[0])/pow(1+x0*pow(1.0/s1[3],2),3);
    sum2 += pow(1.0/s1[4],4)*(s2[1]-s1[1])*(s2[1]-s1[1])/pow(1+x0*pow(1.0/s1[4],2),3);
    sum2 += pow(1.0/s1[5],4)*(s2[2]-s1[2])*(s2[2]-s1[2])/pow(1+x0*pow(1.0/s1[5],2),3);
    x1=x0-(sum1-1)/(-2*sum2);
    count ++;
    if(count>1000){
      std::cout<<"Trop d'iteration dans le calcul de la distance minimum\n\n";
      break;
    }
  }
  std::vector<double> z(5);
  z[1] =(s2[0]-s1[0])/(1+x1*pow(1.0/s1[3],2))+s1[0];
  z[2] =(s2[1]-s1[1])/(1+x1*pow(1.0/s1[4],2))+s1[1];
  z[3] =(s2[2]-s1[2])/(1+x1*pow(1.0/s1[5],2))+s1[2];
  z[0] = sqrt(pow(s1[0]-z[1],2)+pow(s1[1]-z[2],2)+pow(s1[2]-z[3],2));
  z[4] = sqrt(pow(s2[0]-z[1],2)+pow(s2[1]-z[2],2)+pow(s2[2]-z[3],2));
  return z;
}

/* vtk for debug */
void crpacking::write_sphere_vtk( const std::string& file_name ){
  std::ofstream pfile;
  pfile.open( file_name, std::ios::out | std::ios::trunc );
  std::string sep = " ";
  if ( pfile ) {
    // write headers
    pfile << "# vtk DataFile Version 2.0" << std::endl;
    pfile << "Unstructured grid legacy vtk file with point scalar data" << std::endl;
    pfile << "ASCII" << std::endl;
    pfile << std::endl;
    // centers
    pfile << "DATASET UNSTRUCTURED_GRID" << std::endl;
    pfile << "POINTS " << _n_objects << " float" << std::endl;
    for(unsigned int i=0; i<_n_objects; i++) {
      pfile << _objects[i][1] << sep
	    << _objects[i][2] << sep
	    << _objects[i][3] << std::endl;
    }
    pfile << std::endl;
    // radii
    pfile << "POINT_DATA " << _n_objects << std::endl;
    pfile << "SCALARS radii float" << std::endl;
    pfile << "LOOKUP_TABLE default" << std::endl;
    for(unsigned int i=0; i<_n_objects; i++) {
      pfile << _objects[i][0] << std::endl;
    }
    pfile << std::endl;
    // radii
    pfile << "SCALARS field float" << std::endl;
    pfile << "LOOKUP_TABLE default" << std::endl;
    for(unsigned int i=0; i<_n_objects; i++) {
      pfile << _objects[i][4] << std::endl;
    }
    pfile << std::endl;
    pfile.close();
  } else {
    std::string msg = "can\'t open vtk file file \'"+file_name+"\'";
    print_error( msg, true );
  }
}
