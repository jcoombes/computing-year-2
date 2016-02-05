# -*- coding: utf-8 -*-
'''
A module filled with particle properties.

Useful to ensure the same value is used for every constant.
'''
import numpy as np


pion_mass = 139.6 #MeV
pion_lifetime = 2.6e-8 #s

muon_mass = 105.7 #MeV
muon_lifetime = 2.2e-6 #s

electron_mass = 0.5 #MeV
#electron lifetime is so long we can assume it lives forever.
#also neutrino mass is 0.320eV. We can assume they're massless.

# 1eV^-1 of length = 1.97327e-7 m
# 1eV of mass = 1.782662e-36 kilograms
# 1eV-1 of time = 6.582119e-16 seconds

def michel():
    x,y = np.random.sample(2)
    if x > y:
        return x * 53
    else:
        return y * 53

def ls2m(lightseconds):
    """
    Convert light seconds to natural units.
    Only use this to make output more human friendly.
    Not built to do any calculations in metres.
    
    Inputs:
        lightseconds - float.
    """
    return lightseconds*299792458
