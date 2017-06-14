'''Shapes module for theia, provides shape-calculating for 3D rendering.'''

# Provides:
#   mirrorShape
#   lensShape
#   beamDumpShape
#   ghostShape
#   beamShape

import FreeCAD as App
import Part

def beamShape(beam):
    '''Compues the 3D representation of the beam, as a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object

    '''

    return Part.makeLine(App.Vector(0, 0, 0), App.Vector(1, 1, 1))
