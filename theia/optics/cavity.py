'''Defines the Cavity class for theia.'''

# Provides:
#   class Cavity

from units import *
from component import OpticalComponent

class Cavity(OpticalComponent):
    '''

    Cavity class.

    This class represents optical cavities, which are distict from mirros and
    lenses and declared as such. Essential the interaction of a cavity with a
    Gaussian beam is that the input beam is projected on the cavity mode beam,
    and the corresponding power inside the cavity is used to calculate the
    output beam power. The output beam has the cavity mode's characteristics.

    Cavitis also have the particularity of being verified for alignement by the
    simulation before running and the user is warned.

    *=== Attributes ===*


    *=== Methods ===*

    '''
