


#define PP 0.172537688699f
#define PSI 25464.7908947f
#define A 1.56879760003e-06f
#define B -1.57279760003e-06f
#define PIB 1.57079632679e-06f
#define D 8600
#define N  100
#define M  200
#define HX 10000
#define HY 10000
#define HT 48132761.9126f
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
  //U  = PIB * psi * np.cos( Y * PIB ) * (   P * np.exp(A*X)  +      (1-P) * np.exp(B*X) -1  )/D;
  //V  =     - psi * np.sin( Y * PIB ) * ( A*P * np.exp(A*X)  +  B * (1-P) * np.exp(B*X)     )/D; 

inline float u( long i ,long j ){ 
  if ( i < 1 || i > M-1 || j < 1 || j > N-1 ) {
    return 0.0f;
  } else {
    //return 1.0;
    return PIB* PSI * cos ( i * HY * PIB ) * ( PP*exp(A*j*HX) + (1-PP)*exp(B*j*HX) -1.0f )/D;
    //return sin( 2*i*HY*PIB ) * cos( j*TWOPI*HX/A );
  }
}
inline float v( long i ,long j ){ 
  if ( i < 1 || i > M-1 || j < 1 || j > N-1 ) {
    return 0.0f;
  } else {
    //return 1.0;
    return -PSI * sin( i * HY * PIB) * ( A*PP*exp(A*j*HX) + B*(1.0f-PP) * exp(B*j*HX) )/D; 
    //return cos( i*TWOPI*HX ) * sin( j*TWOPI*HY );
  }
}
inline float T(const global float *array, long i , long j) { 
  if ( i < 0 || i > M-1 || j < 0 || j > N-1 ) {
    return 0.0f;
  } else {  
    return array[i*N + j];
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
kernel void rk_step( const global float* Tin,
		     global float* Tout) {
  
  // get location
  long i = get_global_id(0);  
  long j = get_global_id(1);  

  if ( i < M && j < N) {

    // Here we inline the Mathematica string. This is the actual Euler step calculation.
    float res = T(Tin,i,j) + HT*(-(-((T(Tin,-1 + i,j) + T(Tin,i,j))*u(i,j)) + (T(Tin,i,j) + T(Tin,1 + i,j))*u(1 + i,j))/(2.f*HX) - (-((T(Tin,i,-1 + j) + T(Tin,i,j))*v(i,j)) + (T(Tin,i,j) + T(Tin,i,1 + j))*v(i,1 + j))/(2.f*HY));
  
    Tout[i*N + j] = res;
  }
}



