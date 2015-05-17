import csv

rk1size = []
rk2size = []
rk3size = []
rk1time = []
rk2time = []
rk3time = []

with open('res/cedar3d.txt', 'r') as csvfile:
    res = csv.reader(csvfile, delimiter=',')
    for row in res:
        
        if row[0] == 'RK order ':
            pass
        elif int(row[0]) == 1:
            rk1size.append(float(row[3]))
            rk1time.append(float(row[4])/float(row[2]))
        elif int(row[0]) == 2:
            rk2size.append(float(row[3]))
            rk2time.append(float(row[4])/float(row[2]))
        elif int(row[0]) == 3:
            rk3size.append(float(row[3]))
            rk3time.append(float(row[4])/float(row[2]))

import matplotlib.pyplot as plt

plt.plot(rk1size, rk1time, 'r--', label = 'RK1')
plt.plot(rk2size, rk2time, 'b--', label = 'RK2')
plt.plot(rk3size, rk3time, 'g--', label = 'RK3')
plt.plot(rk1size, rk1time, 'rs', rk2size, rk2time, 'bs', rk3size, rk3time, 'gs')
plt.title("Run time of 3D solutions for different RK methods")
plt.xlabel("Problem size - number of grid points")
plt.ylabel("run time in seconds")
plt.legend(loc = 2)
plt.savefig('pdf/3d.png')
        
