'''This is a first example of use of theia.'''

import numpy as np
from theia.running import simulation as sim
from theia.optics import beam as gbeam
from theia.optics import mirror as mir
from theia.helpers import settings
from theia.helpers.units import *

# initialize globals (necessary to use theia in library form)
dic = {'info': False, 'warning': True, 'text': True, 'cad': True,
		'fname': 'test_optics'}
settings.init(dic)

# Here is a spherical mirror
mirror1 = mir.Mirror(Thickness = 2*m, Diameter = 2*m, Phi = 180.*deg,
            X = 0, HRK = 1, ARK = 0, Wedge = 0, HRr = 1.0,
            HRt = 0.00, ARr = 0.10, ARt = .90, Name = 'Semi-sphere', Ref = 'M1')

# Here are some beams which all depart from the focus of the semi-spherical
# mirror
beams = []
for i in range(-3, 3):
	for j in range(-3, 3):
		beams.append(gbeam.userGaussianBeam(Wx = 0.001, Wy = 0.001,
					Theta = np.pi/2. + i * np.pi/7.,
					Phi = j * np.pi/7., X = 0.5))
# Create simulation object:
simu = sim.Simulation(FName = 'sphere')
simu.LName = 'An Important Property of Spherical Mirrors'

# Load the initial data of the simulation
simu.InBeams = beams
simu.OptList = [mirror1]
simu.Order = 0
simu.Threshold = .5*W

# run the simulation
simu.run()

# observe that all the reflected beams point to infinity
if __name__ == "__main__":
    print "Direction of reflected beams:"
    for k in range(len(simu.BeamTreeList)):
        print(simu.BeamTreeList[k].R.Root.Dir)
