'''Defines the BeamTree class for theia.'''

# Provides:
#   class OpticalComponent

import numpy as np
from units import *
from helpers import formatter


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
    Distance: distance from root beam origin to interaction. [float]
    Optic: Optic where the Root beam gave rise to T's and R's root beams.
        [OpticalBeam]
    Face: face where the interaction occured. ['HR', 'AR', or 'Side']
    ImpactPoint: 3D point in space where the interaction occured. [3D vector]
    *=== Methods ===*

    '''

    def __init__(self, Root = None, T = None, R = None, Distance = None,
            Optic = None, Face = None, ImpactPoint = None):
        '''BeamTree constructor.'''
        self.Root = Root
        self.T = T
        self.R = R
        self.Distance = Distance
        self.Optic = Optic
        self.Face = Face
        self.ImpactPoint = ImpactPoint

    def __str__(self):
        '''String representation of a BeamTree, for print(tree).

        '''
        return formatter(self.lineList())

    def lineList(self):
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
        return formatter(before + self.beamLineList() + after)

    def beamLineList(self):
        '''Returns the list of lines necessary to print the list of beams.

        '''
        ans = []
        if self.Root is not None:
            ans = self.Root.lineList()
            if self.T is not None:
                ans = ans + self.T.beamLineList()
            if self.R is not None:
                ans = ans + self.R.beamLineList()

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


def treeOfBeam(srcBeam, optList, order, threshold):
    '''Function to calculate the tree of daughter beams of srcBeam.

    srcBeam: Input beam. [GaussianBeam]
    optList: List of optical components of the setup. [List of OpticalComponent]
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

    # initialize next beam dictionnaries
    dist = 1.e15
    mini = 1.e-12
    finalHit = {}
    fianlisHit = {}
    finalOpt = optList[0]
    hitAtLeastOnce = False

    # look for closest impact
    for opt in optList:
        dicoisHit = opt.isHit(srcBeam)
        if dicoisHit['isHit'] and dicoisHit['distance'] < dist \
                                and dicoisHit['distance'] > mini:
            hitAtLeastOnce = True
            dist = dicoisHit['distance']
            finalOpt = opt

    if not hitAtLeastOnce:
        # no interaction
        return BeamTree(Root = srcBeam)

    # get parametrs of this closest impact
    finalisHit = finalOpt.isHit(srcBeam)
    finalHit = finalOpt.hit(srcBeam, order = order, threshold = threshold)

    return BeamTree(Root = srcBeam,
        T = treeOfBeam(finalHit['t'], optList, order, threshold),
        R = treeOfBeam(finalHit['r'], optList, order, threshold),
        Distance = finalisHit['distance'], Optic = finalOpt,
        Face = finalisHit['face'],
        ImpactPoint = finalisHit['intersection point'])
