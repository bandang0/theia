'''Test the optics module.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)


from optics import beam, beamdump, thinlens, thicklens, mirror
from units import *

# input data
bm = beam.GaussianBeam(Wx = 1*cm, Wy = 1*cm, WDistx = 0, WDisty = 0)
bd = beamdump.BeamDump(Center = 10*cm, Norm = [-1, 0, 0], Thickness = 5*cm)
thin = thinlens.ThinLens()
thick = thick.ThickLens()
mr = mirror.Mirror()

print(bm)
print(bd)
print(thin)
print(thick)
print(mr)
