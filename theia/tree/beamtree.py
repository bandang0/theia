'''Defines the BeamTree class for theia.'''

# Provides:
#   class OpticalComponent

from units import *
from node import Node

class BeamTree(object):
    '''

    BeamTree class.

    A BeamTree is a binary tree which allows to keep track of the beams as they
    are traced throughout the optical setup. A node of this tree has a beam and
    the next beams are the children of this beam by transmission or reflection
    on surfaces of components.

    *=== Attributes ===*
    Root: beam of this node of the tree. [GaussianBeam]
    Trans: beam resulting from the transmission of the Root beam. [GaussianBeam]
    Refl: beam resulting from the reflection of the Root beam. [GaussianBeam]
    Parent: beam which has given Root beam by interaction with an optical
        component. [GaussianBeam]
    Surf: Surface where the Root beam gave rise to the Trans and Refl beams.
    [tuple (OpticalComponent, string), string is 'HR' or 'AR']

    *=== Methods ===*

    '''

    def __init__(self, Root = None, Parent = None):
        '''BeamTree constructor.'''
        self.Root = Root
        self.Trans = None
        self.Refl = None
        self.Parent = None
        self.Surf = None
