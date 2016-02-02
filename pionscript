"""
Unit test to ensure pions are created with the right distribution (exponential)
Nothing decays yet.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pion
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ilist = []
for ii in range(100000):
    ii = pion.Pion(500)
    ilist.append(ii)

jlist = []
for j in range(100000):
    j = pion.Pion(10000)
    jlist.append(j)

def gen_coord(ind, listy):
    for pi in listy:
        pi.move()
        yield pi.died[ind]

x= np.fromiter(gen_coord(0,ilist),dtype ='float64')
y= np.fromiter(gen_coord(1,ilist), dtype ='float64')
z= np.fromiter(gen_coord(2,ilist), dtype ='float64')

x2= np.fromiter(gen_coord(0,jlist),dtype ='float64')
y2= np.fromiter(gen_coord(1,jlist), dtype ='float64')
z2= np.fromiter(gen_coord(2,jlist), dtype ='float64')

ax.scatter(z,x,y,c='red')
ax.scatter(z2,x2,y2,c='yellow')
plt.xlabel('z')
plt.ylabel('x')
