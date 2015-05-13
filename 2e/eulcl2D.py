import numpy as np
import math

import pyopencl as cl
import pyopencl.tools as cl_tools
import pyopencl.array as cl_array

# Flow parameters
alpha = 1.5
a     = 1.5
A     = -alpha/2.0 + math.sqrt( (alpha/2)**2 + (math.pi)**2 )
B     = -alpha/2.0 - math.sqrt( (alpha/2)**2 + (math.pi)**2 )
psi   = 1.0
P     = (1-math.exp(B*a))/(math.exp(A*a)-math.exp(B*a))
cfl   = psi * 2*P * math.exp(A) * math.exp(B) * A * B * 2
print cfl
# mean and variance of initial data
mu  = (.5,.5)
sig = (.1,.1);

# meshes sizes
hx = 0.01
hy = 0.01

# times
ht    = 0.005    # time step
final = 15       # final time
nt    = final/ht  # number of time steps
np.save("data/times.npy" ,np.array([ht,final]))

# center locations
xCenters   = np.arange( hx/2, 1.0 + hx/2 , hx) # from 0 to 1 - don't change!!!
nxCenters  = len(xCenters)
yCenters   = np.arange( hy/2, 1.0 + hy/2 , hy) # from 0 to 1 - don't change!!!
nyCenters  = len(yCenters)

# grids
X, Y = np.meshgrid(xCenters , yCenters )
np.save("data/X.npy" ,X) # save, so we use it in the movie...
np.save("data/Y.npy", Y)

# define the initial distribution of T
T = np.exp( - (  
        ((X-mu[0])/sig[0])**2 +
        ((Y-mu[1])/sig[1])**2 
        )/2.0
              )
T = T.astype(np.float32) # cast to float32 so it works with kernel
#T = np.ravel( T )


########################### OpenCl ###########################

# setup stuff
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

# get and modify kernel string
prg_file = open('ker.c' , 'r')
prg_str = prg_file.read()
hx_str = "#define HX " + str(hx) + "f\n"
hy_str = "#define HY " + str(hy) + "f\n"
ht_str = "#define HT " + str(ht) + "f\n"
N_str  = "#define N  " + str(nxCenters)  + "\n"
PP_str = "#define PP " + str(P)  + "f\n" 
PSI_str= "#define PSI "+ str(psi)+ "f\n" 
A_str  = "#define A "  + str(A)  + "f\n" 
B_str  = "#define B "  + str(B)  + "f\n" 
#PIB_str= "#define PIB "+ str(PIB)+ "f\n"

# now we cut and paste and mess with the kernel
prg_str  = N_str  + hx_str  + hy_str  + ht_str + prg_str # Add constatns...
prg_str  =  PP_str  + PSI_str + A_str  + B_str  + prg_str # ...and more constants 
parts = prg_str.split("SPLIT") # Split were we put the Mathematica expression
op_file = open('str2d.txt' ,'r') # open Mathmatica txt file
op_str  = op_file.read() # Read the Mathematica expression
prg_str = "\n\n\n" + parts[0] +  op_str + parts[1] + "\n\n\n" #put the expression where it belongs
print prg_str  # print it, so we see the new kernel
op_file.close() # Close file
prg_file.close()# Close file
 
# compile
prg = cl.Program(ctx, prg_str).build()

# create memory pools
mf = cl.mem_flags
in_pool    = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))#,
                                                             #mem_flags=mf.READ_ONLY))
Tin_d      = cl_array.arange(queue, nxCenters*nyCenters, dtype=np.float32, allocator=in_pool)

out_pool   = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))#,
                                                             #mem_flags=mf.WRITE_ONLY))
Tout_d     = cl_array.arange(queue, nxCenters*nyCenters, dtype=np.float32, allocator=out_pool)


# do time stepping and plotting.
for i  in range(int(nt)):
    
    # Write T into disk
    np.save("data/array" + str(i) ,T)

    # Copy T into Tin_d
    Tin_d.set( T.ravel(), queue=queue )   

    # apply the kernel here!
    prg.euler2D(queue, T.shape, None, 
                Tin_d.data, Tout_d.data)
    
    # copy data into T
    Tout_d.get(queue=queue , ary=T)

