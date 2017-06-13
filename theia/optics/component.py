'''Defines the SetupComponent class for theia.'''

# Provides:
#   class SetupComponent
#       __init__
#       __str__
#       lines
#       isHit

import numpy as np
from abc import ABCMeta, abstractmethod
from ..helpers.tools import formatter

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
    Name = "SetupComponent"

    def __init__(self, HRCenter, HRNorm, Ref, Thickness, Diameter):
        '''SetupComponent initializer.

        Parameters are the attributes of the object to construct.

        Returns a setupComponent.

        '''
        # allow empty initializer
        if Ref is None:
            Ref = "Set" + str(SetupComponent.SetupCount)
        # initialize data
        self.HRCenter = np.array(HRCenter, dtype = np.float64)
        self.HRNorm = np.array(HRNorm, dtype = np.float64)
        self.HRNorm = self.HRNorm/np.linalg.norm(self.HRNorm)
        self.Thick = Thickness
        self.Dia = Diameter
        self.Ref = Ref

        SetupComponent.SetupCount = SetupComponent.SetupCount + 1

    def __str__(self):
        '''String representation of the component, when calling print(object).

        '''
        return formatter(self.lines())

    @abstractmethod
    def lines(self):
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
