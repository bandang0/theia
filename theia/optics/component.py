'''Defines the OpticalComponent class for theia.'''

# Provides:
#   class OpticalComponent

#from units import *

class OpticalComponent(object):
    '''

    OpticalComponent class.


    *=== Attributes ===*
    OptCount: class attribute, counts optics. [integer]
    Name: name of the optics. [string]
    Ref: reference string (for keeping track with the lab). [string]

    *=== Methods ===*

    '''
    OptCount = 0   #counts the optical components

    def __init__(self, Name = None,
                Ref = None):
        '''OpticalComponent constructor.

        Parameters are the attributes of the object to construct.

        Returns an OpticalComponent.

        '''
        if Name is not None:
            self.Name = Name
        else:
            self.Name = "Optics"

        if Ref is not None:
            self.Ref = Ref
        else:
            self.Ref = "Opt" + str(self.__class__.OptCount)

        self.__class__.count = self.__class__.OptCount + 1
