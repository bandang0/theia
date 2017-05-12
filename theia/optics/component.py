'''Defines the SetupComponent class for theia.'''

# Provides:
#   class SetupComponent
#       __init__
#       __str__
#       lineList
#       isHit

import numpy as np
from units import *
from abc import ABCMeta, abstractmethod
from helpers import formatter

class SetupComponent(object):
    '''

    SetupComponent class.

    This is an Abstract Base Class for all the components (optical or not) of
    the setup. Its methods may be implemented in daughter classes.

    *=== Attributes ===*
    SetupCount: class attribute, counts setup components. [integer]
    HRCenter: center of the principal face of the component in space.
        [3D vector]
    HRnorm: normal unitary vector the this principal face, supposed to point
        outside the media. [3D vector]
    Thick: thickness of the component, counted in opposite direction to
        HRNorm. [float]
    Dia: diameter of the component. [float]
    Name: name of the component. [string]
    Ref: reference string (for keeping track with the lab). [string]


    '''

    __metaclass__ = ABCMeta
    SetupCount = 0   #counts the setup components

    def __init__(self, HRCenter = [0., 0., 0.], HRNorm = [-1., 0., 0.],
                Name = None, Ref = None, Thickness = 2.*cm, Diameter = 10*cm):
        '''SetupComponent constructor.

        Parameters are the attributes of the object to construct.

        Returns a setupComponent.

        '''
        # initialize data
        self.HRCenter = np.array(HRCenter, dtype = np.float64)
        self.HRNorm = np.array(HRNorm, dtype = np.float64)
        self.HRNorm = self.HRNorm/np.linalg.norm(self.HRNorm)
        self.Thick = float(Thickness)
        self.Dia = float(Diameter)

        #initialize setup name and ref
        if Name is not None:
            self.Name = Name
        else:
            self.Name = "Setup"

        if Ref is not None:
            self.Ref = Ref
        else:
            self.Ref = "Set" + str(self.__class__.SetupCount)

        self.__class__.SetupCount = self.__class__.SetupCount + 1

    def __str__(self):
        '''String representation of the component, when calling print(object).

        '''
        return formatter(self.lineList())

    @abstractmethod
    def lineList(self):
        '''Method to return the list of strings to __str__.

        Abstract (pure virtual) method.

        '''
        pass

    @abstractmethod
    def isHit(self, beam):
        '''Method to determine if component is hit by a beam.

        Abstract (pure virtual) method.

        '''
        pass
