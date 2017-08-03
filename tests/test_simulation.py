'''Test the running module. This is not portable *at all*.'''

import sys

THEIAPATH = '/home/dev0/theia'    # path to access modules of theia
FREECADPATH = '/usr/lib/freecad/lib'	# and freecad
sys.path.insert(0, THEIAPATH)

import theia
from theia.helpers import settings, tools
from theia.helpers.units import *
from theia.optics import beam, beamdump, thinlens, thicklens, mirror
from theia.running import simulation

# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
        'fname': 'test_simulation', 'fclib': FREECADPATH, 'antiClip': True,
        'short': False}

settings.init(dic)


# Create simulation object:
simu = simulation.Simulation(FName = 'devTest')

# test functions
@tools.timer
def loader():
    simu.load()

@tools.timer
def runner():
    simu.run()

@tools.timer
def writer():
	simu.writeOut()

# load input data
loader()

# run simulation
runner()

# write out
writer()
