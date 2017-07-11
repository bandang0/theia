'''Module to demonstrate the optimization capabilities of theia.

In this module, we simulate a setup cmposed of two converging lenses in a 2F
configuration and vary the position of the second lens in order to find the
case where the output beam is the most collimated.

'''

#plotting stuff
import numpy as np
import matplotlib.pyplot as plt

#FreeCAD stuff
import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App
import Part

#theia stuff
from theia.helpers import settings
from theia.helpers.units import *
from theia.running import simulation
from theia.optics import thinlens, beam

# initialize globals (necessary to use theia in library form)
dic = {'info': False, 'warning': True, 'text': True, 'cad': True,
		'fname': 'optimization', 'fclib' : '/usr/local/lib/freecad/lib'}
settings.init(dic)

#simulation object
simu = simulation.Simulation(FName = 'optimization')
simu.LName = 'Optimizing with theia!'
simu.Order = 0
simu.Threshold = 0.5*mW

#optics, the first L1 lens doesn't move
L1 = thinlens.ThinLens(X = 0*cm, Y = 0., Z = 0., Focal = 20.*cm,
			Diameter = 3.*cm, Phi = 180.*deg, Ref = 'L1')

bm = beam.userGaussianBeam(1.*mm, 1.*mm, 0., 0, 1064*nm, 1*W,
							X = -30*cm, Phi = 0, Ref = 'Beam')

# this is a list of centers for the second lens we want to try (it is around
#70 cm = L1.X + 2*Focal to respect the 2F configuration). We're trying n
#configurations around L2.X = 50
n = 50
centers = [ 40.*cm + 2.*cm*(float(i)/n) for i in range(-n, n)]
waistSizes = []
waistPositions = []

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

	#save output data for plotting
	waistSizes.append(output.waistSize()[0])
	waistPositions.append(output.waistPos()[0])

simu.writeCAD()

#plot the results
plt.figure(1)
plt.subplot(211)
plt.plot(centers, waistSizes, 'r')
plt.ylabel('waists (m)')
plt.xlabel('center of second lens (m)')
plt.subplot(212)
plt.plot(centers, waistPositions, 'g')
plt.ylabel('positions (m)')
plt.xlabel('center of second lens (m)')
plt.show()
