'''Defines the BeamDump class for theia.'''

# Provides:
#   class BeamDump

import numpy as np
#from units import *
from component import OpticalComponent
from optics import geometry as geo
from optics import beam as gbeam
import helpers
from helpers import formatter

class BeamDump(OpticalComponent):
    '''

    BeamDump class.

    This class represents components on which rays stop.

    *=== Attributes ===*
    OptCount (inherited): class attribute, counts all optics created. [integer]
    '''

    def __init__(self, Diameter, Center = [0., 0., 0.], Norm = [1., 0., 0.],
                Name = None, Ref = None):
        '''BeamDump constructor.

        Parameters are the attributes.

        Returns a BeamDump.

        '''
        super(Mirror, self).__init__(Name, Ref)
        self.Dia = float(Diameter)
        self.Norm = np.array(Norm, dtype = float64)
        self.Norm = self.Norm/np.linalg.norm(self.Norm)
        self.Center = np.array(Center, dtype = float64)
