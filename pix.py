import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os
import sys

import pyopencl as cl
import pyopencl.tools as cl_tools
import pyopencl.array as cl_array

from constants import *
import getstring

def make_pix(rk_ord , set_up, target, h, final):
    
    os.environ["PYOPENCL_CTX"] = set_up
    
    # RK order 1 = Euler
    order = int(rk_ord)
     
    # meshes sizes
    hx = float(h)
    hy = float(h)

    # center locations
    xCenters   = np.arange( hx/2,  a + hx/2 , hx) 
    nxCenters  = len(xCenters)
    yCenters   = np.arange( hy/2,  b + hy/2 , hy) 
    nyCenters  = len(yCenters)

    # grids
    X, Y = np.meshgrid(xCenters , yCenters )
    U  = PIB * psi * np.cos( Y * PIB ) * (   P * np.exp(A*X)  +      (1-P) * np.exp(B*X) -1  )/D;
    V  =     - psi * np.sin( Y * PIB ) * ( A*P * np.exp(A*X)  +  B * (1-P) * np.exp(B*X)     )/D; 
    cfl = np.max(np.abs(U)) +  np.max(np.abs(V))

    # times
    ht    = hx/(factor*cfl)   # time step
    nt    = int(int(final)/ht)    # number of time steps

    # define the initial distribution of T
    T = np.exp( - (  
            ((X-mu[0])/sig[0])**4 +
            ((Y-mu[1])/sig[1])**4 
            )/2.0
              )
    T = T.astype(np.float32) # cast to float32 so it works with kernel

    # setup stuff
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    # Get the kernel from a string
    prg_str = getstring.get(order , hx, hy, ht, nxCenters, nyCenters)

    # compile
    prg = cl.Program(ctx, prg_str).build()

    # create memory pools
    in_pool    = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
    Tin_d      = cl_array.arange(queue, nxCenters*nyCenters, dtype=np.float32, allocator=in_pool)
    out_pool   = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
    Tout_d     = cl_array.arange(queue, nxCenters*nyCenters, dtype=np.float32, allocator=out_pool)


    # do time stepping and plotting.
    for i  in range(nt):
    
        # plot, not very interesting
        fig = plt.figure()
        CS = plt.contour(X, Y, T, levels=levels)
        plt.clabel(CS)
        plt.title("Tracer concentration. Spatial FEM and RK" + str(order) +" Time Steps.\n Step "
                  +str(i) + ",T = " + str(i*ht)+ " weeks.")
        if hasattr(plt, "streamplot"):
            plt.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=plt.cm.autumn)
        fig.savefig(target + '/frame' + str(i) + '.png')
        plt.close(fig)    
            
        # Copy T into Tin_d
        Tin_d.set( T.ravel(), queue=queue )   

        # Apply the kernel here
        prg.rk_step(queue, T.shape, None, 
                    Tin_d.data, Tout_d.data)
    
        # Copy data into T
        Tout_d.get(queue=queue , ary=T)
            
make_pix(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
