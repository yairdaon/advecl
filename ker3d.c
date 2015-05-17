/*
#ifdef cl_khr_fp64
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#else defined(cl_amd_fp64)
    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
#endif
*/
// HX,HY are (x,y) spatial mesh distances.
// HT is the length of the time step we take.
// They are added to the kenrel as #define HX ... when python creates the
// modified kernel.
// We use the inline flag so that the compiler can optimize memory access.


// From python:
//U   = PIB * psi * np.cos( Y * PIB ) * (   P * np.exp(A*X)  +      (1-P) * np.exp(B*X) -1  )/D;
//V   =     - psi * np.sin( Y * PIB ) * ( A*P * np.exp(A*X)  +  B * (1-P) * np.exp(B*X)     )/D; 
  

inline float u( float xCol ,float yRow,  float zDep ){ 
  float x = (xCol+0.5)*HX;
  float y = (yRow+0.5)*HY;
  float z = (zDep+0.5)*HZ;
  if ( x <= 0 || x >= HX*XCOLS    || y <= 0 || y >= HY*YROWS || z <= 0 || z >= HZ*ZDEPT ) {
    return 0.0f;
  } else {
    return PIB* PSI * cos ( y * PIB ) * ( PP*exp(A*x) + (1-PP)*exp(B*x) -1.0f )/D; // todo??
  }
}

inline float v( float xCol ,float yRow, float zDep ){ 
  float x = (xCol+0.5)*HX;
  float y = (yRow+0.5)*HY;
  float z = (zDep+0.5)*HZ;
  if ( x <= 0 || x >= HX*XCOLS    || y <= 0 || y >= HY*YROWS || z <= 0 || z >= HZ*ZDEPT ) {
    return 0.0f;
  } else {
    return -PSI * sin( y * PIB) * ( A*PP*exp(A*x) + B*(1.0f-PP) * exp(B*x) )/D;  // todo??
  }
}
inline float w( float xCol ,float yRow, float zDep ){ 
  float x = (xCol+0.5)*HX;
  float y = (yRow+0.5)*HY;
  float z = (zDep+0.5)*HZ;
  if ( x <= 0 || x >= HX*XCOLS    || y <= 0 || y >= HY*YROWS || z <= 0 || z >= HZ*ZDEPT ) {
    return 0.0f;
  } else {
    return 1.0f;//-PSI * sin( y * PIB) * ( A*PP*exp(A*z) + B*(1.0f-PP) * exp(B*z) )/D; // DEF TODO
  }
}

inline float T(__global float *array, long xCol , long yRow, long zDep) { 
  if ( xCol < 0 || xCol > XCOLS-1 || yRow < 0 || yRow > YROWS-1 || zDep < 0 || zDep > ZDEPT-1) {
    return 0.0f;
  } else {  
    return array[ yRow*XCOLS*ZDEPT + xCol*ZDEPT + zDep ];
  }
}


/* A kernel to perform one RK step in a 2D finite element method.
   We calculate f, so that the ODE satisfied is T'(t) = f(t).
   T is the concentration of the tracer in *the middle of the elemnts*.
   (consequently, if we'd like to calculate it on the boundary, we need to 
   average two neighbouring cells).
   u and v are flows in the (x,y) directions (respectively).

   Space discretization: the bottom left cell is (0,0). 

   variables:
   Tin = Input  array of tracer concentration.
   Tout= Output array of tracer concentration.
*/
kernel void rk_step( __global float* Tin,
		     __global float* Tout) {
  
  // get location
  long xCol = get_global_id(0);  
  long yRow = get_global_id(1);  
  long zDep = get_global_id(2);  

  if ( xCol < XCOLS && yRow < YROWS && zDep < ZDEPT) {

    // Here we inline the Mathematica string. This is the actual time step calculation.
    float res = SPLIT;
  
    Tout[yRow*XCOLS*ZDEPT + xCol*ZDEPT + zDep ] = res; // TODO [i * height * depth + j * depth + k ]
  }
}
