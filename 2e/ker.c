#define TWOPI 6.28318530718f
#define PI    3.14159265359f

// HX,HY are (x,y) spatial mesh distances.
// HT is the length of the time step we take.
// They are added to the kenrel as #define HX ... when python creates the
// modified kernel.
// We use the inline flag so that the compiler can optimize memory access.

inline float u( float i ,float j ){ 
  return sin( i*TWOPI*HX ) * cos( j*TWOPI*HY );
}
inline float v( float i ,float j ){ 
  return cos( i*TWOPI*HX ) * sin( j*TWOPI*HY );
}
inline float T(const global float *array, long i , long j) { 
  return array[(i%N)*N + (j%N)];
}
/* A kernel to perform one euler step in a 2D finite element method.
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
kernel void euler2D( const global float* Tin,
		     global float* Tout)
{
  
  // get location
  long i = get_global_id(0);  
  long j = get_global_id(1);  

  if ( i < N && j < N) {

    // Here we inline the Mathematica string. This is the actual Euler step calculation.
    float res = SPLIT;
  
    Tout[i*N + j] = res;
  }
    barrier(CLK_GLOBAL_MEM_FENCE);
    //return;
}
