'''Writer module for theia, to write CAD content to files.'''

# Provides:
#   writeToCAD
#   writeTree

import FreeCAD as App
from FreeCAD import Base
from .shapes import mirrorShape, lensShape, beamDumpShape, ghostShape, beamShape
from .features import FCMirror, FCLens, FCBeamDump, FCBeam

def writeToCAD(component, doc):
    '''Write the relevant shape and feature content of components in CAD file.

    This function is for everython except for beams.
    To the doc .fcstd file are added two objects, one of type
        App::FeaturePython which will hold the internal data of the component
        for reviewing in the side panel of FreeCAD, and one of type
        Part::Feature for visualization. The classes for the App::FeaturePython
        objects are i nthe features modules, and those for the shapes are in
        the shapes module.
    The important functions are the PythonFeatures
        constructors found in features, and the shape functions found in shapes.

    component: component to represent. [Mirror, Lens, BeamDump, Ghost, Beam]
    doc: CAD file to write to. [CAD file]

    No return value.

    '''

    # here are some dics to refer to the right features and shapes for all
    # components
    FCDic = {'Mirror': FCMirror,
                'ThickLens': FCLens,
                'ThinLens': FCLens,
                'BeamDump': FCBeamDump}

    shapeDic = {'Mirror': mirrorShape,
                'ThickLens': lensShape,
                'ThinLens': lensShape,
                'BeamDump': beamDumpShape,
                'Ghost': ghostShape}

    #First take care of optics
    if component.Name in ['Mirror', 'ThickLens', 'ThinLens', 'BeamDump']:
        # First feature (not for ghosts)
        if not component.Name == 'Ghost':
            featureObj = doc.addObject("App::FeaturePython",
                            component.Ref + '_doc')
            FCDic[component.Name](featureObj, component)

        # Then shape
        shapeObj = doc.addObject("Part::Feature", component.Ref)
        shapeObj.Shape = shapeDic[component.Name](component)
        shapeObj.Placement.Base = Base.Vector(tuple(component.HRCenter))

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

    if tree.Root is not None:
        # write feature of beam
        featureObj = doc.addObject("App::FeaturePython", tree.Root.Ref + '_doc')
        FCBeam(featureObj, tree.Root)
        # write shape of beam
        shapeObj = doc.addObject("Part::Feature", tree.Root.Ref)
        shapeObj.Shape = beamShape(tree.Root)
        shapeObj.Placement.Base = Base.Vector(tuple(tree.Root.Pos))
        
        #recursively for daughter beams
        if tree.T is not None:
            writeTree(tree.T, doc)
        if tree.R is not None:
            writeTree(tree.R, doc)
