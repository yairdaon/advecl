import numpy as np
import math
import time
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os
import sys

import pyopencl as cl
import pyopencl.tools as cl_tools
import pyopencl.array as cl_array

import getstring
from constants import *

def test_speed(file_name , ctx_str):
    

    os.environ["PYOPENCL_CTX"] = ctx_str
    
    with open(file_name, "w") as myfile:
        myfile.write("RK order , space step , number of time steps , number of points, total time\n")

    # setup stuff
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
        

    
   
        
       

    for h in hs: 
        for order in orders:

            # meshes sizes
            hx = h
            hy = h
            hz = h
        
            # center locations
            xCenters   = np.arange( hx/2,  a + hx/2 , hx) 
            nxCenters  = len(xCenters)
            yCenters   = np.arange( hy/2,  b + hy/2 , hy) 
            nyCenters  = len(yCenters)
            zCenters   = np.arange( hy/2,  c + hy/2 , hy) 
            nzCenters  = len(zCenters)

            
# grids, to get the CFL
        #X, Y , Z= np.meshgrid(xCenters , yCenters , zCenters)
        #U  = PIB * psi * np.cos( Y * PIB ) * (   P * np.exp(A*X)  +      (1-P) * np.exp(B*X) -1  )/D;
        #V  =     - psi * np.sin( Y * PIB ) * ( A*P * np.exp(A*X)  +  B * (1-P) * np.exp(B*X)     )/D; 
        #W  = np.ones(U.shape)
            cfl = 3 #np.max(np.abs(U)) +  np.max(np.abs(V)) + 1

            # time step
            ht    = hx/(factor*cfl)  

# define the initial distribution of T
#T = np.exp( - (  
#        ((X-mu[0])/sig[0])**2 +
#        ((Y-mu[1])/sig[1])**2 +
#        ((Z-mu[2])/sig[2])**2 
#        )/2.0
#              )
            T = np.ones( (nyCenters, nxCenters ,nzCenters), dtype = np.float32) # T.astype(np.float32) # cast to float32 so it works with kernel
            
            # Do string manipulations under the hood
            prg_str = getstring.get3d(order , hx, hy, hz, ht, nxCenters, nyCenters, nzCenters)
        
            # compile
            prg = cl.Program(ctx, prg_str).build()

            # create memory pools       
            in_pool    = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
            Tin_d      = cl_array.arange(queue, nxCenters*nyCenters*nzCenters, dtype=np.float32, allocator=in_pool)    
            out_pool   = cl_tools.MemoryPool(cl_tools.ImmediateAllocator(queue))
            Tout_d     = cl_array.arange(queue, nxCenters*nyCenters*nzCenters, dtype=np.float32, allocator=out_pool)

            # start the timing:
            start = time.clock()

            # do time stepping and plotting.
            for i  in range(nSpeed):
            
                # Copy T into Tin_d
                Tin_d.set( T.ravel(), queue=queue )   
            
                # Apply the kernel here
                prg.rk_step(queue, T.shape, None, 
                        Tin_d.data, Tout_d.data)
    
                # Copy data into T
                Tout_d.get(queue=queue , ary=T)
        
            # End timing for this round
            end = time.clock()

            # RK order , space step , number of time steps , number of points, total time\n")
            data = str(order) + " , " + str(h) +  " , " + str(nSpeed) + " , " + str(T.shape[0]*T.shape[1]*T.shape[2]) + " , " + str(end-start)  + "\n"
            with open(file_name, "a") as myfile:
                myfile.write(data)


test_speed(sys.argv[1] , sys.argv[2])
