import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os

# contour plot levels
levels = np.arange(0.01,1.51,0.05)

xCenters = np.load("data/xCenters.npy")
times = np.load("data/times.npy")
ht = times[0]
final = times[1]

for i in range(int(final/ht)):

    # Load T
    T = np.load("data/array" +str(i) +".npy")
    
    # plot, not very interesting
    fig = plt.figure()
    plt.plot(xCenters,T)
    plt.title("Tracer concentration. Spatial FEM and Fwd Euler Time Steps. Step " +str(i))
    plt.axis([0.0,1.0,0.0,1.5])
    fig.savefig('frames/frame' + str(i) + '.png')
    plt.close(fig)    


res = os.system("ffmpeg -i frames/frame%d.png euler1D.mpg")
if (res != 0):
    print "Your machine does not have ffmpeg, so there is no movie."
