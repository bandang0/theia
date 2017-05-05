'''This is a first example of use of theia.'''

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

# Here is a spherical mirror
mirror1 = mir.Mirror(thickness = 2*m, diameter = 2*m, HRCenter = [0,0, 0],
            HRNorm = [-1, 0,0], HRK = 1, ARK = 0, Wedge = 0, HRr = 1.0,
            HRt = 0.00, ARr = 0.10, ARt = .90, Name = 'Semi-sphere', Ref = 'M1')

# Here are some beams which all depart from the focus of the semi-spherical
# mirror
beams = []
for i in range(-3, 3):
	for j in range(-3, 3):
		beams.append(gbeam.GaussianBeam(Wx = .5*cm, Wy = .5*cm, 
					ortho = True, Dir = [1., i/4., j/4.],
					Pos = [0.5, 0., 0.]))
# Create simulation object:
simu = sim.Simulation(FName = 'sphere', 
		LName = 'An Important Property of Spherical Mirrors')

# Load the initial data of the simulation
simu.load(beams, [mirror1])

# run the simulation
simu.run(threshold = 5.*mW, order = 2)

# observe that all the reflected beams are parallel! 

for k in range(len(simu.BeamTreeList)):
	print(simu.BeamTreeList[k].R.Root.Dir)


