# -*- coding: utf-8 -*-
"""
Implements relativistic four vectors. Note we assume natural units c = 1 here.
"""

from __future__ import division
import numpy as np

class FourVector(object):
    """
    Represents a point in Minkowsky space.
    
    ct - float, time-like component.
    r - array, space-like component. Expected length 3.
    """
    def __init__(self, ct = 0, r = np.array([0,0,0])):
        if len(r) != 3:
            raise Exception("FourVector parameter length.")
        self.__ct = float(ct)
        self.__r = np.array(r,dtype='float64')
        
    def __repr__(self):
        return "FourVector(ct = {0}, r = [{1},{2},{3}])".format(self.ct, self.r[0],self.r[1], self.r[2])
        
    def __str__(self):
        out_list = [self.ct, \
        self.r[0],\
        self.r[1],\
        self.r[2]]
        return str(out_list)
    
    def __add__(self, other):
        return FourVector(self.ct + other.ct, self.r + other.r)
    
    def __iadd__(self, other):
        return FourVector(self.ct + other.ct, self.r + other.r)
    
    def __sub__(self, other):
        return FourVector(self.ct - other.ct, self.r - other.r)
    
    def __isub__(self, other):
        return FourVector(self.ct - other.ct, self.r - other.r)
    
    def __eq__(self, other):
        if not np.all(np.isclose(self.r, other.r)):
            return False
        elif not np.isclose(self.ct,other.ct):
            return False
        else: return True
    
    @property    
    def ct(self):
        return self.__ct
    
    @property
    def r(self):
        return self.__r
    
    def copy(self):
        """Returns a distinct FourVector with the same values."""
        return(eval(repr(self))) #repr(self) will instantiate a new 4-vector with same values.
    
    def inner(self, other):
        """Returns the inner product of two 4-vectors.
        Note we use the + - - - convention here."""
        return self.ct*other.ct - self.r.dot(other.r)
    
    def magsquare(self):
        """Returns the magnitude of the 4-vector squared.
        """
        return self.inner(self)
    
    def boost(self, beta):
        """ Returns a new 4-vector after a Lorenz transformation in the z axis.
        Inputs:
            beta - fraction of the speed of light. number between zero and 1.
        """
        gamma = 1.0/np.sqrt(1 - beta*beta)
        new_z = gamma*(self.r[2]-beta*self.ct)
        new_ct = gamma *(self.ct - beta*self.r[2])
        return FourVector(new_ct, [self.r[0],self.r[1], new_z])
    
    def super_boost(self, b, k):
        '''
        Provides a lorenz boost in an arbitrary direction using 4d matrix.
        
        b(eta) - velocity in units of c.
        k - numpy array. Which way do you want to boost?  len(k) == 3. 
        '''
        k = np.array(k,dtype='float64')
        if abs(b) >= 1.0:
            raise ValueError('Faster than the speed of Light!')
        if np.allclose(k,[0,0,0]):
            raise ValueError('boost direction shouldn\'t be [0,0,0]')
        mag_dir = np.sqrt(k.dot(k))
        if not np.allclose(mag_dir,1): #if Not normalised:
            k = k/mag_dir # normalise it. note /= doesn't work here.
        g = 1.0/np.sqrt(1 - b*b) #Lorenz factor gamma shortened to g for brevity
        
        boost = np.array([
        [g,         -g*b*k[0],          -g*b*k[1],          -g*b*k[2]],
        [-g*b*k[0], 1+(g-1)*k[0]*k[0],  (g-1)*k[0]*k[1],     (g-1)*k[0]*k[2]], 
        [-g*b*k[1], (g-1)*k[1]*k[0],    1+(g-1)*k[1]*k[1],   (g-1)*k[1]*k[2]],
        [-g*b*k[2], (g-1)*k[2]*k[0],    (g-1)*k[2]*k[1],   1+(g-1)*k[2]*k[2]]])
        
        array_ans = boost.dot(np.array(
        [self.ct, self.r[0],self.r[1],self.r[2]]
        ))
        
        return FourVector(ct = array_ans[0], r = array_ans[1:])
