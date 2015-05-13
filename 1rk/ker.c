/* A kernel to perform one euler step in a 1D finite element method.
   We calculate f, so that the ODE satisfied is T'(t) = f(t).
   T is the concentration of the tracer in *the middle of the elemnts*.
   (consequently, if we'd like to calculate it on the boundary, we need to 
   average two neighbouring cells).
   u and v are flows in the (x,y) directions (respectively).

   Space discretization: the bottom left cell is (0,0). 

   variables:
   Tin = Input array of tracer concentration
   Tout= Output array of tracer concentrations.
   hx,hy are (x,y) spatial mesh distances.
   ht is the length of the time step we take.
   
*/

#define TWOPI 6.28318530718f
#define PI    3.14159265359f


inline float u( float i ){ 
  return 1.0f;
}

// We use the inline flag so that the compiler can optimize memory access.
inline float T(const global float *array, int i) { 
  return array[i];
}

kernel void euler1D( const global float* Tin,
		     global float* Tout)
{
  // get location
  int i = get_global_id(0);  

  // get the dimensions
  int n = get_global_size(0); 

  // Here we inline the Mathematica string
  float f = //SPLIT;
 
  // set the final value - perform the actual euler step
  Tout[i] = f; 
  return;
 
}
