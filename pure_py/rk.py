# numerix
import numpy as np
import scipy as scp

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import helper


# the range of xs and ys
xStart = 0.0
yStart = 0.0
xEnd   = 1.5
yEnd   = 1.0

levels = [ 0.15 , 0.3 , 0.45, 0.5 , 0.75]

# mesh sizes
hx = 0.005
hy = 0.005
#assert x/hx -int(x/hx) == 0.0 , "hx does not fit in x: "  + str(x/hx) + " , " +str(int(x/hx))
#assert y/hy -int(y/hy) == 0.0 , "hy does not fit in y: "  + str(y/hy) + " , " +str(int(y/hy))

# times
ht= 0.005 # time step
final = 10.0
nt   = final/ht

# mean and variance of initial data
mu  = (0.5 , 0.5)
sig = 0.01;

# center locations
xCenters = np.arange(xStart +hx/2, xEnd + hx/2 , hx)
yCenters = np.arange(yStart +hy/2, yEnd + hy/2 , hy)

# number of elements on boundaries
#nxBoundary = len(xBoundary)
#assert nxBoundary == x/hx + 1

#nyBoundary = len(yBoundary)
#assert nyBoundary == y/hy + 1 , str(nyBoundary) + " != " + str(y/hy + 1) 

nxCenters  = len(xCenters)
#assert nxCenters == x/hx

nyCenters  = len(yCenters)
#assert nyCenters == y/hy

# get grids
X ,Y = np.meshgrid( xCenters, yCenters )

# define the initial distribution of T
T = np.exp( - (  (X - mu[0])**2 + ( Y -mu[1])**2 )/(2*sig) )
assert  T.shape == (nyCenters , nxCenters ) 


# plot or not
if 0:
    plt.figure(0)
    CS = plt.contour(X, Y, T)# , levels)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Plots of  T, time = 0' )
    plt.show()

# define flows on edges 
uVertBound  =  np.ones  ( ( nyCenters   , nxCenters+1) )
vHorzBound  =  np.zeros( ( nyCenters+1 , nxCenters  ) )

assert uVertBound.shape == ( nyCenters   , nxCenters+1)
assert vHorzBound.shape == ( nyCenters+1 , nxCenters  )

# do time stepping.
for i  in range(0,int(nt)):
    

    fig = plt.figure()
    CS = plt.contour(X, Y, T, levels)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Plots of  T, time = ' + str(i*ht))
    fig.savefig('frames/rk/T' + str(i*ht) + '.png')
    plt.close(fig)

    T  = helper.RK3(T, uVertBound, vHorzBound, hx, hy ,ht)

