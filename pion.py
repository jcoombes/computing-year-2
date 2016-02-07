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
        """
        Make sure e is greater than rest mass of particle.
        """
        if e < m:
            raise ValueError('particle energy is less than the rest mass energy.')
        self.e = e #MeV Lab frame. #2:pf
        self.m = m #MeV
        self.tau = tau #Particle frame. #2:pf
        self.k = np.array(k, dtype='float64') #Lab frame #2: pf
        self.born = np.array(born, dtype = 'float64') #Lf #2: lf
        self.life = tau #pf
        
        self.g = self.e/self.m #lf
        self.b = np.sqrt(1-1/(self.g*self.g)) #lf
        self.p = self.e*self.b # lf
        
        self.knorm = self.k/np.sqrt(self.k.dot(self.k)) #normalised direction lf
        self.pvec = self.p * self.knorm #momentum vector. # lf
        
        self.emom = fv.FourVector(self.e, self.pvec) #energy momentum 4-vector.
        #Muon position 4-vector currently uses lifetime in own frame, position in lab frame
        #Muon energy 4-vector currently uses energy in pion frame. Momentum in momentum/lab frame.    
        
        self.walls = None
        
    def move(self):
        """
        propagates particle for length of life in lab frame.
        
        This method will only work for derived classes (with defined self.life)
        Output distances in light-seconds as c=1.
        Use pion.props.ls2m() for an output in metres.  
        """
        self.lab_emom = self.emom.super_boost(-self.b, self.knorm)
        self.lab_pvec = self.lab_emom.r
        self.lab_e = self.lab_emom.ct
        self.lab_u = self.lab_pvec/self.lab_e
        self.lab_life = Pion.instances[-1].g * self.life
        self.died = self.born + self.lab_u * self.lab_life
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
    
    def hits_walls(self):
        """
        Method to determine location particle ultimately intersects detector walls.
        Use after particle.move()
        """
        t1 = (0-self.born[2])/self.lab_u[2] # z = 0
        t2 = (props.chamber_z-self.born[2])/self.lab_u[2] # z = 100
        
        quant = (self.born[0]*self.lab_u[0] + self.born[1]*self.lab_u[1])
        
        t3 = (-quant+np.sqrt(quant*quant \
        - (self.lab_u.dot(self.lab_u)*\
        (self.born[:2].dot(self.born[:2])-(props.chamber_r*props.chamber_r)))))\
        /self.lab_u.dot(self.lab_u)
        
        first_intersection_time = min([t for t in [t1, t2, t3] if t>0])
        hits = self.born + first_intersection_time*self.lab_u
        
        if first_intersection_time <= self.lab_life: #hits wall before it decays
            self.walls = hits
            return hits
        else:
            return None
         
    def inside(self):
        """
        Return true if a particle is inside chamber.
        Use after particle.move().
        """
        if hasattr(self, 'walls') and self.walls is not None:
            x = self.walls
        elif hasattr(self, 'died') and self.died is not None:
            x = self.died
        else:
            x = self.born
        
        if x[0]*x[0] + x[1] * x[1] <= props.chamber_r*props.chamber_r:
            return True
        elif 100 >= x[2] >= 0:
            return True
        else:
            return False
        
    
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
            
        else:
            energy = (props.pion_mass*props.pion_mass
                    +props.electron_mass*props.electron_mass)/(2*props.pion_mass)
                    #Assumes zero neutrino mass. 
            return Electron(energy, self.died, self.decay_direction(),parent = 'Pion')
    
    def hits_walls(self):
        """
        Specific pion method to detect if pion hits the back wall of the chamber.
        Returns None if False, Returns co-ordinates if true.
        """
        if self.died[2] >= props.chamber_z:
            self.walls = np.array([0,0,props.chamber_z], dtype = 'float64')
            return self.walls
    """
    def detect(self):
        raise NotImplementedError
    """
    
    
    def __str__(self):
        '''Returns a string representation of particle.
        This output should be used to debug.
        Do not use the output of this to create new pions.'''
        #Note that I need to use energy, self.born, self.hits, detected?
        if hasattr(self, 'walls'):
            if hasattr(self, 'detected'):
                ans = 'Pion({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, self.walls, self.detected)
            else:
                ans = 'Pion({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, self.walls, 'None')
        elif hasattr(self, 'detected'):
            ans = 'Pion({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, 'None ',self.detected)
        else:
            ans = 'Pion({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, 'None ','None')
        return ans


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
   
    def __str__(self):
        '''
        Returns a string representation of the particle.
        This output should be used to debug.
        Do not use this output to make new muons.
        '''
        #Note that I need to use energy, self.born, self.hits, detected?
        if hasattr(self, 'walls'):
            if hasattr(self, 'detected'):
                ans = 'Muon({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, self.walls, self.detected)
            else:
                ans = 'Muon({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, self.walls, 'None')
        elif hasattr(self, 'detected'):
            ans = 'Muon({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, 'None ',self.detected)
        else:
            ans = 'Muon({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, 'None ','None')
        
        return ans 
    
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
        
    
    def __str__(self):
        '''
        Returns a string representation of the particle.
        This output should be used to debug.
        Do not use this output to make new electrons.
        '''
        #Note that I need to use energy, self.born, self.hits, detected?
        if hasattr(self, 'walls'):
            if hasattr(self, 'detected'):
                ans = 'Electron({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, self.walls, self.detected)
            else:
                ans = 'Electron({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, self.walls, 'None')
        elif hasattr(self, 'detected'):
            ans = 'Electron({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, 'None ',self.detected)
        else:
            ans = 'Electron({},died = {}, walls = {}, detected = {})'\
                .format(self.e, self.died, 'None ','None')
        
        return ans 
