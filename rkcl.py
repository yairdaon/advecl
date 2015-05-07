import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import pyopencl as cl
import pyopencl.tools as cl_tools
import pyopencl.array as cl_array

# the range of xs and ys
xStart = 0.0
yStart = 0.0
xEnd   = 1.5
yEnd   = 1.0
levels = [ 0.15 , 0.3 , 0.45, 0.5 , 0.75]

# mesh sizes
hx = 0.01
hy = 0.01

# times
ht= 0.001 # time step
final = 7.5
nt   = final/ht

# mean and variance of initial data
mu  = (0.5 , 0.5)
sig = 0.01;

# center locations
xCenters = np.arange(xStart +hx/2, xEnd + hx/2 , hx)
yCenters = np.arange(yStart +hy/2, yEnd + hy/2 , hy)

nxCenters  = len(xCenters)

nyCenters  = len(yCenters)

# get grids
X ,Y = np.meshgrid( xCenters, yCenters )

# define the initial distribution of T
T = np.exp( - (  (X - mu[0])**2 + ( Y -mu[1])**2 )/(2*sig) )
T = T.astype(np.float32) # cast to float32 so it works with kernel



########################### OpenCl ###########################

# setup stuff
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

# get kernel string
prg_file = open('pycl/fwd_euler_knl.c' , 'r')
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
    plt.title('Euler steps using OpenCl, time = ' +str(i*ht) )
    fig.savefig('frames/euler/T' + str(i*ht) + '.png')
    plt.close(fig)
