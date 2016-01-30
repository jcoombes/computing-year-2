"""
Tests the super_boost() method of FourVector class.

This first test ensures the boost forwards then backwards returns
the original minkowski vector.
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
k1 = np.array([1,2,3])
k2 = np.array([-0.4,0.14,0])
k3 = np.array([5,0,3])
k4 = np.array([2,2,2])
k5 = np.array([10,10,10])
k6 = np.array([0.2,0.3,0.07])
k7 = np.array([0,0,34])
k8 = np.array([2,4,6])
k9 = np.array([8,8,8])
k10 = np.array([0,0,10000])

k = [k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10]
vectors = a + b + c

for vector in vectors:
    for direction in k:
        temp = rel.FourVector.super_boost(vector,0.866,direction)
        temp2 = rel.FourVector.super_boost(temp,0.866,-direction)
        if not(temp2==vector):
            fail = True
            print 'Fail! {} is not {},dir ={}'.format(vector,temp2,direction)
        if temp2==vector:
            print('.')
         
if not fail:
    print('Success, super_boost -> then <- works in all directions.')
