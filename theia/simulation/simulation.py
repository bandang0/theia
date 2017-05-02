'''Defines the Simulation class for theia.'''

# Provides:
#   class Simulation

from units import *
from tree import beamtree
class Simulation(object):
    '''

    Simulation class.

    This class is a wrapper for all the metadata (names of setup and of files,
    etc.) as well as for the high level functions of a simulation.

    *=== Attributes ===*
    LName: name of the simulation [string]
    FName: name of the file for outputs (without extension) [string]
    OptList: list of optical components of the setup [list of optics]
    InBeams: list of input beams [list of beams]
    BeamTree: binary tree of beams [Beam Tree from tree package]

    *=== Methods ===*


    '''

    def __init__(self, LName, FName):
        '''Simulation constructor.

        LName: simulation name. [string]
        Fname: output files name without extension. [string]
        '''

        self.LName = LName
        self.FName = FName
        self.OptList = []
        self.InBeams = []
        self.BeamTree = beamtree.BeamTree()

    def load(self):
        '''Initialize simulation attributes by input from .tia file.'''

    def run(self, threshold = 1*W, write3D = True):
        '''Run simulation with input as read by load.

        *=== Arguments ===*
        threshold: power of beam below which the simulation stops tracing child
                    beams
        write3D: whether or not to write to the .fcstd file for FreeCAD
                    rendering
        *=== Returns a integer exit code according to success of simulation ===*
        '''
