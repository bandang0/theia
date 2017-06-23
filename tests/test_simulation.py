'''Test the running module. This is not portable *at all*.'''

import sys

THEIAPATH = '/home/dev0/theia'    # path to access modules of theia
FREECADPATH = '/usr/lib/freecad/lib'	# and freecad
sys.path.insert(0, THEIAPATH)

import theia
from theia.helpers import settings
from theia.helpers.units import *
from theia.optics import beam, beamdump, thinlens, thicklens, mirror

# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
        'fname': 'test_optics', 'fclib': FREECADPATH}

settings.init(dic)


# Create simulation object:
simu = simulation.Simulation(FName = 'devTest')

# test functions
@timer
def loader():
    simu.load()

@timer
def runner():
    simu.run()

@timer
def writer():
	simu.writeOut()

# load input data
loader()

# run simulation
runner()

# write out
writer()
