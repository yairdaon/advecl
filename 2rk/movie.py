import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os

# contour plot levels
levels = np.arange(0.01,1.51,0.05)

X = np.load("data/X.npy")
Y = np.load("data/Y.npy")
times = np.load("data/times.npy")
ht = times[0]
final = times[1]
for i in range(int(final/ht)):

    # load file to memory
    tmp = "data/array" +str(i) +".npy"
    
    # Load T
    T = np.load(tmp)
    
    # plot, not very interesting
    fig = plt.figure()
    CS = plt.contour(X, Y, T, levels=levels)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title("Tracer concentration. Spatial FEM and Fwd Euler Time Steps. Step " +str(i))
    fig.savefig('frames/frame' + str(i) + '.png')
    plt.close(fig)    
    os.remove(tmp)

res = os.system("ffmpeg -i frames/frame%d.png euler1D.mpg")
if (res != 0):
    print "Your machine does not have ffmpeg, so there is no movie."
