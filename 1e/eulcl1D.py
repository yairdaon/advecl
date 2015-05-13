import numpy as np

import pyopencl as cl
import pyopencl.tools as cl_tools
import pyopencl.array as cl_array

# contour plot levels
#levels = np.arange(0.1,1.0,0.05)

# mean and variance of initial data
mu  = (0.4)
sig = (0.15);

# meshes sizes
hx = 0.01

# times
ht    = 0.001     # time step
final = 0.1       # final time
nt    = final/ht  # number of time steps
np.save("data/times.npy" ,np.array([ht,final]))

# center locations
xCenters = np.arange( hx/2, 1.0 + hx/2 , hx) # from 0 to 1 - don't change!!!
nxCenters  = len(xCenters)
np.save("data/xCenters.npy" ,xCenters)


# define the initial distribution of T
T = np.exp( - (  
        ( (  xCenters - mu  )/sig) **2 
        )/2.0
              )
T = T +0.1
T = T.astype(np.float32) # cast to float32 so it works with kernel



########################### OpenCl ###########################

# setup stuff
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

# get and modify kernel string
prg_file = open('ker.c' , 'r')
prg_str = prg_file.read()
hx_str = "#define HX " + str(hx) + "f\n"
ht_str = "#define HT " + str(ht) + "f\n"
N_str  = "#define N "  + str(nxCenters)
prg_str  = hx_str +  ht_str + N_str + prg_str
parts = prg_str.split("SPLIT")

# get the Mathmatica expression
op_file = open('str1d.txt' ,'r')
op_str  = op_file.read()
prg_str = "\n\n\n" + parts[0] +  op_str + parts[1] + "\n\n\n"
print prg_str 
op_file.close()
prg_file.close()

 
# compile
prg = cl.Program(ctx, prg_str).build()

# create memory pools
in_pool    = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
Tin_d      = cl_array.arange(queue, nxCenters , dtype=np.float32, allocator=in_pool)

out_pool   = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
Tout_d     = cl_array.arange(queue, nxCenters, dtype=np.float32, allocator=out_pool)


# do time stepping.
for i  in range(0,int(nt)):
    
    # Write T into disk
    np.save("data/array" + str(i) ,T)

    Tin_d.set( T )
    
    # apply the kernel here!
    prg.euler1D(queue, T.shape, None, 
                           Tin_d.data, Tout_d.data)# array inputs
    # copy data into T
    Tout_d.get(queue=queue , ary=T)

    
