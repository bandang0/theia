'''Test the simulation module.'''

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


# Create optical objects

#(self, thickness, diameter, HRCenter =  [0., 0., 0.],
#            HRNorm = [1., 0., 0.], HRK = 0., ARK = 0., Wedge = 0.,
#            Alpha = 0., HRr = 1., HRt = 0., ARr = 0., ARt = 1., N = 1.4585,
#            Name = None, Ref = None, KeepI = True):

#(self, Wx = None, Wy = None, WDistx = None, WDisty = None,
#    Q = None, ortho = True, N = 1.,
#    Wl = 1064.*nm, P = 1*W, Pos = [0., 0., 0.], Dir = [1., 0., 0.],
#    Ux = [0., -1., 0.], Uy = None, Name = None, OptDist = 0.*m,
#    Length = 0.*m, StrayOrder = 0):

mirror1 = mir.Mirror(thickness = 1*cm, diameter = 5*cm, HRCenter = [1*m,0, 0],
            HRNorm = [-1, .10, 0], HRK = 0.90, ARK = 0, Wedge = 0, HRr = 0.90,
            HRt = 0.10, ARr = 0.10, ARt = .90, Name = 'Mirror1', Ref = 'M1',
            ARNorm = [1, -0, 0])

mirror2 = mir.Mirror(thickness = 1* cm, diameter = 5*cm,
            HRCenter = [0.*cm, 20*cm, 0], HRNorm = [1, -.1, 0.], HRK = 0.90,
            ARK = 0, Wedge = 0, HRr = 0.90, HRt = 0.1, ARr = 0.1, ARt = 0.90,
            Name = 'Mirror2', Ref = 'M2', ARNorm = [-1, .1, 0])


beam1 = gbeam.GaussianBeam(Wx = .5*cm, Wy = .5*cm, WDistx = 0, WDisty = 0,
            ortho = True, Pos = [0,0,0], Ref = 'ORI')

inBeam = [beam1]
optList = [mirror1, mirror2]

# parameters
threshold = 0.5*mW
order = 2

# Create simulation object:
simu = sim.Simulation(FName = 'test', LName = 'Test')


# test functions
@timer
def loader():
    simu.load(inBeam, optList)

@timer
def runner():
    simu.run(threshold, order)



# load input data
loader()

# run simulation
runner()



print simu.BeamTreeList[0].beamList()
print(simu)
