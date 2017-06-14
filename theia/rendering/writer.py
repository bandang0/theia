'''Writer module for theia, to write CAD content to files.'''

# Provides:
#   writeToCAD

import FreeCAD as App
from .shapes import mirrorShape, lensShape, beamDumpShape, ghostShape, beamShape
from .features import FCMirror, FCLens, FCBeamDump, FCBeam

def writeToCAD(component, doc):
    '''Write the relevant shape and feature content of components in CAD file.

    To the doc .fcstd file are added two objects, one of type
        App::FeaturePython which will hold the internal data of the component
        for reviewing in the side panel of FreeCAD, and one of type
        Part::Feature for visualization.
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
                'BeamDump': FCBeamDump,
                'Beam': FCBeam}

    shapeDic = {'Mirror': mirrorShape,
                'ThickLens': lensShape,
                'ThinLens': lensShape,
                'BeamDump': beamDumpShape,
                'Beam': beamShape
                'Ghost': ghostShape}

    #First feature (only for other than ghost)
    if not component.Name == "Ghost":
        featureObj = doc.addObject("App:FeaturePython", component.Ref)
        FCDic[component.Name](featureObj, component)

    # Then shape
    shapeObj = doc.addObject("Part::Feature", component.Ref)
    shapeObj.Shape = shapeDic[component.Name](component)

    if not component.Name == 'Beam':
        #HRCenter is defined
        shapeObj.Placement.Base = App.Vector(component.HRCenter[0],
                                            component.HRCenter[1],
                                            component.HRCenter[2])
    else:
        # it is a beam, use pos
        shapeObj.Placement.Base = App.Vector(component.Pos[0],
                                            component.Pos[1],
                                            component.Pos[2])
