'''This is a second example of use of theia.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)

import simulation
import optics
import tree

from simulation import simulation as sim
from optics import beam as gbeam
from optics import mirror as mir
from tree import beamtree
from helpers import timer
from units import *

# Apex of the surface
A = np.array([0.1,0.,0.], dtype = np.float64)
theta = 0.52359877
HRNorm = np.array([-1, .1, 0.], dtype = np.float64)
HRCenter = A + 0.1*(1-np.cos(theta))*HRNorm

# Here is a spherical mirror
mirror1 = mir.Mirror(thickness = 2*cm, diameter = 10*cm, HRCenter = [.1, 0.,0.],
            HRNorm = [-1, 0, 0.], HRK = 10., ARK = 0, Wedge = 0, HRr = .9,
            HRt = 0.10, ARr = 0.10, ARt = .90, Name = 'Mirror', Ref = 'M1',
            ARNorm = [1.,0.,0.])

# Here are ghost surfaces
bd1 = mir.Mirror(thickness = 2*cm, diameter = 5*cm,
            HRCenter = [0., 2., 0],
            HRNorm = [1., -.2, 0.], HRK = 0., ARK = 0., Wedge = 0., HRr = 0.,
            HRt = 1., ARr = 0., ARt = 1.0, Name = 'Ghost1', Ref = 'G1',
            N = 1.0)

bd2 = mir.Mirror(thickness = 2*cm, diameter = 5*cm, HRCenter = [.3, .0, 0.],
            HRNorm = [-1.,0., 0.], HRK = 0., ARK = 0., Wedge = 0., HRr = 0.,
            HRt = 1., ARr = 0., ARt = 1.0, Name = 'Ghost2', Ref = 'G2',
            N = 1.)

#The beam
beam1 = gbeam.GaussianBeam(Wx = .1*cm, Wy = .1*cm,
					ortho = True, Dir = [1., 0., 0.], WDistx = 0., WDisty = 0.,
					Pos = [0., 0., 0.])
# Create simulation object:
simu = sim.Simulation(FName = 'vignale',
		LName = 'Beam at the center of curvature')

# Load the initial data of the simulation
simu.load([beam1], [mirror1, bd1, bd2])

# run the simulation
simu.run(threshold = 5.*mW, order = 2)

if __name__ == "__main__":
    print(simu)
    print(simu.BeamTreeList[0].beamList())
