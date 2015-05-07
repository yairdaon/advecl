import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os

import pyopencl as cl
import pyopencl.tools as cl_tools
import pyopencl.array as cl_array

# contour plot levels
levels = np.arange(0.1,1.0,0.05)

# mean and variance of initial data
mu  = (0.4 , 0.6)
sig = (0.15, 0.07);

# meshes sizes
hx = 0.01
hy = 0.01

# times
ht    = 0.001     # time step
final = 0.5       # final time
nt    = final/ht  # number of time steps

# center locations
xCenters = np.arange( hx/2, 1.0 + hx/2 , hx) # from 0 to 1 - don't change!!!
yCenters = np.arange( hy/2, 1.0 + hy/2 , hy) # from 0 to 1 - don't change!!!
nxCenters  = len(xCenters)
nyCenters  = len(yCenters)

# get grids
X ,Y = np.meshgrid( xCenters, yCenters )

# define the initial distribution of T
T = np.exp( - (  
        ( (  X-mu[0]  )/sig[0]) **2      +
        ( (  Y-mu[1]  )/sig[1]) **2 
        )/2.0
              )
T = T.astype(np.float32) # cast to float32 so it works with kernel



########################### OpenCl ###########################

# setup stuff
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

# get kernel string
prg_file = open('fwd_euler_knl.c' , 'r')
prg_str  = prg_file.read()
prg_file.close()

 
# compile
prg = cl.Program(ctx, prg_str).build()

# create memory pools
in_pool    = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
Tin_d      = cl_array.arange(queue, nyCenters*nxCenters, dtype=np.float32, allocator=in_pool)

out_pool   = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
Tout_d     = cl_array.arange(queue, nyCenters*nxCenters, dtype=np.float32, allocator=out_pool)


# do time stepping.
for i  in range(0,int(nt)):
        
    Tin_d.set( T )
    # apply the kernel here!
    prg.forward_euler_step(queue, T.shape, None, 
                           Tin_d.data, Tout_d.data, # array inputs
                           np.float32(hx), np.float32(hy), np.float32(ht) ) # float inputs
    # copy data into T
    Tout_d.get(queue=queue , ary=T)

    # plot, not very interesting
    fig = plt.figure()
    CS = plt.contour(X, Y, T, levels)
    plt.clabel(CS, inline=1, fontsize=10)
    t_str = format(i*ht, "1.3f")
    plt.title('Tracer in Taylor vortex. Spatial FEM and Fwd Euler Time Steps. \n Time = ' + t_str)
    fig.savefig('frames/euler/frame' + str(i) + '.png')
    plt.close(fig)


res = os.system("ffmpeg -i frames/euler/frame%d.png euler.mpg")
if (res != 0):
    print "Your machine does not have ffmpeg, so there is no movie."
