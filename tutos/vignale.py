'''This is a second example of use of theia as a library.'''

import numpy as np
from theia.running import simulation as sim
from theia.optics import beam as gbeam
from theia.optics import mirror as mir
from theia.optics import thicklens as tk
from theia.helpers import settings
from theia.helpers.units import *

# initialize globals (necessary to use theia in library form)
dic = {'info': False, 'warning': True, 'text': True, 'cad': True,
		'fname': 'vignale', 'fclib' : '/usr/local/lib/freecad/lib'}
settings.init(dic)

# Here is a spherical mirror
mirror1 = mir.Mirror(Thickness = 2, Diameter = 10*cm, X = 1.,
            Theta = np.pi/2. - np.arctan(.1), Phi = 180.*deg,
            HRK = 10., ARK = 0, Wedge = 0, HRr = .9,
            HRt = 0.10, ARr = 0.10, ARt = .90, Ref = 'M1')

# Here are ghost surfaces
bd1 = tk.ThickLens(Thickness = 0.1*cm, Diameter = 5*cm, Theta = 101.5*deg,
            Phi = 0., X = 0., Z = .2, K1 = 0., K2 = 0., Ref = 'G1', N = 1.0)

bd2 = tk.ThickLens(Thickness = 0.1*cm, Diameter = 5*cm, X = 5.,
            Phi = 180.*deg, K1 = 0., K2 = 0., R = 0, T = 1, N = 1., Ref = 'G2')

# The beam
beam1 = gbeam.userGaussianBeam(Wx = .1*cm, Wy = .1*cm, Theta = 90.*deg,
					Phi = 0., WDistx = 0., WDisty = 0.)

# Create simulation object:
simu = sim.Simulation(FName = 'vignale')

# Load the initial data of the simulation
simu.InBeams = [beam1]
simu.OptList = [mirror1, bd1, bd2]
simu.Order = 0
simu.Threshold = .5*mW

# run the simulation
simu.run()
simu.writeOut()

if __name__ == "__main__":
    print(simu)
    print(simu.BeamTreeList[0].beamList())
