"""
Tests the decay function changes variables as expected.
"""

import pion
pen0 = pion.Pion(500)
pen1 = pion.Pion(500)
pen2 = pion.Pion(500)
pen3 = pion.Pion(500)
pen4 = pion.Pion(500)
pen5 = pion.Pion(500)
pen6 = pion.Pion(500)
pen7 = pion.Pion(500)
pen8 = pion.Pion(500)
pen9 = pion.Pion(500)

pat0 = pion.Pion(10000)
pat1 = pion.Pion(10000)
pat2 = pion.Pion(10000)
pat3 = pion.Pion(10000)
pat4 = pion.Pion(10000)
pat5 = pion.Pion(10000)
pat6 = pion.Pion(10000)
pat7 = pion.Pion(10000)
pat8 = pion.Pion(10000)
pat9 = pion.Pion(10000)

pens = [pen0, pen1, pen2, pen3, pen4, pen5, pen6, pen7, pen8, pen9]
pats = [pat0, pat1, pat2, pat3, pat4, pat5, pat6, pat7, pat8, pat9]

slow_muons = []
slow_electrons = []

for pi in pens:
    pi.move()
    for i in range(100000):
        slow = pi.decay()
        if isinstance(slow, pion.Muon):
            slow_muons.append(slow)
        elif isinstance(slow, pion.Electron):
            slow_electrons.append(slow)
        else:
            raise ValueError('{}'.format(type(slow)))

fast_muons = []
fast_electrons = []

for pi in pats:
    pi.move()
    for i in range(100000):
        fast = pi.decay()
        if isinstance(fast, pion.Muon):
            fast_muons.append(fast)
        elif isinstance(fast, pion.Electron):
            fast_electrons.append(fast)
        else:
            raise ValueError('{}'.format(type(fast)))

print('The branching ratio is {}'.format(pat9.branch))
print('len(slow_muons is {})'.format(len(slow_muons)))
print('len(slow_electrons is {})'.format(len(slow_electrons)))
print('len(fast_muons is {})'.format(len(fast_muons)))
print('len(fast_electrons is {})'.format(len(fast_electrons)))
