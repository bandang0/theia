'''Test the optics module.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)


import optics
from optics import geometry as geo
from optics import beam as gbeam
from optics import mirror
from units import *
from helpers import *

# geometrical data

bm = gbeam.GaussianBeam(Wx = 1*cm, Wy = 1*cm, WDistx = 0, WDisty = 0)
print(bm)

mr = mirror.Mirror(1.*cm, 50.*cm, HRCenter = [2*m,0*m,0*m], HRNorm = [1, 0, 0],
ARr = 0.5, ARt = 0.5, HRr = 0.5, HRt = 0.5, ARK = -.001, HRK = -.001)
print(mr)


print mr.isHit(bm)

newBeams = mr.hit(bm, order = 2, threshold = 1*uW)

print 'Reflected:'
print newBeams['r']

print 'Refracted:'
print newBeams['t']
