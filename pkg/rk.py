# numerix
import numpy as np
import scipy as scp

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import helper


# the range of xs and ys
x = 1.5
y = 1.0

# mesh sizes
hx = 0.005
hy = 0.005
assert x/hx -int(x/hx) == 0.0 , "hx does not fit in x: "  + str(x/hx) + " , " +str(int(x/hx))
assert y/hy -int(y/hy) == 0.0 , "hy does not fit in y: "  + str(y/hy) + " , " +str(int(y/hy))

# times
ht= 0.01 # time step
final = 4.0
nt   = final/ht

# mean and variance of initial data
mu  = (0.5 , 0.5)
sig = 0.01;

# boundary grids
xBoundary = np.arange(0, x+hx, hx)
yBoundary = np.arange(0, y+hy, hy)


# center locations
xCenters = xBoundary + hx/2.0
xCenters = xCenters[0:-1]
yCenters = yBoundary + hy/2.0
yCenters = yCenters[0:-1]

# number of elements on boundaries
nxBoundary = len(xBoundary)
assert nxBoundary == x/hx + 1

nyBoundary = len(yBoundary)
assert nyBoundary == y/hy + 1 , str(nyBoundary) + " != " + str(y/hy + 1) 

nxCenters  = len(xCenters)
assert nxCenters == x/hx

nyCenters  = len(yCenters)
assert nyCenters == y/hy

# get grids
X ,Y = np.meshgrid( xCenters, yCenters )

# define the initial distribution of T
T = np.exp( - (  (X - mu[0])**2 + ( Y -mu[1])**2 )/(2*sig) )
assert  T.shape == (nyCenters , nxCenters ) 


# plot or not
if 0:
    plt.figure(0)
    CS = plt.contour(X, Y, T)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Plots of  T, time = 0' )
    plt.show()

Tx , Ty = helper.T_on_boundaries(T)

# define flows on edges
uBoundary  =  np.ones ( Tx.shape )
vBoundary  =  np.zeros( Ty.shape )

# get the F and G arrays
F = helper.F(uBoundary, Tx)
G = helper.G(vBoundary, Ty)

# do time stepping.
for i  in range(0,int(nt)):
    
    dF = F[:,1:] - F[:,0:nxBoundary -1]
    assert dF.shape == T.shape

    dG = G[1:,:] - G[0:nyBoundary- 1,:]
    assert dG.shape == T.shape

    dT = -(dF*hy + dG*hx)/(hx*hy)
    T  = T + ht*dT

    fig = plt.figure()
    CS = plt.contour(X, Y, T)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Plots of  T, time = ' + str(i*ht))
    fig.savefig('frames/euler/T' + str(i*ht) + '.png')
    plt.close(fig)
