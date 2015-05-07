/* A kernel to perform one euler step in a 2D finite element method.
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
kernel void forward_euler_step(
			       const global float* Tin,
			       global float* Tout,
			       const float hx,
			       const float hy,
			       const float ht)
{
  // get location
  int i = get_global_id(0);  // row
  int j = get_global_id(1);  // columns

  // get the dimensions
  int nRows = get_global_size(0); // number of rows
  int nCols = get_global_size(1); // number of columns 

  // get indices
  uint itop      = (i+1) % nRows; // the row above (wrapped) 
  uint ibottom   = (i-1) % nRows; // the row below (wrapped)
  uint jleft     = (j-1) % nCols; // the column on the left 
  uint jright    = (j+1) % nCols; // the column on the right  



  // location of middle of cell
  float midx = i*hx*TWOPI;
  float midy = j*hy*TWOPI;

  float topy = midy + hy*PI; // y at top    boundary of cell
  float boty = midy - hy*PI; // y at bottom boundary of cell
  float lefx = midx - hx*PI; // x at left   boundary of cell
  float rigx = midx + hx*PI; // x at right  boundary of cell



  float uTop     =  sin( midx )  *  cos( topy );
  float uBottom  =  sin( midx )  *  cos( boty );
  float vLeft    =  cos( lefx )  *  sin( midy );
  float vRight   =  cos( rigx )  *  sin( midy );
  
  // Read the current  values just once.
  float mid      = Tin[i*nCols + j];
  float top      = Tin[itop*nCols    +  j      ]    ;//(i-1) % nRows; 
  float bottom   = Tin[ibottom*nCols +  j      ]    ;//(i+1) % nRows;
  float left     = Tin[i      *nCols +  jleft  ]    ;//(j-1) % nCols;
  float right    = Tin[i      *nCols +  jright ]    ;//(j+1) % nCols; 
  

  // Calculate the value at the middle
  float f = -(
	      uTop    * (top    + mid) / (2.0f*hx) -
	      uBottom * (bottom + mid) / (2.0f*hx) +
	      vRight  * (right  + mid) / (2.0f*hy) -
	      vLeft   * (left   + mid) / (2.0f*hy)
	      );
	
  // set the final value - perform the actual euler step
  Tout[i*nCols + j] = mid + f*ht; 
  return;
 
}
