'''Writer module for theia, to write CAD content to files.'''

# Provides:
#   writeToCAD
#   writeTree

from FreeCAD import Base
import Part
from ..helpers import settings
from ..helpers.tools import shortRef
from .features import FCMirror, FCLens, FCBeamDump, FCBeam

def writeToCAD(component, doc):
    '''Write the relevant FreeCAD objects of components in CAD file.

    This function is for everything except for beams.
    To the doc .fcstd file are added one object per optic and beam, they
        are of type Part::FeaturePython to allow for shapes and features.

    The important functions are the PythonFeatures
        constructors found in features, and the shape functions found in shapes.

    component: component to represent. [Mirror, Lens, BeamDump, Ghost, Beam]
    doc: CAD file to write to. [CAD file]

    No return value.

    '''

    # here are some dics to refer to the right features and shapes for all
    # components
    fact = settings.FCFactor    #factor for units in CAD
    FCDic = {'Mirror': FCMirror,
                'ThickLens': FCLens,
                'ThinLens': FCLens,
                'BeamDump': FCBeamDump}

    #First take care of optics
    if component.Name in ['Mirror', 'ThickLens', 'ThinLens', 'BeamDump']:
        FCDic[component.Name](doc.addObject("Part::FeaturePython",
                            component.Ref), component)

    # Then tree (call write tree function)
    if component.Name == 'BeamTree':
        writeTree(component, doc)

def writeTree(tree, doc):
    '''Recursively write the shape and feature content of the beams of a tree.

    If the tree's root is not None, write the shape and feature for tree.Root
        and start over for the daughter trees.

    tree: beamtree to write the info. [BeamTree]
    doc: CAD file to write to. [CAD file]

    No return value.

    '''
    fact = settings.FCFactor   #factor for units in CAD

    if tree.Root is not None:
        # write FreeCAD object of beam according to short option
        if tree.Root.N == 1. or not settings.short:
            FCBeam(doc.addObject("Part::FeaturePython", tree.Root.Ref\
                if not settings.short else shortRef(tree.Root.Ref)), tree.Root)

            # add laser object if input beam
            if 't' not in tree.Root.Ref and 'r' not in tree.Root.Ref:
                laserObj = doc.addObject("Part::FeaturePython", 'laser')
                laserObj.Shape = Part.makeCylinder(0.01/fact, 0.1/fact,
                                                Base.Vector(0,0,0),
                                                Base.Vector(tuple(-tree.Root.Dir)))
                laserObj.Placement.Base = Base.Vector(tuple(tree.Root.Pos/fact))

            #recursively for daughter beams
        if tree.T is not None:
            writeTree(tree.T, doc)
        if tree.R is not None:
            writeTree(tree.R, doc)
