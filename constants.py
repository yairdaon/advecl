import math
import numpy as np

# Natural parameters. Distance mesured in millions of meters,
# mass measured in 1e18 kgs
# time measured in weeks
a     = 1       # west  to east - X axis - distanc
b     = 1       # north to west - Y axis - distance
c     = 1       # depth, for 3D simulations
tau   = 0.0365  # = 0.1*(60*60*24*7)**2/1e12     # wind stress
rho   = 1e6     # density - mass/volume = mass/distance^3
beta  = 6e-5    # 1/distance
D     = 0.0086  # atlantic ocean depth - distance
C_d   = 0.0025  # pure number

# Derived quantities
alpha = beta/C_d 
A     = -alpha/2.0 + math.sqrt( (alpha/2)**2 + (math.pi/b)**2 )
B     = -alpha/2.0 - math.sqrt( (alpha/2)**2 + (math.pi/b)**2 )
psi   = (tau * b) / (rho * C_d * math.pi )
P     = (1-math.exp(B*a))/(math.exp(A*a)-math.exp(B*a))
PIB   = math.pi/b

# mean and variance of initial data
mu  = (0.5   ,0.4 , 0.3  )
sig = (0.05  ,0.05, 0.05 ) 

# Number of speed test iterations
nSpeed = 150

# RK order 1 = Euler
orders = [1, 2, 3]

# Spatial discretizations
hs = [0.1 , 0.05 , 0.025, 0.02, 0.0125 , 0.01 , 5e-3 ]

# CFL multiplier factor
factor = 5.0

# contour levels
levels = np.arange(0.05 , 1.1 , 0.15)

# Save the kernel?
saveTmpKer=False
