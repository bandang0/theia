'''Defines the Simulation class for theia.'''

# Provides:
#   class Simulation

from units import *
import helpers
from helpers import formatter
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
        self.BeamTreeList = []

    def __str__(self):
        '''String representation of the simulation, for print(simulation).

        '''
        sList = ["Simulation: " + str(self.LName) + " (" + str(self.FName)\
                 + ") {"]
        sList.append("OptList: {")
        for opt in self.OptList:
            sList = sList + opt.lineList()
        sList.append("}")
        sList.append("InBeams: {")
        for beam in self.InBeams:
            sList = sList + beam.lineList()
        sList.append("}")
        sList.append("BeamTrees: {")
        for tree in self.BeamTreeList:
            sList = sList + tree.lineList()
        sList.append("}")
        sList.append("}")

        return formatter(sList)


    def load(self, InBeams, OptList):
        '''Initialize simulation attributes by input from .tia file.

        No return value.

        '''

        self.InBeams = InBeams
        self.OptList = OptList

    def run(self, threshold = -1*mW, order = np.Inf, write3D = True):
        '''Run simulation with input as read by load.

        *=== Arguments ===*
        threshold: power of beam below which the simulation stops tracing child
                    beams
        write3D: whether or not to write to the .fcstd file for FreeCAD
                    rendering

        No return value.
        '''

        BeamTreeList = []

        for k in range(len(self.InBeams)):
            BeamTreeList.append(beamtree.treeOfBeam(self.InBeams[k],
            self.OptList, order, threshold ))


        self.BeamTreeList = BeamTreeList
