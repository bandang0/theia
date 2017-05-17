'''Test the simulation module.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)

import numpy as np
from helpers import settings
from helpers.units import *
from helpers.tools import timer
from simulation import simulation as sim
from optics import beam, beamdump, thicklens, thinlens, mirror


# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
		'fname': 'test_optics'}

settings.init(dic)

# Create optical objects
mirror1 = mirror.Mirror(Thickness = 1*cm, Diameter = 1*m, 
			HRCenter = [1*m,0, 0], Theta = np.pi/2., Phi = np.pi,
            HRK = 0.0, ARK = 0, Wedge = 0, HRr = 0.90,
            HRt = 0.10, ARr = 0.10, ARt = .90, Name = 'Mirror1', Ref = 'M1')
print mirror1.HRNorm
#mirror2 = mirror.Mirror(Thickness = 1* cm, Diameter = 5*cm,
#            HRCenter = [0.*cm, 20*cm, 0], HRK = 0.90,
#            ARK = 0, Wedge = 0, HRr = 0.90, HRt = 0.1, ARr = 0.1, ARt = 0.90,
#            Name = 'Mirror2', Ref = 'M2')


lens = thinlens.ThinLens(Focal = 10*cm, Diameter = 15*cm, Center = [2., 0,0.],
		Ref = 'len', Norm = [-1., 0., 0.])

print lens.HRNorm
print lens.ARNorm
print lens.HRK
print lens.ARK
print lens.HRCenter
print lens.ARCenter

# beams
beam1 = beam.GaussianBeam(Wx = .5*cm, Wy = .5*cm, WDistx = 0, WDisty = 0,
            ortho = True, Pos = [0,0,0], Dir = [1., 0., 0.], Ref = 'ORI')



inBeams = [beam1]
optList = [mirror1, lens]

# parameters
threshold = -0.5*mW
order = 2

# Create simulation object:
simu = sim.Simulation(FName = 'test', LName = 'Test')


# test functions
@timer
def loader():
    simu.load(inBeams, optList)

@timer
def runner(order):
    simu.run(threshold, order)



# load input data
loader()

# run simulation
runner(order)

print simu.BeamTreeList[0].beamList()
print(simu)

