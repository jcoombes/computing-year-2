"""
Tests the super_boost() method of FourVector class.

This second test ensures boost() has the same behaviour as super_boost() in 1d.
"""
from __future__ import division
import relativity as rel
import numpy as np

fail = False

a0 = rel.FourVector(0,[0,0,0]) #This could be done with a for loop and eval()
a1 = rel.FourVector(10,[0,0,0]) #But Explicit Is Better Than Implicit.
a2 = rel.FourVector(20,[0,0,0])
a3 = rel.FourVector(30,[0,0,0])
a4 = rel.FourVector(40,[0,0,0])
a5 = rel.FourVector(50,[0,0,0])
a6 = rel.FourVector(60,[0,0,0])
a7 = rel.FourVector(70,[0,0,0])
a8 = rel.FourVector(80,[0,0,0])
a9 = rel.FourVector(90,[0,0,0])
a10 = rel.FourVector(100,[0,0,0])

a = [a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10]

b0 = rel.FourVector(0,[0,0,50])
b1 = rel.FourVector(10,[0,0,50])
b2 = rel.FourVector(20,[0,0,50])
b3 = rel.FourVector(30,[0,0,50])
b4 = rel.FourVector(40,[0,0,50])
b5 = rel.FourVector(50,[0,0,50])
b6 = rel.FourVector(60,[0,0,50])
b7 = rel.FourVector(70,[0,0,50])
b8 = rel.FourVector(80,[0,0,50])
b9 = rel.FourVector(90,[0,0,50])
b10 = rel.FourVector(100,[0,0,50])

b = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10]

c0 = rel.FourVector(0,[15,20,65])
c1 = rel.FourVector(10,[15,20,65])
c2 = rel.FourVector(20,[15,20,65])
c3 = rel.FourVector(30,[15,20,65])
c4 = rel.FourVector(40,[15,20,65])
c5 = rel.FourVector(50,[15,20,65])
c6 = rel.FourVector(60,[15,20,65])
c7 = rel.FourVector(70,[15,20,65])
c8 = rel.FourVector(80,[15,20,65])
c9 = rel.FourVector(90,[15,20,65])
c10 = rel.FourVector(100,[15,20,65])

c = [c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]

k0 = np.array([0,0,1])
k1 = np.array([0,0,2])
k2 = np.array([-0,0,15])
k3 = np.array([0,0,10000])

k = [k0,k1,k2,k3]
vectors = a + b + c

for vector in vectors:
    for direction in k:
        temp = rel.FourVector.boost(vector,0.866)
        temp2 = rel.FourVector.super_boost(vector,0.866,direction)
        if not(temp==temp2):
            fail = True
            print 'Fail! {} is not {},dir ={}'.format(temp,temp2,direction)
        if temp2==temp:
            print('.')
         
if not fail:
    print('Success, super_boost -> then <- works in all directions.')
