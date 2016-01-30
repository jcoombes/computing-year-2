"""
A program to optimise the design of a simple particle physics experiment.

Note natural units are used here so h-bar = c = 1.
"""

from __future__ import division
import numpy as np
import fourvectors as fv
import properties as props

class Particle(object):
    """
    A particle base class, provides relativistic movement.
    
    Inputs:
        e - energy. float. measured in MeV.
        m - mass. float. measured in MeV
        tau - lifetime. measured in s.
        k - direction of travel. defaults to z-axis.

    """
    
    def __init__(self, e=500, m=0, tau = 1, k = [0,0,1], places = []):
        self.e = e #MeV #Make sure to encapsulate data at some point.
        self.m = m #MeV
        self.tau = tau
        self.k = np.array(k, dtype='float64')
        self.places = np.array(places, dtype = 'float64')
        
        self.g = self.e/self.m
        self.b = np.sqrt(1-1/(self.g*self.g))
        self.p = self.e*self.b
        
        self.knorm = self.k/np.sqrt(self.k.dot(self.k)) #normalised direction
        self.pvec = self.p * self.knorm #momentum vector.
        
        self.emom = fv.FourVector(self.e, self.pvec) #energy momentum 4-vector.
"""
class Pion(Particle):
    raise NotImplementedError

class Muon(Particle):
    raise NotImplementedError

class Electron(Particle):
    raise NotImplementedError
"""
