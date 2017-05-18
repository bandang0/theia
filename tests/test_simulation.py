'''Test the simulation module.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)

import numpy as np
from helpers import settings
from helpers.units import *
from helpers.tools import timer
from helpers.interaction import welcomeString
from running import simulation
from optics import beam, beamdump, thicklens, thinlens, mirror


# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
		'fname': 'test_optics'}

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



# load input data
loader()

# run simulation
runner()



