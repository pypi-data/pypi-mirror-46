#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <cmath>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

#include "tetrahedron.hpp"

std::vector<double> tetrahedron::get_interface( std::vector<std::vector<double> > c_tet, std::vector<double> theta_edge, std::vector<int> me ) {
  std::vector<std::vector<double> > c_theta; // coordinates of edge intersection  
  double u1, u2, u3, v1, v2, v3, n1, n2, n3; // compute normal with scalar product
  n1 = 1.0; n2 = 0.0; n3 = 0.0;              // default orientation value  
  unsigned int isw = 0;                      // configuration
  double sv = 0.0;                           // sub volume

  // CASE 1 NODE ISOLATED
  if ( (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 21 || // 1 node  in the paste and 3 in the aggregates
       (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 12 ){ // 3 nodes in the paste and 1 in the aggregates
    if ( ( me[0] + me[1] + me[2]) == 9 ){ // A isolated
      isw = 0; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
      u1 = c_theta[0][2] - c_theta[0][0]; u2 = c_theta[1][2] - c_theta[1][0]; u3 = c_theta[2][2] - c_theta[2][0];
      v1 = c_theta[0][1] - c_theta[0][0]; v2 = c_theta[1][1] - c_theta[1][0]; v3 = c_theta[2][1] - c_theta[2][0];
      n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
    } // end if sum = 9 A
    else if ( (me[3] + me[0] + me[4]) == 9 ){ // B isolated
      isw = 1; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
      u1 = c_theta[0][1] - c_theta[0][2]; u2 = c_theta[1][1] - c_theta[1][2]; u3 = c_theta[2][1] - c_theta[2][2];
      v1 = c_theta[0][0] - c_theta[0][2]; v2 = c_theta[1][0] - c_theta[1][2]; v3 = c_theta[2][0] - c_theta[2][2];
      n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
    } // end if sum = 9 B
    else if ( (me[4] + me[5] + me[2]) == 9 ){ // C isolated
      isw = 2; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
      u1 = c_theta[0][1] - c_theta[0][0]; u2 = c_theta[1][1] - c_theta[1][0]; u3 = c_theta[2][1] - c_theta[2][0];
      v1 = c_theta[0][2] - c_theta[0][0]; v2 = c_theta[1][2] - c_theta[1][0]; v3 = c_theta[2][2] - c_theta[2][0];
      n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
    } // end if sum = 9 C
    else if ( (me[1] + me[3] + me[5]) == 9 ){ // D isolated
      isw = 3; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
      u1 = c_theta[0][0] - c_theta[0][1]; u2 = c_theta[1][0] - c_theta[1][1]; u3 = c_theta[2][0] - c_theta[2][1];
      v1 = c_theta[0][2] - c_theta[0][1]; v2 = c_theta[1][2] - c_theta[1][1]; v3 = c_theta[2][2] - c_theta[2][1];
      n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
    } else { std::cout << "WARNING: no sub case found to compute interface orientation."  << std::endl; } // end if sum = 9 D
    sv = get_sub_volume_1n( c_tet, c_theta, isw );
    if ( (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 12 ){ // switch orientation vector
      n1 = -n1; n2 = -n2; n3 = -n3;
    }
  }

  // CASE 2 NODES ISOLATED
  else if ( (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 17 ) {
    if ( ((me[1]+me[0]+me[2])==10) && ((me[0]+me[3]+me[4])==10) ) { // A and B in aggregates
      isw = 0; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
      u1 = c_theta[0][0] - c_theta[0][1]; u2 = c_theta[1][0] - c_theta[1][1]; u3 = c_theta[2][0] - c_theta[2][1];
      v1 = c_theta[0][3] - c_theta[0][1]; v2 = c_theta[1][3] - c_theta[1][1]; v3 = c_theta[2][3] - c_theta[2][1];
      n1 = u2*v3-u3*v2; n2 = u3*v1-u1*v3; n3 = u1*v2-u2*v1;
    }
    else if ( ((me[1]+me[0]+me[2])==7) && ((me[0]+me[3]+me[4])==7) ) { // A and B in paste
      isw = 1; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
      u1 = c_theta[0][0] - c_theta[0][1]; u2 = c_theta[1][0] - c_theta[1][1]; u3 = c_theta[2][0] - c_theta[2][1];
      v1 = c_theta[0][3] - c_theta[0][1]; v2 = c_theta[1][3] - c_theta[1][1]; v3 = c_theta[2][3] - c_theta[2][1];
      n1 = -1.0*(u2*v3-u3*v2); n2 = -1.0*(u3*v1-u1*v3); n3 = -1.0*(u1*v2-u2*v1);
    }
    else if ( ((me[0]+me[3]+me[4])==10) && ((me[4]+me[5]+me[2])==10) ) { // B and C in aggregates
      isw = 2; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
      u1 = c_theta[0][1] - c_theta[0][0]; u2 = c_theta[1][1] - c_theta[1][0]; u3 = c_theta[2][1] - c_theta[2][0];
      v1 = c_theta[0][3] - c_theta[0][0]; v2 = c_theta[1][3] - c_theta[1][0]; v3 = c_theta[2][3] - c_theta[2][0];
      n1 = u2*v3-u3*v2; n2 = u3*v1-u1*v3; n3 = u1*v2-u2*v1;
    }
    else if ( ((me[0]+me[3]+me[4])==7) && ((me[4]+me[5]+me[2])==7) ) { // B and C in paste
      isw = 3; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
      u1 = c_theta[0][1] - c_theta[0][0]; u2 = c_theta[1][1] - c_theta[1][0]; u3 = c_theta[2][1] - c_theta[2][0];
      v1 = c_theta[0][3] - c_theta[0][0]; v2 = c_theta[1][3] - c_theta[1][0]; v3 = c_theta[2][3] - c_theta[2][0];
      n1 = -1.0*(u2*v3-u3*v2); n2 = -1.0*(u3*v1-u1*v3); n3 = -1.0*(u1*v2-u2*v1);
    }
    else if ( ((me[1]+me[3]+me[5])==10) && ((me[0]+me[3]+me[4])==10) ) { // B and D in aggregates
      isw = 4; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
      u1 = c_theta[0][0] - c_theta[0][2]; u2 = c_theta[1][0] - c_theta[1][2]; u3 = c_theta[2][0] - c_theta[2][2];
      v1 = c_theta[0][3] - c_theta[0][2]; v2 = c_theta[1][3] - c_theta[1][2]; v3 = c_theta[2][3] - c_theta[2][2];
      n1 = u2*v3-u3*v2; n2 = u3*v1-u1*v3; n3 = u1*v2-u2*v1;
    }
    else if ( ((me[1]+me[3]+me[5])==7) && ((me[0]+me[3]+me[4])==7) ) { // B and D in the paste
      isw = 5; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
      u1 = c_theta[0][0] - c_theta[0][2]; u2 = c_theta[1][0] - c_theta[1][2]; u3 = c_theta[2][0] - c_theta[2][2];
      v1 = c_theta[0][3] - c_theta[0][2]; v2 = c_theta[1][3] - c_theta[1][2]; v3 = c_theta[2][3] - c_theta[2][2];
      n1 = -1.0*(u2*v3-u3*v2); n2 = -1.0*(u3*v1-u1*v3); n3 = -1.0*(u1*v2-u2*v1);
    }
    else { std::cout << "WARNING : no sub case found to compute interface orientation."  << std::endl; }
    sv = get_sub_volume_2n( c_tet, c_theta, isw );
  } else {
    std::cout << "[ERROR] no case found to compute interface orientation (sum="+std::to_string( me[0]+me[1]+me[2]+me[3]+me[4]+me[5] )+")" << std::endl;
    exit(EXIT_FAILURE);
    std::cout << "         it can come from the threshold being equal to the field value " << std::endl;
  } // end if 17

  double norm = sqrt(pow(n1,2)+pow(n2,2)+pow(n3,2));
  std::vector<double> interface(4); // [V-, n1, n2, nz]
  interface[0] = sv;
  interface[1] = n1/norm;
  interface[2] = n2/norm;
  interface[3] = n3/norm;  
  return interface;
}

std::vector<std::vector<double> > tetrahedron::get_coor_theta_1n( std::vector<std::vector<double> > c_tet, std::vector<double> theta_edge, unsigned int isw) {
  std::vector<std::vector<double> > c_theta(3);
  if ( isw==0 ) { // node A is alone
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
  }
  if ( isw==1 ) { // node B is alone
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC       
  }
  if ( isw==2 ) { // node C is alone
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
  }
  if ( isw==3 ) { // node D is alone
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
  }
  return c_theta;
}

std::vector<std::vector<double> > tetrahedron::get_coor_theta_2n( std::vector<std::vector<double> > c_tet, std::vector<double> theta_edge, unsigned int isw) {
  std::vector<std::vector<double> > c_theta(3);
  if ( isw==0 || isw==1 ) { //AD, AC, BD and BC are cut
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC
  }
  if ( isw==2 || isw==3 ) { //AB, BD, DC and AC are cut
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
  }
  if ( isw==4 || isw==5 ) { // AD, DC, AB and BC are cut
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
    for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC
  }
  return c_theta;
}

double tetrahedron::get_volume_tet( std::vector<std::vector<double> > c_tet ) {
  double xa = c_tet[0][0]; double ya = c_tet[1][0]; double za = c_tet[2][0];
  double xb = c_tet[0][1]; double yb = c_tet[1][1]; double zb = c_tet[2][1];
  double xc = c_tet[0][2]; double yc = c_tet[1][2]; double zc = c_tet[2][2];
  double xd = c_tet[0][3]; double yd = c_tet[1][3]; double zd = c_tet[2][3];
  double ax = xd-xa; double bx = xd-xb; double cx = xd-xc;
  double ay = yd-ya; double by = yd-yb; double cy = yd-yc;
  double az = zd-za; double bz = zd-zb; double cz = zd-zc;
  double pvx = by*cz - bz*cy;
  double pvy = bz*cx - bx*cz;
  double pvz = bx*cy - by*cx;
  //std::cout << "volu: " << std::abs(ax*pvx+ay*pvy+az*pvz)/6.0 << std::endl;
  return std::abs(ax*pvx+ay*pvy+az*pvz)/6.0;
}

double tetrahedron::get_sub_volume_1n( std::vector<std::vector<double> > c_tet, std::vector<std::vector<double> > c_theta, unsigned int isw) {
  int s = 0;              // isw = 0 : A is isolated and B,D and C together -> shift of s=0
  if      (isw==1) s = 1; // isw = 1 : B is isolated and A,D and C together -> shift of s=1
  else if (isw==2) s = 2; // isw = 2 : C is isolated and A,D and B together -> shift of s=2
  else if (isw==3) s = 3; // isw = 3 : D is isolated and A,C and B together -> shift of s=3
  else if (isw>3) std::cout << "[tetrahedron::get_sub_volume] Error: unkown isolated case. isw = " << isw << std::endl;
  double xa = c_theta[0][0]; double ya = c_theta[1][0]; double za = c_theta[2][0];
  double xb = c_theta[0][1]; double yb = c_theta[1][1]; double zb = c_theta[2][1];
  double xc = c_theta[0][2]; double yc = c_theta[1][2]; double zc = c_theta[2][2];
  double xd =   c_tet[0][s]; double yd =   c_tet[1][s]; double zd =   c_tet[2][s];
  double ax = xd-xa; double bx = xd-xb; double cx = xd-xc;
  double ay = yd-ya; double by = yd-yb; double cy = yd-yc;
  double az = zd-za; double bz = zd-zb; double cz = zd-zc;
  double pvx = by*cz - bz*cy;
  double pvy = bz*cx - bx*cz;
  double pvz = bx*cy - by*cx;
  //  std::cout << "sv1n: " << std::abs(ax*pvx+ay*pvy+az*pvz)/6.0 << std::endl;
  return std::abs(ax*pvx+ay*pvy+az*pvz)/6.0;
}

double tetrahedron::get_sub_volume_2n( std::vector<std::vector<double> > c_tet, std::vector<std::vector<double> > c_theta, unsigned int isw) {
  // STEP 0 - Define all 6 vertices
  // is isw 0 || 1 : c_theta correspond to AD AC BD and BC that we are going to call edge 1 2 3 and 4
  // is isw 2 || 3 : c_theta correspond to AB BD DC and AC that we are going to call edge 1 2 3 and 4
  // is isw 4 || 5 : c_theta correspond to AD DC AB and BC that we are going to call edge 1 2 3 and 4
  unsigned int s1, s2;
  if ( (isw==0) || (isw==1) ) { s1=0; s2=1; } // vertice 1 and 2 of tetrahedron are A and B respectively
  if ( (isw==2) || (isw==3) ) { s1=1; s2=2; } // vertice 1 and 2 of tetrahedron are B and C respectively
  if ( (isw==4) || (isw==5) ) { s1=1; s2=3; } // vertice 1 and 2 of tetrahedron are B and D respectively
  double x1 = c_theta[0][0];  double y1 = c_theta[1][0];  double z1 = c_theta[2][0];  // point on edge 1
  double x2 = c_theta[0][1];  double y2 = c_theta[1][1];  double z2 = c_theta[2][1];  // point on edge 2
  double x3 = c_theta[0][2];  double y3 = c_theta[1][2];  double z3 = c_theta[2][2];  // point on edge 3
  double x4 = c_theta[0][3];  double y4 = c_theta[1][3];  double z4 = c_theta[2][3];  // point on edge 4
  double xa =   c_tet[0][s1]; double ya =   c_tet[1][s1]; double za =   c_tet[2][s1]; // vertice A of origin tetrahedron
  double xb =   c_tet[0][s2]; double yb =   c_tet[1][s2]; double zb =   c_tet[2][s2]; // vertice B of origin tetrahedron
  // STEP 1 - Define a "centroid"
  double xo = (x1+x2+x3+x4+xa+xb)/6.0;
  double yo = (y1+y2+y3+y4+ya+yb)/6.0;
  double zo = (z1+z2+z3+z4+za+zb)/6.0;
  // STEP 2 - compute volume of each 6 tetrahedrons
  std::vector<std::vector<double> > ctmp(3);
  for( unsigned int i=0; i<3; i++ ) { ctmp[i].resize(4); }
  // tetrehedron 1 : A13O
  ctmp[0][0] = xa; ctmp[1][0] = ya; ctmp[2][0] = za;
  ctmp[0][1] = x1; ctmp[1][1] = y1; ctmp[2][1] = z1;
  ctmp[0][2] = x3; ctmp[1][2] = y3; ctmp[2][2] = z3;
  ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
  double v1 = get_volume_tet( ctmp );
  // tetrehedron 2 : A3BO
  ctmp[0][0] = xa; ctmp[1][0] = ya; ctmp[2][0] = za;
  ctmp[0][1] = x3; ctmp[1][1] = y3; ctmp[2][1] = z1;
  ctmp[0][2] = xb; ctmp[1][2] = yb; ctmp[2][2] = z3;
  ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
  double v2 = get_volume_tet( ctmp );
  // tetrehedron 3 : 1A2O
  ctmp[0][0] = x1; ctmp[1][0] = y1; ctmp[2][0] = z1;
  ctmp[0][1] = xa; ctmp[1][1] = ya; ctmp[2][1] = za;
  ctmp[0][2] = x2; ctmp[1][2] = y2; ctmp[2][2] = z2;
  ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
  double v3 = get_volume_tet( ctmp );
  // tetrehedron 4 : 34BO
  ctmp[0][0] = x3; ctmp[1][0] = y3; ctmp[2][0] = z3;
  ctmp[0][1] = x4; ctmp[1][1] = y4; ctmp[2][1] = z4;
  ctmp[0][2] = xb; ctmp[1][2] = yb; ctmp[2][2] = zb;
  ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
  double v4 = get_volume_tet( ctmp );
  // tetrehedron 5 : AB2O
  ctmp[0][0] = xa; ctmp[1][0] = ya; ctmp[2][0] = za;
  ctmp[0][1] = xb; ctmp[1][1] = yb; ctmp[2][1] = zb;
  ctmp[0][2] = x2; ctmp[1][2] = y2; ctmp[2][2] = z2;
  ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
  double v5 = get_volume_tet( ctmp );
  // tetrehedron 6 : B42O
  ctmp[0][0] = xb; ctmp[1][0] = yb; ctmp[2][0] = zb;
  ctmp[0][1] = x4; ctmp[1][1] = y4; ctmp[2][1] = z4;
  ctmp[0][2] = x2; ctmp[1][2] = y2; ctmp[2][2] = z2;
  ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
  double v6 = get_volume_tet( ctmp );  
  // std::cout << "[DEBUG] x1: " << "[" << x1 << " " << y1 << " " << z1 << "]"  << std::endl;
  // std::cout << "[DEBUG] x2: " << "[" << x2 << " " << y2 << " " << z2 << "]"  << std::endl;
  // std::cout << "[DEBUG] x3: " << "[" << x3 << " " << y3 << " " << z3 << "]"  << std::endl;
  // std::cout << "[DEBUG] x4: " << "[" << x4 << " " << y4 << " " << z4 << "]"  << std::endl;
  // std::cout << "[DEBUG] xa: " << "[" << xa << " " << ya << " " << za << "]"  << std::endl;
  // std::cout << "[DEBUG] xb: " << "[" << xb << " " << yb << " " << zb << "]"  << std::endl;
  // std::cout << "[DEBUG] xo: " << "[" << xo << " " << yo << " " << zo << "]"  << std::endl;  
  // std::cout << "[DEBUG] v1  = " << v1 << std::endl;
  // std::cout << "[DEBUG] v2  = " << v2 << std::endl;
  // std::cout << "[DEBUG] v3  = " << v3 << std::endl;
  // std::cout << "[DEBUG] v4  = " << v4 << std::endl;
  // std::cout << "[DEBUG] v5  = " << v5 << std::endl;
  // std::cout << "[DEBUG] v6  = " << v6 << std::endl;
  // std::cout << "[DEBUG] sum = " << v1+v2+v3+v4+v5+v6 << std::endl; 
  // STEP 3 - return the sub volume
  // std::cout << "sv2n: " << v1+v2+v3+v4+v5+v6 << std::endl;
  return v1+v2+v3+v4+v5+v6;
}
