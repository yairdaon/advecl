// Convolution kernel from Heterogeneous Computing with OpenCL
// by Gaster, Howes, Kaeli, Mistry, and Schaa

kernel void forward_euler_step(
			       global float* Tin,
			       global float* Tout,
			       global int* dims,
			       global float* steps)
//constant float* filter,
//int filterWidth, == 3 
//local float* localT,
//int localHeight,== 32
//int localWidth, == 32
{

  // first: unpack:
  // dimensions...
  local int rows = dims[0];
  local int cols = dims[1];
  local int localHeight = dims[2];
  local int localWidth  = dims[3];
  
  // ... time steps
  local float hx = steps[0];
  local float hy = steps[1];
  local float ht = steps[2];
  
  local float uTop    =  -0.0/(2.0*hx);
  local float uBot    =   0.0/(2.0*hx);
  local float vLeft   =  -1.0/(2.0*hy);
  local float vRight  =   1.0/(2.0*hy);
  local float middle  =   uTop + uBot + vLeft + vRight;
  
  // Define the input we're missing
  local float filetr[9] = { 0.0     , uTop    , 0.0     ,
			    vLeft   , middle  , vRight  ,
			    0.0     , uBot    , 0.0     };
  int filterWidth = 3;

  // Determine the amount of padding for this filter
  int filterRadius = 1; //filterWidth/2;
  int padding = filterRadius * 2;
  
  // Determine where each workgroup begins reading
  int groupStartCol = get_group_id(0)*get_local_size(0);
  int groupStartRow = get_group_id(1)*get_local_size(1);
  
  // Determine the local ID of each work-item
  int localCol = get_local_id(0);
  int localRow = get_local_id(1);
  
  // Determine the global ID of each work-item. Work-items
  // representing the output region will have a unique global ID
  int globalCol = groupStartCol + localCol;
  int globalRow = groupStartRow + localRow;
#if 0
  if(globalRow < rows && globalCol < cols)
    TOut[globalRow*cols + globalCol] = Tin[globalRow*cols + globalCol];
#endif
  
  // Cache the data to local memory
  // Step down rows
  for(int i = localRow; i < localHeight; i += get_local_size(1)) {
    int curRow = groupStartRow+i;
    
    // Step across columns
    for(int j = localCol; j < localWidth; j += get_local_size(0)) {
      int curCol = groupStartCol+j;
      
      // Perform the read if it is in bounds
      if(curRow < rows && curCol < cols) {
	localT[i*localWidth + j] = Tin[curRow*cols+curCol];
      }
    }
  }
  barrier(CLK_LOCAL_MEM_FENCE);
  
  // Perform the convolution
  if(globalRow < rows-padding && globalCol < cols-padding) {
    
    // Each work item will filter around its start location
    //(starting from the filter radius left and up)
    float sum = 0.0f;
    int filterIdx = 0;
    
    // Not unrolled
    for(int i = localRow; i < localRow+filterWidth; i++) {
     
      int offset = i*localWidth;
      for(int j = localCol; j < localCol+filterWidth; j++){
	sum += localT[offset+j] * filter[filterIdx++];
      }
    }
    /*
    // Inner loop unrolled
    for(int i = localRow; i < localRow+filterWidth; i++) {
    int offset = i*localWidth+localCol;
    sum += localT[offset++] * filter[filterIdx++];
    sum += localT[offset++] * filter[filterIdx++];
    sum += localT[offset++] * filter[filterIdx++];
    sum += localT[offset++] * filter[filterIdx++];
    sum += localT[offset++] * filter[filterIdx++];
    sum += localT[offset++] * filter[filterIdx++];
    sum += localT[offset++] * filter[filterIdx++];
    }
    */

    // Write the data out
    Tout[(globalRow+filterRadius)*cols + (globalCol+filterRadius)] = 
      Tin[(globalRow+filterRadius)*cols + (globalCol+filterRadius)] - sum*ht;
  }
  return;
}
