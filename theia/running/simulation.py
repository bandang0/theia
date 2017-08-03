'''Defines the Simulation class for theia.'''

# Provides:
#   class Simulation
#       __init__
#       __str__
#       numberOfOptics
#       load
#       run
#       writeOut
#       writeCAD

import numpy as np
from time import strftime
from ..__init__ import __version__
from ..helpers import settings
from ..helpers.units import mW
from ..helpers.tools import formatter, shortRef
from ..optics.optic import Optic
from ..optics.beam import userGaussianBeam
from ..optics.beamdump import BeamDump
from ..optics.thinlens import ThinLens
from ..optics.thicklens import ThickLens
from ..optics.mirror import Mirror
from ..optics.ghost import Ghost
from ..tree import beamtree
from . import parser

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
    BeamTreeList: list of binary trees of beams [list of BeamTree]
    Order: order of the simulation, beams transmitted by HRs or reflected by ARs
        have their orders augmented by 1, and simulation calculates only until
        this Order attribute. [int]
    Threshold: Power under which beams are no longer traced. [float]
    Date: string of the date-time when the simulation was created (not run).
        [string]

    '''

    def __init__(self, FName = 'simulationinput'):
        '''Simulation initializer.

        FName: output files name without extension. [string]

        '''

        self.LName = 'Simulation'
        self.FName = FName
        self.OptList = []
        self.InBeams = []
        self.BeamTreeList = []
        self.Order = np.inf
        self.Threshold = -1.*mW
        self.Date = strftime("%c")

    def __str__(self):
        '''String representation of the simulation, for print(simulation).'''
        sList = ["Simulation: %s (%s.*) {" %(str(self.LName), str(self.FName))]
        sList.append("OptList: {")
        for opt in self.OptList:
            sList = sList + opt.lines()
        sList.append("}")
        sList.append("InBeams: {")
        for beam in self.InBeams:
            sList = sList + beam.lines()
        sList.append("}")
        sList.append("BeamTrees: {")
        for tree in self.BeamTreeList:
            sList = sList + tree.lines()
        sList.append("}")
        sList.append("}")

        return formatter(sList)

    def numberOfOptics(self):
        '''Calculate the number of optics of OptList.

        Returns the number of optics (not components, optics).

        '''
        n = 0
        for obj in self.OptList:
            if isinstance(obj, Optic):
                    n = obj.OptCount
                    break
        return n

    def load(self):
        '''Initialize simulation attributes by input from .tia file.

        See documantation for the format of the input file.

        No return value.

        '''
        finalList = parser.readIn(settings.fname + '.tia')

        # default dictionary for translation
        translateDic = {'X': 0., 'Y': 0., 'Z': 0.}

        # populate simulation attributes with objects from input
        for uple in finalList:
            if uple[0] == 'bo':
                #update translation dic
                translateDic = uple[1]
            elif uple[0] == 'LName':
                self.LName = uple[1]
            elif uple[0] == 'order':
                self.Order = uple[1]
            elif uple[0] == 'threshold':
                self.Threshold = uple[1]
            elif uple[0] ==  'bm':
                self.InBeams.append(userGaussianBeam(**uple[1]))
                #translate last read object
                self.InBeams[len(self.InBeams)-1].translate(**translateDic)
            elif uple[0] == 'mr':
                self.OptList.append(Mirror(**uple[1]))
                self.OptList[len(self.OptList)-1].translate(**translateDic)
            elif uple[0] == 'th':
                self.OptList.append(ThinLens(**uple[1]))
                self.OptList[len(self.OptList)-1].translate(**translateDic)
            elif uple[0] == 'tk':
                self.OptList.append(ThickLens(**uple[1]))
                self.OptList[len(self.OptList)-1].translate(**translateDic)
            elif uple[0] == 'bd':
                self.OptList.append(BeamDump(**uple[1]))
                self.OptList[len(self.OptList)-1].translate(**translateDic)
            elif uple[0] == 'gh':
                self.OptList.append(Ghost(**uple[1]))
                self.OptList[len(self.OptList)-1].translate(**translateDic)

    def run(self):
        '''Run simulation with input as read by load.

        threshold: power of beam below which the simulation stops tracing child
                    beams. [float]
        order: maximum order to keep daughter beams. [integer]

        No return value.
        '''
        #warn if threshold is negative or order is inf
        if settings.warning and self.Threshold < 0.:
            print "theia: Warning: Running simulation with negative threshold,"\
            + " termination not guaranteed."

        if settings.warning and self.Order is np.inf:
            print "theia: Warning: Running simulation with infinite order,"\
            + " termination not guaranteed."

        # reinitialize treeList
        self.BeamTreeList = []

        for k in range(len(self.InBeams)):
            self.BeamTreeList.append(beamtree.treeOfBeam(self.InBeams[k],
            self.OptList, self.Order, self.Threshold ))

    def writeOut(self):
        '''Write the results from the simulation in the .out file.'''
        outList = []
        outList.append("######## theia output file for simulation: ########")
        outList.append("\t\t\t %s\n" %self.LName)
        outList.append('#'*10 + " META DATA " + '#'*10)
        outList.append("Generated at: %s" %strftime("%c"))
        outList.append("theia version: %s" %__version__)
        outList.append("Options: {")
        outList.append("Input file: %s.tia" %self.FName)
        outList.append("Anti-clipping: %s" %str(settings.antiClip))
        outList.append("Short output: %s" %str(settings.short))
        outList.append("}\n")

        outList.append('#' *10 + ' SIMULATION DATA ' + '#' * 10)
        outList.append("Simulation Order: %s" %str(self.Order) )
        outList.append("Simulation Threshold: %smW" %str(self.Threshold/mW))
        outList.append("Number of Components: %s" %str(len(self.OptList)))
        outList.append("Number of Optics: %s\n" %str(self.numberOfOptics()))
        outList.append("Simulation: %s (%s.*) {" %(self.LName, self.FName))
        outList.append("Components: {")

        for opt in self.OptList:
            outList.append("%s (%s) %s" %(opt.Name, opt.Ref, str(opt.HRCenter)))
        outList.append("}")
        outList.append("BeamTrees: {")

        for tree in self.BeamTreeList:
            outList = outList + tree.lines()

        outList.append("}")
        outList.append("}\n")

        outList.append('#' * 10 + " BEAM LISTING " + '#' * 10)
        for tree in self.BeamTreeList:
            outList.append("Tree: Root beam = %s {" % (tree.Root.Ref\
                if not settings.short else shortRef(tree.Root.Ref)))
            outList = outList + tree.outputLines()
            outList.append("}")

        with open(settings.fname + '.out', 'w') as outF:
            outF.write(formatter(outList))

    def writeCAD(self):
        '''Write the CAD .fcstd file by calling rendering functions.'''

        # these two following import statements are here because they require
        # that the PYTHONPATH be updated, and thus they are not
        # at the beginning of the module, which is read at the very beginning
        # of main.
        import FreeCAD as App
        from ..rendering.writer import writeToCAD

        #New fcstd document
        App.newDocument(self.FName)
        App.setActiveDocument(self.FName)
        doc = App.ActiveDocument

        #write all optics
        for opt in self.OptList:
            writeToCAD(opt, doc)

        # write beams recursively
        for tree in self.BeamTreeList:
            writeToCAD(tree, doc)

        #Wrap up
        doc.recompute()
        doc.saveAs(settings.fname + '.fcstd')
