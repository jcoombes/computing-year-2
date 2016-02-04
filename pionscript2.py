"""
Unit test to ensure pions are created with the right distribution (exponential)
Nothing decays yet.

Source of /graphics/generating_pions.png

Note this script works with versions of pion.py before the 04/02/2016 changes.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pion
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)

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
        yield pion.ls2m(pi.died[ind]) #Convert lab frame decay location to metres.

x= np.fromiter(gen_coord(0,ilist),dtype ='float64')
z= np.fromiter(gen_coord(2,ilist), dtype ='float64')

x2= np.fromiter(gen_coord(0,jlist),dtype ='float64')
z2= np.fromiter(gen_coord(2,jlist), dtype ='float64')

plt.xlabel('Distance travelled in metres before decay.')
plt.ylabel('Number of pions.')

print(len(z),len(z2),'samples')

print("mean distance travelled of 500MeV pions is",np.mean(z))
print("mean distance travelled of 10,000MeV pions is",np.mean(z2))

print("standard deviation in distance travelled of 500MeV pions is",np.std(z))
print("standard deviation in distance travelled of 10,000MeV pions is",np.std(z2))

plt.hist(z,bins = 1000,histtype = 'stepfilled', color='magenta',alpha = 0.5)
plt.hist(z2,bins=1000,histtype = 'stepfilled', color='yellow',alpha = 0.5)
plt.savefig('pion energies',format ='jpg')
