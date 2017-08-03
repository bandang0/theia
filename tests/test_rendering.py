'''Test the rendering module. This is not portable *at all*.'''

import sys

THEIAPATH = '/home/dev0/theia'    # path to access modules of theia
FREECADPATH = '/usr/lib/freecad/lib'	# and freecad
sys.path.insert(0, THEIAPATH)
sys.path.append(FREECADPATH)

import theia
from theia.helpers import settings
from theia.running import simulation
# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
        'fname': 'test_rendering', 'fclib': FREECADPATH, 'antiClip': True,
        'short': False}

settings.init(dic)

#simulation
simu = simulation.Simulation(dic['fname'])
simu.load()

#run
simu.run()

#write
simu.writeOut()
simu.writeCAD()
