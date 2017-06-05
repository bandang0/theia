'''Defines the BeamTree class for theia.'''

# Provides:
#   class OpticalComponent
#       __init__
#       __str__
#       lines
#       beamList
#       beamLines
#       numberOfBeams
#       outputLines
#   treeOfBeam

from ..helpers import settings
from ..helpers.units import *
from ..helpers.tools import formatter
from ..helpers.geometry import rectToSph

class BeamTree(object):
    '''

    BeamTree class.

    A BeamTree is a binary tree which allows to keep track of the beams as they
    are traced throughout the optical setup. The Root of the tree is a Gaussian
    beam and the other attributes are the daughter trees and all the data of the
    interaction producing these with the Root beam

    *=== Attributes ===*
    Root: beam of this node of the tree. [GaussianBeam]
    T: beam resulting from the transmission of the Root beam. [BeamTree]
    R: beam resulting from the reflection of the Root beam. [BeamTree]

    '''

    def __init__(self, Root = None,
                T = None, R = None):
        '''BeamTree initializer.'''
        self.Root = Root
        self.T = T
        self.R = R

    def __str__(self):
        '''String representation of a BeamTree, for print(tree).

        '''
        return formatter(self.lines())

    def lines(self):
        '''Returns the list of lines necessary to print the object.

        '''
        ans = []
        ans.append("Tree: {")
        ans.append("Root beam: " + str(self.Root.Name))
        ans.append("Number of beams: " + str(self.numberOfBeams()))
        ans.append("}")

        return ans

    def beamList(self):
        '''Returns the string representation the tree of beams.

        '''
        before = ["Tree: Root beam = " + str(self.Root.Name) + " {"]
        after = ["}"]
        return formatter(before + self.beamLines() + after)

    def beamLines(self):
        '''Returns the list of lines necessary to print the list of beams.

        '''
        ans = []
        if self.Root is not None:
            ans = self.Root.lines()
            if self.R is not None:
                ans = ans + self.R.beamLines()
            if self.T is not None:
                ans = ans + self.T.beamLines()

        return ans

    def numberOfBeams(self):
        '''Return the total number of beams.'''
        if self.Root is None:
            return 0

        if self.T is None and self.R is None:
            return 1
        elif self.T is None and self.R is not None:
            return 1 + self.R.numberOfBeams()
        elif self.T is not None and self.R is None:
            return 1 + self.T.numberOfBeams()
        else:
            return 1 + self.T.numberOfBeams() + self.R.numberOfBeams()

    def outputLines(self):
        '''Return the list of lines necessary to write the output of simulation.

        '''
        sList = []
        if self.Root is not None:
            if self.Root.Optic is not None:
                if self.Root.Length > 0.:
                    if self.R is not None and self.R.Root is not None:
                        sList = ['(' + self.Root.Optic + ', ' + self.Root.Face \
                        + ') ' + str(self.Root.Length)\
                        + 'm (' + self.R.Root.Optic + ', '\
                        + self.R.Root.Face + ') ' + self.Root.Ref + ' {']
                    elif self.T is not None and self.T.Root is not None:
                        sList = ['(' + self.Root.Optic + ', '+ self.Root.Face \
                        + ') ' + str(self.Root.Length) \
                        + 'm (' + self.T.Root.Optic + ', '+ self.T.Root.Face \
                        + ') ' + self.Root.Ref + ' {']
                    else:
                        sList = ['(' + self.Root.Optic \
                        + ', ' +self.Root.Face + ') ' + str(self.Root.Length) \
                        + 'm [End] ' + self.Root.Ref + ' {']
                else:
                    sList = ['(' + self.Root.Optic + ', ' +self.Root.Face \
                    + ') [Open] ' + self.Root.Ref + ' {']
            else:
                if self.Root.Length > 0.:
                    if self.R is not None and self.R.Root is not None:
                        sList = ['[InBeam] ' + str(self.Root.Length) \
                        + 'm (' + self.R.Root.Optic + ', '+ self.R.Root.Face \
                        + ') ' + self.Root.Ref + ' {']
                    elif self.T is not None and self.T.Root is not None:
                        sList = ['[InBeam] ' + str(self.Root.Length) \
                        + 'm (' + self.T.Root.Optic + ', '+ self.T.Root.Face \
                        + ') ' + self.Root.Ref + ' {']
                    else:
                        sList = ['[InBeam] ' + str(self.Root.Length)\
                        + 'm [End] ' + self.Root.Ref + ' {']
                else:
                    sList = ['[InBeam] [Open] ' + self.Root.Ref + ' {']
            sList.append("Waist Pos: " + str(self.Root.waistPos()) + 'm')
            sList.append("Waist Size: (" \
                + str(self.Root.waistSize()[0]/mm) + ', ' \
                + str(self.Root.waistSize()[1]/mm)\
                + ')mm')
            sph = rectToSph(self.Root.Dir)
            sList.append("Direction: (" + str(sph[0]/deg) + ', ' \
                    + str(sph[1]/deg) + ')deg')
            sList.append('}')
            if self.R is not None:
                sList = sList + self.R.outputLines()
            if self.T is not None:
                sList = sList + self.T.outputLines()

        return sList

#Beware this is a global scope function not a method of the BeamTree class
def treeOfBeam(srcBeam, optList, order, threshold):
    '''Function to calculate the tree of daughter beams of srcBeam.

    srcBeam: Input beam. [GaussianBeam]
    optList: List of optical components of the setup. [list of OpticalComponent]
    order: order of simulation. [integer]
    threshold: power threshold for daughter beams. [float]

    Returns a BeamTree.

    '''

    if len(optList) == 0:
        # No optics
        return BeamTree(Root = srcBeam)

    if srcBeam is None:
        # leaf of the tree
        return BeamTree()

    # initialize next beam dictionary
    dist = settings.inf
    finalHit = {}
    fianlisHit = {}
    finalOpt = optList[0]
    hitAtLeastOnce = False

    # look for closest impact
    for opt in optList:
        dicoisHit = opt.isHit(srcBeam)
        if dicoisHit['isHit'] and dicoisHit['distance'] < dist:
            hitAtLeastOnce = True
            dist = dicoisHit['distance']
            finalOpt = opt

    if not hitAtLeastOnce:
        # no interaction
        if settings.info:
            print "theia: Info: Reached open beam "\
            + srcBeam.Ref + "."
        return BeamTree(Root = srcBeam)

    # get parametrs of this closest impact
    finalisHit = finalOpt.isHit(srcBeam)
    finalHit = finalOpt.hit(srcBeam, order = order, threshold = threshold)

    return BeamTree(Root = srcBeam,
            T = treeOfBeam(finalHit['t'], optList, order, threshold),
            R = treeOfBeam(finalHit['r'], optList, order, threshold))
