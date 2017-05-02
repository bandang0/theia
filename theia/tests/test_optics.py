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
pos1 = [0.5, 0., 0.]
pos2 = [2., 0., 0.]
pos3 = [0., 2., 0.]
pos4 = [0., 0., 0.]
pos5 = [0., 0., 0.]

dirV1 = [1., 0., 0.]
dirV2 = [-1., 0., 0.]
dirV3 = [0., 1., 0.]
dirV4 = [0., -1, 0.]

planeC1 = [4, 0, 0]
planeC2= [0., 4., 0.]

normV1 = [1., 0., 0.]
normV2 = [-1, 0., 0.]
normV3 = [0., 0., 1]

diameter1 = 4.
diameter2 = 2

chordC = [0., 3., 0.]
chordNorm1 = [0., 1., 0.]
chordNorm2 = [0., -1., 0.]

kurv1 = 1.0e-6
kurv2 = .01

# tests
print geo.linePlaneInter(pos1, dirV1, planeC1, normV1, diameter1)
print geo.linePlaneInter(pos2, dirV1, planeC1, normV1, diameter1)
print geo.linePlaneInter(pos1, dirV1, planeC1, normV2, diameter2)
print geo.linePlaneInter(pos2, dirV2, planeC2, normV3, diameter1)

print geo.lineSurfInter(pos1, dirV3, chordC, chordNorm1, kurv2, diameter1)
print geo.lineSurfInter(pos1, dirV3, chordC, chordNorm2, kurv2, diameter1)
print geo.lineSurfInter(pos1, dirV3, chordC, chordNorm1, kurv1, diameter1)

bm = gbeam.GaussianBeam(Wx = 1*cm, Wy = 1*cm, WDistx = 0, WDisty = 0)

print bm.Q(0)
print bm.QTens

mr = mirror.Mirror(1.*cm, 50.*cm, HRCenter = [2*m,0*m,0*m])

print mr.isHit(bm)

print mr.hit(bm)
