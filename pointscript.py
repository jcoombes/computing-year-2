"""
Are our direction vectors spherically uniform?
let's eyeball it.
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pion
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

listy = []
for i in range(100000):
    listy.append(pion.Pion())

points = [i.decay_direction() for i in (pion.Pion(2000) for i in range(1000))]
xs = [ar[0] for ar in points]
ys = [ar[1] for ar in points]
zs = [ar[2] for ar in points]

print 'average x is {}'.format(np.mean(xs))
print 'average y is {}'.format(np.mean(ys))
print 'average z is {}'.format(np.mean(zs))
ax.scatter(xs,ys,zs)
