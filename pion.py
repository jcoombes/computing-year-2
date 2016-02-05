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
        born - initial location. expect len(born)==3.
        k - direction of travel.
        m - mass. float. measured in MeV
        tau - lifetime. measured in s.
    """
    
    def __init__(self, e, born, k, m, tau):
        #Make sure to encapsulate data at some point.
        self.e = e #MeV
        self.m = m #MeV
        self.tau = tau
        self.k = np.array(k, dtype='float64')
        self.born = np.array(born, dtype = 'float64')
        self.life = tau
        
        self.g = self.e/self.m
        self.b = np.sqrt(1-1/(self.g*self.g))
        self.p = self.e*self.b
        
        self.knorm = self.k/np.sqrt(self.k.dot(self.k)) #normalised direction
        self.pvec = self.p * self.knorm #momentum vector.
        
        self.emom = fv.FourVector(self.e, self.pvec) #energy momentum 4-vector.
        #Muon position 4-vector currently uses lifetime in own frame, position in lab frame
        #Muon energy 4-vector currently uses energy in pion frame. Momentum in momentum/ab frame.
    
    def move(self):
        """
        propagates particle for length of life in lab frame.
        
        This method will only work for derived classes (with defined self.life)
        Output distances in light-seconds as c=1.
        Use pion.props.ls2m() for an output in metres.  
        """
        rest_position = fv.FourVector(self.life, self.born)
        lab_position = rest_position.super_boost(-self.b, self.knorm)
        #This line currently converts muon frame to some other frame. Not lab!!!
        self.died = lab_position.r
        return self.died
    
    def decay_direction(self):
        """
        Randomly generates a uniform vector on the unit sphere.
        """
        u = np.random.sample()
        v = np.random.sample()
        phi = 2*np.pi*u
        theta = np.arccos(2*v-1) #mathworld.wolfram.com/SpherePointPicking.html
        
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        return np.array([x,y,z])
    """
    def out_of_bounds(self):
        if
    """
class Pion(Particle):
    """
    It's a pion. All our particles start off as these.
    """
    pion_lives = np.random.exponential(props.pion_lifetime,2E7)
    seed = 0 # so we can get back the same exp-distributed rand numbers.
    #Code is faster if we generate lots at once then look it up.
    
    instances = []
    
    def __init__(self, e, born = [0,0,0], k = [0,0,1], m = props.pion_mass , tau = props.pion_lifetime, branch = 0.0001):
        super(Pion, self).__init__(e, born, k, m, tau)
        self.branch = branch #Branching Ratio. REALLY IMPORTANT.
        self.life = self.pion_lives[self.seed]
        Pion.seed += 1
        Pion.instances.append(self)
    
    def move(self):
        """
        Special faster pion method to move faster than the general lorenz boost.
        propagates particle for length of life in lab frame.
        
        Output distances in light-seconds as c=1.
        See ls2m function in properties file for output in metres.
        """
        self.died = self.knorm * self.life * self.b * self.g  
        return self.died
       
    def decay(self):
        """
            Deletes particle.
            Makes new particle.
            
            Note if self.died hasn't been set by move() the particle decays in place.
        """
        if np.random.sample() > self.branch:
            
            energy = (props.pion_mass*props.pion_mass
                    +props.muon_mass*props.muon_mass)/(2*props.pion_mass)
                    #Assumes zero neutrino mass. 
            return Muon(energy, self.died, self.decay_direction())
            
        else:leccy
            energy = (props.pion_mass*props.pion_mass
                    +props.electron_mass*props.electron_mass)/(2*props.pion_mass)
                    #Assumes zero neutrino mass. 
            return Electron(energy, self.died, self.decay_direction(),parent = 'Pion')
    """
    def detect(self):
        raise NotImplementedError
    """


class Muon(Particle):
    """
    It's a muon. Pions decay into this.
    Inputs:
        e - total energy.
        born - initial position. 3-position.
        k - initial direction in created frame.
    """
    muon_lives = np.random.exponential(props.muon_lifetime, 2e7)
    seed = 0 # so we can get back the same exp-distributed rand numbers.
    #Code is faster if we generate lots at once then look it up.
    
    instances = []
    
    def __init__(self, e, born, k, m = props.muon_mass, tau = props.muon_lifetime):
        super(Muon, self).__init__(e, born, k, m, tau)
        self.life = self.muon_lives[self.seed]
        Muon.seed += 1
        Muon.instances.append(self)
    
    def decay(self):
        """
        Unlike pion decays, muons can only decay into electrons.
        """
        return Electron(props.michel(), self.died, self.decay_direction(), parent = 'Muon')
        
    
class Electron(Particle):
    """
    It's an electron. Electrons have an extra parameter showing their parent.
    """
    instances = []
    
    def __init__(self, e, born, k, m = props.electron_mass, parent = 'Pion'):
        tau = 1
        super(Electron, self).__init__(e, born, k, m, tau)
        self.parent = parent
        #Easier to have both pion and muon inherit from particle,
        #and delete tau in electron, than implement for both pion and muon.
        Electron.instances.append(self)
