# FDTD-1D-Gaussian_Additive-Source_Waterfall-Plot

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter


imp0 = 377.0
tSIZE = 600
SPACE = 300
ez_value = np.zeros((800,300))
ez = np.zeros(SPACE+1)
hy = np.zeros(SPACE)



# doing FDTD
for time in range(tSIZE):
    
    for mm in range(SPACE-1):
        hy[mm] = hy[mm] + (ez[mm+1] - ez[mm])/imp0
    for mm in range(1,SPACE):
        ez[mm] = ez[mm] + (hy[mm] - hy[mm-1])*imp0
    ez[100] += 5*np.exp(-(time -40.0)**2/100.0)
    for z in range(SPACE-1):
        ez_value[time][z]=ez[z]    
    

    
# for plot, make the boundary value at 800 time become 0
for z in range(1,SPACE): 
    ez_value[tSIZE-1][z] = 0


zs = np.arange(0.0, float(tSIZE), 10.0)
# Attract the data 20 unit of space per step# 
xs = np.arange(0.0,float(SPACE))  
verts = []

for z in zs:
    ys = ez_value[:][z]
    verts.append(zip(xs,ys))

        
fig = plt.figure()
ax = fig.gca(projection='3d')

    
cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

poly = PolyCollection(verts, facecolors = [cc('b') for x in zs]) # control the color of each set
poly.set_alpha(0.7)

ax.add_collection3d(poly, zs=zs, zdir='y')

plt.xlabel('Position')
plt.ylabel('Time')
plt.title('Propagation of a Gaussian wave')
ax.set_xlim(0,max(xs))
ax.set_ylim(0,tSIZE+1)
ax.set_zlim(-5,5)
                      
plt.show()
