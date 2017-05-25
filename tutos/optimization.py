'''Module to demonstrate the optimization capabilities of theia.

In this module, we simulate a setup cmposed of two converging lenses in a 2F
configuration and vary the position of the second lens in order to find the
case where the output beam is the most collimated.

'''

import numpy as np
from theia.helpers import settings
from theia.helpers.units import *
from theia.running import simulation
from theia.optics import thinlens, beam

# initialize globals (necessary to use theia in library form)
dic = {'info': False, 'warning': True, 'text': True, 'cad': True,
		'fname': 'test_optics'}
settings.init(dic)

#simulation object
simu = simulation.Simulation(FName = 'optimization')
simu.LName = 'Optimizing with theia!'
simu.Order = 0
simu.Threshold = 0.5*mW

#optics, the first L1 lens doesn't move
L1 = thinlens.ThinLens(X = 30*cm, Y = 0., Z = 0., Focal = 20.*cm,
			Diameter = 3.*cm, Phi = 180.*deg, Ref = 'L1')

bm = beam.GaussianBeam(100.*km, 100.*km, 0., 0, 1064*nm, 1*W, Phi = 0, Ref = 'Beam')

# this is a list of centers for the second lens we want to try (it is around
#70 cm = L1.X + 2*Focal to respect the 2F configuration). We're trying n
#configurations around L2.X = 50
n = 10
centers = [ 70.*cm + 2.*cm*(float(i)/n) for i in range(-n, n)]

# load beam
simu.InBeams = [bm]

#run the simulations in sequence!
for center in centers:
	print 'Running with center = ' + str(center/cm) + 'cm.'
	dic = {'X': center, 'Y': 0., 'Z': 0., 'Focal': 20.*cm,
		'Diameter': 3.*cm, 'Theta': 90*deg, 'Phi': 180.*deg, 'Ref': 'L2'}
	simu.OptList = [L1, thinlens.ThinLens(**dic)]

	#go theia go!
	simu.run()
	output = simu.BeamTreeList[0].T.T.T.T.Root
	print 'Results of the output beam waist (after two lenses):'
	print '\tPosition: '+str(output.waistPos()) + 'm'
	print '\tSize: ('+str(output.waistSize()[0]/mm)\
			+ ', ' + str(output.waistSize()[1]/mm)\
            + ')mm'
