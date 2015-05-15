import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os
import sys

from constants import *
import getstring

# Glbals
global hz
global hy

global V_zero_yphalf 
global V_zero_ymhalf
global U_xphalf_zero
global U_xmhalf_zero 


def Ufun(X, Y):
    return PIB * psi * np.cos( Y * PIB ) * (   P * np.exp(A*X)  +      (1-P) * np.exp(B*X) -1  )/D
def Vfun(X, Y):
    return      -psi * np.sin( Y * PIB ) * ( A*P * np.exp(A*X)  +  B * (1-P) * np.exp(B*X)    )/D 

def Tbd(T):
    
    yDim , xDim = T.shape
    T_xphalf_zero =  (
        np.concatenate( (T[:,1:],np.zeros((yDim,1)))  ,  axis=1 ) +
        T )/ 2.0

    T_xmhalf_zero =  (
        np.concatenate( ( np.zeros((yDim,1)) , T[:,:-1] ) ,axis=1 ) +
        T )/ 2.0    
    assert T_xphalf_zero.shape == T.shape ,  str(T_xphalf_zero.shape) + "!=" + str(T.shape)
    assert T_xmhalf_zero.shape == T.shape ,  str(T_xmhalf_zero.shape) + "!=" + str(T.shape)

        
    T_zero_yphalf =  (
        np.concatenate( (T[1:,:],np.zeros((1,xDim)))  ,  axis=0 ) +
        T )/ 2.0
    T_zero_ymhalf =  (
        np.concatenate( (T[:-1,:],np.zeros((1,xDim)))  ,  axis=0 ) +
        T )/ 2.0
    assert T_zero_yphalf.shape == T.shape
    assert T_zero_ymhalf.shape == T.shape

    #print "Suck sex!"
    return  T_xphalf_zero , T_xmhalf_zero  , T_zero_yphalf  ,   T_zero_ymhalf



def Op(T):
    
    yDim , xDim = T.shape

    # Get T values on cell boundaries
    T_xphalf_zero , T_xmhalf_zero  , T_zero_yphalf  ,   T_zero_ymhalf = Tbd(T)

    F_xphalf_zero =   U_xphalf_zero * T_xphalf_zero
    F_xmhalf_zero =   U_xmhalf_zero * T_xmhalf_zero 
    
    G_zero_yphalf =   V_zero_yphalf * T_zero_yphalf 
    G_zero_ymhalf =   V_zero_ymhalf * T_zero_ymhalf 
    
    return  -(F_xphalf_zero - F_xmhalf_zero )/ hx -  (G_zero_yphalf - G_zero_ymhalf)/hy
    
    
    
    
target = "pure"
    # RK order 1 = Euler
order = 2

# meshes sizes
hx = 0.01
hy = 0.01

# center locations
xCenters   = np.arange( hx/2,  a + hx/2 , hx) 
yCenters   = np.arange( hy/2,  b + hy/2 , hy) 

# Edge locations
xEdges = np.arange( 0, a+hx , hx)
yEdges = np.arange( 0, b+hy , hy)

# grids
X_zero_phalf, Y_zero_phalf = np.meshgrid( xCenters     , yEdges[1:  ]  )
X_zero_mhalf, Y_zero_mhalf = np.meshgrid( xCenters     , yEdges[ :-1]  )
X_phalf_zero, Y_phalf_zero = np.meshgrid( xEdges[1:  ] , yCenters      )
X_mhalf_zero, Y_mhalf_zero = np.meshgrid( xEdges[ :-1] , yCenters      )

V_zero_yphalf = Vfun( X_zero_phalf, Y_zero_phalf )
V_zero_ymhalf = Vfun( X_zero_mhalf, Y_zero_mhalf )
U_xphalf_zero = Ufun( X_phalf_zero, Y_phalf_zero )
U_xmhalf_zero = Ufun( X_mhalf_zero, Y_mhalf_zero )



# Stream plot data
X, Y = np.meshgrid(xCenters , yCenters  )
U  = PIB * psi * np.cos( Y * PIB ) * (   P * np.exp(A*X)  +      (1-P) * np.exp(B*X) -1  )/D;
V  =     - psi * np.sin( Y * PIB ) * ( A*P * np.exp(A*X)  +  B * (1-P) * np.exp(B*X)     )/D; 

# define the initial distribution of T
T = np.exp( - (  
        ((X-mu[0])/sig[0])**2 +
        ((Y-mu[1])/sig[1])**2 
        )/2.0
              )


cfl = np.max(np.abs(U)) +  np.max(np.abs(V))

    # times
ht    = hx/(factor*cfl)   # time step
nt    = int(2500/ht)    # number of time steps


    

# do time stepping and plotting.
for i  in range(nt):
    
    # plot, not very interesting
    fig = plt.figure()
    CS = plt.contour(X, Y, T, levels=levels)
    plt.clabel(CS)
    plt.title("Tracer concentration. Spatial FEM and RK" + str(order) +" Time Steps.\n Step "
              +str(i) + ",T = " + str(i*ht)+ " weeks.")
    if hasattr(plt, "streamplot"):
        plt.streamplot(X, Y, U, V, linewidth=2)
    fig.savefig(target + '/frame' + str(i) + '.png')
    plt.close(fig)    
        
    # Make time step
    tmp = Op(T)
    T = T + ht*tmp + 0.5*ht*ht*Op(tmp)
            
