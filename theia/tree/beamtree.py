'''Defines the BeamTree class for theia.'''

# Provides:
#   class BeamTree
#       __init__
#       __str__
#       lines
#       beamList
#       beamLines
#       numberOfBeams
#       outputLines
#   treeOfBeam

import numpy as np
from ..helpers import settings
from ..helpers.units import mm, deg
from ..helpers.tools import formatter, shortRef
from ..helpers.geometry import rectToSph, linePlaneInter

class BeamTree(object):
    '''

    BeamTree class.

    A BeamTree is a binary tree which allows to keep track of the beams as they
    are traced throughout the optical setup. The Root of the tree is a Gaussian
    beam and the other attributes are the daughter trees and all the data of the
    interaction producing these with the Root beam

    *=== Attributes ===*
    Name: class attribute, name of object. [string]
    Root: beam of this node of the tree. [GaussianBeam]
    T: beam resulting from the transmission of the Root beam. [BeamTree]
    R: beam resulting from the reflection of the Root beam. [BeamTree]

    '''
    Name = "BeamTree"

    def __init__(self, Root = None,
                T = None, R = None):
        '''BeamTree initializer.'''
        self.Root = Root
        self.T = T
        self.R = R

    def __str__(self):
        '''String representation of a BeamTree, for print(tree).'''
        return formatter(self.lines())

    def lines(self):
        '''Returns the list of lines necessary to print the object.'''
        return ["Tree: {"
        "Root beam: %s" %(self.Root.Ref if not settings.short\
                                        else shortRef(self.Root.Ref))
        "Number of beams: %s" %str(self.numberOfBeams())
        "}"]

    def beamList(self):
        '''Returns the string representation the tree of beams.

        '''
        before = ["Tree: Root beam = %s {" %str(self.Root.Ref)]
        after = ["}"]
        return formatter(before + self.beamLines() + after)

    def beamLines(self):
        '''Returns the list of lines necessary to print the list of beams.

        '''
        if self.Root is not None:
            ans = self.Root.lines()
            if self.R is not None:
                ans = ans + self.R.beamLines()
            if self.T is not None:
                ans = ans + self.T.beamLines()
            return ans
        return list()

    def numberOfBeams(self):
        '''Return the total number of beams.'''
        if self.Root is None:
            return 0
        return 1    + (self.R.numberOfBeams if self.R is not None else 0)\
                    + (self.T.numberOfBeams if self.R is not None else 0)

    def outputLines(self):
        '''Return the list of lines to write the output of simulation.'''
        sList = list()
        if self.Root is not None and (self.Root.N == 1 or not settings.short):
            beam = self.Root
            Ref = beam.Ref if not settings.short else shortRef(beam.Ref)
            sph = rectToSph(beam.Dir)
            if beam.Length == 0.:
                sList = ["(%s, %s) [open] %s {" % (beam.Optic, beam.Face, Ref)]
            else:
                if self.R is None and self.T is None:
                    sList = ["(%s, %s) %sm [end] (%s, %s) %s {" \
                        % (beam.Optic, beam.face, str(beam.Length),
                            beam.TargetOptic, beam.TargetFace, Ref)]
                else:
                    sList = ["(%s, %s) %sm (%s, %s) %s {" \
                        % (beam.Optic, beam.face, str(beam.Length),
                            beam.TargetOptic, beam.TargetFace, Ref)]

            sList = sList + ["Waist Pos: (%s, %s)m" \
                                %(str(beam.DWx), str(beam.DWy)),
                            "Waist Size: (%s, %s)mm" \
                                %(str(beam.Wx/mm), str(beam.Wy/mm)),
                            "Direction: (%s, %s)deg" %(str(sph[0]/deg),
                                                    str(sph[1]/deg)),
                            "}"]
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
        return None

    BRef = srcBeam.Ref if not settings.short else shortRef(srcBeam.Ref)

    # stuff used for clipping
    clippingOpts = ["Mirror", "ThinLens", "ThickLens", "BeamDump", "Special"]
    waist = max(srcBeam.IWx,
                srcBeam.IWy)

    # initialize
    dist = settings.inf
    finalOpt = None

    # look for closest impact
    for opt in optList:
        dicoisHit = opt.isHit(srcBeam)
        if dicoisHit['isHit'] and dicoisHit['distance'] < dist:
            dist = dicoisHit['distance']
            finalOpt = opt

    # anti-clipping calculations!
    if settings.antiClip:
        for opt in optList:
            if opt.Name in clippingOpts and not opt is finalOpt:
                # determine intersection with larger optic
                HClipDic = linePlaneInter(srcBeam.Pos, srcBeam.Dir,
                            opt.HRCenter, opt.HRNorm,
                            opt.Dia + 2 * settings.clipFactor * waist)

                AClipDic = linePlaneInter(srcBeam.Pos, srcBeam.Dir,
                            opt.ARCenter, - opt.HRNorm,
                            opt.Dia + 2 * settings.clipFactor * waist)

                # it hit the enlarged surface but is outside
                Hif = HClipDic['isHit'] and HClipDic['distance'] < dist \
                        and np.linalg.norm(HClipDic['intersection point'] \
                            - opt.HRCenter) > opt.Dia/2.

                Aif = AClipDic['isHit'] and AClipDic['distance'] < dist \
                        and np.linalg.norm(AClipDic['intersection point'] \
                            - opt.ARCenter) > opt.Dia/2.
                if Hif or Aif and (srcBeam.N == 1. or not settings.short):
                    print "theia: Warning: Anti-clipping of beam %s on %s."\
                                        %(BRef, opt.Ref)

    if finalOpt is None:
        # no interaction
        if settings.info  and (srcBeam.N == 1. or not settings.short):
            print "theia: Info: Reached open beam %s." % BRef
        return BeamTree(Root = srcBeam)

    # get parameters of this closest impact
    finalisHit = finalOpt.isHit(srcBeam)
    finalHit = finalOpt.hit(srcBeam, order = order, threshold = threshold)

    # determine if there was clipping
    isClipped = False   # if there is clipping during the interaction
    if not finalisHit['face'] == 'Side' and finalOpt.Name in clippingOpts:
        center = {  'HR': finalOpt.HRCenter,
                    'AR': finalOpt.ARCenter}[finalisHit['face']]
        distance = np.linalg.norm(finalisHit['intersection point'] - center)
        isClipped = distance + settings.clipFactor * waist > finalOpt.Dia/2.

    #warn for clipping
    if isClipped and settings.warning\
            and (srcBeam.N == 1. or not settings.short):
        print "theia: Warning: Clipping of beam %s on (%s, %s)."\
            %(BRef, finalOpt.Ref, finalisHit['face'])

    return BeamTree(Root = srcBeam,
            T = treeOfBeam(finalHit['t'], optList, order, threshold),
            R = treeOfBeam(finalHit['r'], optList, order, threshold))
