import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os

import pyopencl as cl
import pyopencl.tools as cl_tools
import pyopencl.array as cl_array

# contour plot levels
levels = np.arange(0.01,1.51,0.25)

# Flow parameters
a     = 1e6 # north to west - Y axis
b     = 2e6 # west  to east - X axis
tau   = 0.1
rho   = 1000
beta  = 1e-11
C_d   = 0.0025
alpha = beta/C_d
A     = -alpha/2.0 + math.sqrt( (alpha/2)**2 + (math.pi/b)**2 )
B     = -alpha/2.0 - math.sqrt( (alpha/2)**2 + (math.pi/b)**2 )
psi   = (tau * b) / (rho * C_d * math.pi )
P     = (1-math.exp(B*a))/(math.exp(A*a)-math.exp(B*a))
PIB   = math.pi/b
D     = 8600


# mean and variance of initial data
mu  = (0.3  *a ,0.6 *a)
sig = ( .05 *a , .015 *a) 

# meshes sizes
hx = 10000
hy = 10000

# center locations
xCenters   = np.arange( hx/2,  a + hx/2 , hx) 
nxCenters  = len(xCenters)
yCenters   = np.arange( hy/2,  b + hy/2 , hy) 
nyCenters  = len(yCenters)

# grids
X, Y = np.meshgrid(xCenters , yCenters )
#np.save("data/X.npy" ,X) # save, so we use it in the movie...
#np.save("data/Y.npy", Y)
U  = PIB * psi * np.cos( Y * PIB ) * (   P * np.exp(A*X)  +      (1-P) * np.exp(B*X) -1  )/D;
V  =     - psi * np.sin( Y * PIB ) * ( A*P * np.exp(A*X)  +  B * (1-P) * np.exp(B*X)     )/D; 
cfl = np.max(np.abs(U)) +  np.max(np.abs(V))

# times
ht    = hx/(50.0*cfl)   # time step
nt    = 10000    # number of time steps
final = nt*ht # final time
np.save("data/times.npy" ,np.array([ht,final]))

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
hx_str = "#define HX " + str(hx) + "\n"
hy_str = "#define HY " + str(hy) + "\n"
ht_str = "#define HT " + str(ht) + "f\n"
N_str  = "#define N  " + str(nxCenters)  + "\n"
M_str  = "#define M  " + str(nyCenters)  + "\n"
PP_str = "#define PP " + str(P)  + "f\n" 
PSI_str= "#define PSI "+ str(psi)+ "f\n" 
A_str  = "#define A "  + str(A)  + "f\n" 
B_str  = "#define B "  + str(B)  + "f\n" 
PIB_str= "#define PIB "+ str(PIB)+ "f\n"
D_str  = "#define D "  + str(D)  + "\n"

# now we cut and paste and mess with the kernel
prg_str  =  N_str + M_str + hx_str  + hy_str  + ht_str + prg_str # Add constatns...
prg_str  =  PP_str  + PSI_str + A_str  + B_str + PIB_str + D_str + prg_str # ...and more constants 
parts = prg_str.split("SPLIT") # Split were we put the Mathematica expression
op_file = open('str2d.txt' ,'r') # open Mathmatica txt file
op_str  = op_file.read() # Read the Mathematica expression
prg_str = "\n\n\n" + parts[0] +  op_str + parts[1] + "\n\n\n" #put the expression where it belongs
file_ = open('tmp_ker.c' , 'w')
file_.write(prg_str)  # save to file, so we see the new kernel
file_.close()
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
    
    # plot, not very interesting
    fig = plt.figure()
    CS = plt.contour(X, Y, T, levels=levels)
    plt.clabel(CS)
    plt.title("Tracer concentration. Spatial FEM and RK2 Time Steps.\n Step " +str(i) + ",T = " + str(i*ht/(60*60*24))+ " days.")
    #plt.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=plt.cm.autumn)
    #plt.colorbar()
    fig.savefig('frames/frame' + str(i) + '.png')
    plt.close(fig)    

    # Copy T into Tin_d
    Tin_d.set( T.ravel(), queue=queue )   

    # Apply the kernel here
    prg.rk_step(queue, T.shape, None, 
                Tin_d.data, Tout_d.data)
    
    # Copy data into T
    Tout_d.get(queue=queue , ary=T)
    

res = os.system("ffmpeg -i frames/frame%d.png euler1D.mpg")
if (res != 0):
    print "Your machine does not have ffmpeg, so there is no movie."
