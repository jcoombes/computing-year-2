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
        born - initial location. expect len(born)==3.
        died - final location. expect len(died)==3.

    """
    
    def __init__(self, e = 500, m=0, tau = 1, k = [0,0,1], born = [0,0,0], died = [0,0,0]):
        #Make sure to encapsulate data at some point.
        self.e = e #MeV
        self.m = m #MeV
        self.tau = tau
        self.k = np.array(k, dtype='float64')
        self.born = np.array(born, dtype = 'float64')
        self.died = np.array(died, dtype = 'float64')
        self.life = tau
        
        self.g = self.e/self.m
        self.b = np.sqrt(1-1/(self.g*self.g))
        self.p = self.e*self.b
        
        self.knorm = self.k/np.sqrt(self.k.dot(self.k)) #normalised direction
        self.pvec = self.p * self.knorm #momentum vector.
        
        self.emom = fv.FourVector(self.e, self.pvec) #energy momentum 4-vector.
        
    def move(self, lab = True):
        """
        propagates particle for length of life in lab frame.
        
        This method will only work for derived classes (with defined self.life)
        lab - Bool. Are we already in lab frame? if False, we need to convert.
        
        Output distances in light-seconds as c=1.
        """
        if lab:
            self.died = self.born + self.knorm * self.life * self.b
        else:
            self.died = self.born + self.knorm * self.life * self.b * self.g 
            
        return self.died

class Pion(Particle):
    """
    It's a pion. All our particles start off as these.
    """
    pion_lives = np.random.exponential(props.pion_lifetime,1E8)
    seed = 0 # so we can get back the same exp-distributed rand numbers.
    #Code is faster if we generate lots at once then look it up.
    
    rollcall = []
    
    def __init__(self, e = 500, m = props.pion_mass , tau = props.pion_lifetime, branch = 0.5):
        super(Pion, self).__init__(e, m, tau)
        self.branch = branch #Branching Ratio. REALLY IMPORTANT.
        self.life = self.pion_lives[self.seed]
        Pion.seed += 1
        Pion.rollcall.append(self)
    
    
    """
    def decay():
        raise NotImplementedError
    
    def detect():
        raise NotImplementedError
    """

"""
class Muon(Particle):
    raise NotImplementedError
    Muon.muon_lives = np.random.exponential(props.muon_lifetime, 1E7)

class Electron(Particle):
    raise NotImplementedError
"""

def ls2m(lightseconds):
    """
    Convert light seconds to natural units.
    Only use this to make output more human friendly.
    Not built to do any calculations in metres.
    
    Inputs:
        lightseconds - float.
    """
    return lightseconds*299792458
