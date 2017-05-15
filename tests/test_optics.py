'''Test the optics module.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)


from optics import beam, beamdump, thinlens, thicklens, mirror
from units import *

# input data
bm = beam.GaussianBeam(Wx = 1*cm, Wy = 1*cm, WDistx = 0, WDisty = 0)
bd = beamdump.BeamDump()
thin = thinlens.ThinLens()
thick = thicklens.ThickLens()
mr = mirror.Mirror()

bd2 = beamdump.BeamDump(Center = [0., 10*cm, 0.], Norm = [0, -1, 0],\
			Name = 'BeamDumpX', Diameter = 5.*cm, Thickness = 1.*cm)
thin2 = thinlens.ThinLens(Focal = -25.*cm, KeepI = True, Diameter = 10.*cm,\
			Center = [20.*cm, 0.,0.])
thick2 = thicklens.ThickLens(K1 = -0.01, K2 = -0.01, Apex = [30.*cm , 0., 0.])

print bd2.isHit(bm)
print thin2.isHit(bm)
print thick2.isHit(bm)

print thin2.hit(bm, order = 2, threshold = -1.)
print thick2.hit(bm, order = 2, threshold = -1.)

