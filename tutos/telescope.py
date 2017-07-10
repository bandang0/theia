'''Tutorial to demonstrate theia.'''

import numpy as np
from theia.running import simulation as sim
from theia.optics import beam as gbeam
from theia.optics import mirror as mir
from theia.helpers import settings
from theia.helpers.units import *

# initialize globals (necessary to use theia in library form)
dic = {'info': False, 'warning': True, 'text': True, 'cad': True,
		'fname': 'telescope', 'fclib' : '/usr/local/lib/freecad/lib'}
settings.init(dic)

# Mirrors of telescope
alpha = np.pi/2. - np.arctan(.1)
beta = np.pi/2. + np.arctan(.1)
mirror1 = mir.Mirror(Thickness = 1*cm, Diameter = 5*cm, X = 1*m,
            Theta = alpha, Phi = 180.*deg, HRK = 0.90, ARK = 0, Wedge = 0, HRr = 0.90,
            HRt = 0.10, ARr = 0.10, ARt = .90, Ref = 'M1',
            N = 1.5)

mirror2 = mir.Mirror(Thickness = 1* cm, Diameter = 10*cm,
            Y = 20*cm, Theta = beta, Phi = 0., HRK = 0.90,
            ARK = 0, Wedge = 0, HRr = 0.90, HRt = 0.1, ARr = 0.1, ARt = 0.90,
            Ref = 'M2', N = 1.5)

#Input beam
beam1 = gbeam.userGaussianBeam(Wx = .5*cm, Wy = .5*cm, WDistx = 0, WDisty = 0,
             Ref = 'ORI')

# parameters
threshold = -1*W
order = 1
inBeams = [beam1]
optList = [mirror1, mirror2]

# Create simulation object:
simu = sim.Simulation(FName = 'telescope')
simu.OptList = optList
simu.InBeams = inBeams
simu.Order = order
simu.Threshold = threshold

# Run simulation. Output of this simulation is intended to be compared
# to the output of the telescope.f90 optocad simulation
simu.run()

if __name__ == "__main__":
    print(simu)
    print(simu.BeamTreeList[0].beamList())
