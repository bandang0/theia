'''Shapes module for theia, provides shape-calculating for 3D rendering.'''

# Provides:
#   mirrorShape
#   lensShape
#   beamDumpShape
#   ghostShape
#   beamShape

import numpy as np
import Part
import FreeCAD as App
from FreeCAD import Base
from ..helpers import settings

def mirrorShape(mirror):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    return Part.makeCylinder((mirror.Dia/2.)/0.001, mirror.Thick/0.001,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-mirror.HRNorm)))

def lensShape(lens):
    '''Computes the 3D representation of the lens, a shape for a CAD file obj.

    lens: lens to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    return Part.makeCylinder((lens.Dia/2.)/0.001, max(lens.Thick/0.001, 0.001),
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-lens.HRNorm)))

def beamDumpShape(beamDump):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    return Part.makeCylinder((beamDump.Dia/2.)/0.001, beamDump.Thick/0.001,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-beamDump.HRNorm)))

def ghostShape(ghost):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    return Part.makeCylinder((ghost.Dia/2.)/0.001, 0.01/0.001,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-ghost.HRNorm)))

def beamShape(beam):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    line = Part.Line()
    line.StartPoint = Base.Vector(0,0,0)
    zero = np.array([0., 0., 0.])
    if beam.Length > 0.:
        line.EndPoint = Base.Vector(tuple(zero + beam.Length/0.001 * beam.Dir))
    else:
        line.EndPoint = Base.Vector(tuple(zero + 1.e7/0.001 * beam.Dir))

    return line.toShape()
