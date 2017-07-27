'''Test the geometry of the rendering module. This is not portable *at all*.'''

import sys

THEIAPATH = '/home/dev0/theia'    # path to access modules of theia
FREECADPATH = '/usr/lib/freecad/lib'	# and freecad
sys.path.insert(0, THEIAPATH)
sys.path.append(FREECADPATH)

import theia
from theia.helpers import settings
from theia.running import simulation
from theia.optics import beam, mirror
from theia.helpers.units import *

# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
        'fname': 'test_geometry', 'fclib': FREECADPATH, 'antiClip': True}

settings.init(dic)

#beam
TBeam = beam.userGaussianBeam(Wx = .5*cm, Wy = .2*cm, WDistx = 50.,
                                        WDisty = 20., Alpha = 0.*deg)
#simulation
simu = simulation.Simulation(dic['fname'])
simu.Threshold = 0.5*uW
simu.Order = 0
simu.InBeams = [TBeam]
simu.OptList = [mirror.Mirror(X = 12.*m, Theta = 45*deg, Phi = pi, HRK = 0, HRr = 0.1, HRt = 0.1)]
#inspect beam data
print TBeam.QParam()
print TBeam.U[0]
print TBeam.U[1]

#run
simu.run()

#write
simu.writeOut()
simu.writeCAD()
