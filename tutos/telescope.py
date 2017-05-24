'''Tutorial to demonstrate theia.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)

import simulation
import optics
import tree
from units import *

from simulation import simulation as sim
from optics import beam as gbeam
from optics import mirror as mir
from helpers import timer
from tree import beamtree

# Mirrors of telescope
mirror1 = mir.Mirror(thickness = 1*cm, diameter = 5*cm, HRCenter = [1*m,0, 0],
            HRNorm = [-1, .10, 0.], HRK = 0.90, ARK = 0, Wedge = 0, HRr = 0.90,
            HRt = 0.10, ARr = 0.10, ARt = .90, Name = 'Mirror1', Ref = 'M1',
            N = 1.5)

mirror2 = mir.Mirror(thickness = 1* cm, diameter = 10*cm,
            HRCenter = [0.*cm, 20*cm, 0], HRNorm = [1, -.1, 0.], HRK = 0.90,
            ARK = 0, Wedge = 0, HRr = 0.90, HRt = 0.1, ARr = 0.1, ARt = 0.90,
            Name = 'Mirror2', Ref = 'M2', N = 1.5)

#Input beam
beam1 = gbeam.GaussianBeam(Wx = .5*cm, Wy = .5*cm, WDistx = 0, WDisty = 0,
            ortho = True, Pos = [0,0,0], Ref = 'ORI')

inBeams = [beam1]
optList = [mirror1, mirror2]

# parameters
threshold = -1*W
order = 1

# Create simulation object:
simu = sim.Simulation(FName = 'telescope', LName = 'Telescope')

# load and run simulation. Output of this simulation is intended to be compared
# to the output of the telescope.f90 optocad simulation
simu.load(inBeams, optList)
simu.run(threshold, order)
if __name__ == "__main__":
    print(simu)
    print(simu.BeamTreeList[0].beamList())
