'''Shapes module for theia, provides shape-calculating for 3D rendering.'''

# Provides:
#   mirrorShape
#   lensShape
#   beamDumpShape
#   ghostShape
#   beamShape

import numpy as np
import Part
from FreeCAD import Base
from ..helpers import settings
from ..helpers.units import deg

def mirrorShape(mirror):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor    #factor for units in CAD
    return Part.makeCylinder((mirror.Dia/2.)/fact, mirror.Thick/fact,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-mirror.HRNorm)))

def lensShape(lens):
    '''Computes the 3D representation of the lens, a shape for a CAD file obj.

    lens: lens to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor    #factor for units in CAD
    return Part.makeCylinder((lens.Dia/2.)/fact, max(lens.Thick/fact, 0.001),
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-lens.HRNorm)))

def beamDumpShape(beamDump):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor    #factor for units in CAD
    return Part.makeCylinder((beamDump.Dia/2.)/fact, beamDump.Thick/fact,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-beamDump.HRNorm)))

def beamShape(beam):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor
    L = beam.Length if beam.Length > 0. else 1.e7

    #geometrical data of the beam envelope
    theta = np.real(beam.QParam()['theta'])
    W = beam.waistSize()
    Wx = W[0]
    Wy = W[1]

    D = beam.waistPos()
    DWx = D[0]
    DWy = D[1]
    Ux0 = beam.U[0]
    Uy0 = beam.U[1]

    #rotate vectors to find eigendirections of Q:
    Ux = np.cos(theta) * Ux0 + np.sin(theta) * Uy0
    Uy = -np.sin(theta) * Ux0 + np.cos(theta) * Uy0

    #make shape by using points
    Xalpha = (beam.Wl/beam.N)/(np.pi * Wx)
    Xc = np.tan(Xalpha/2.)
    XE2 =  L * beam.Dir/fact
    XA1 = Base.Vector(tuple( - DWx * Xc * Ux/fact))
    XB1 = Base.Vector(tuple( DWx * Xc * Ux/fact ))
    XA2 = Base.Vector(tuple( (L - DWx) * Xc * Ux/fact))
    XB2 = Base.Vector(tuple( - (L - DWx) * Xc * Ux/fact))

    Yalpha = (beam.Wl/beam.N)/(np.pi * Wy)
    Yc = np.tan(Yalpha/2.)
    YE2 =  L * beam.Dir/fact
    YA1 = Base.Vector(tuple(YE2 - DWy * Yc * Uy/fact))
    YB1 = Base.Vector(tuple(YE2 +  DWy * Yc * Uy/fact ))
    YA2 = Base.Vector(tuple(YE2 + (L - DWy) * Yc * Uy/fact))
    YB2 = Base.Vector(tuple(YE2 - (L - DWy) * Yc * Uy/fact))

    XCone = [Part.Line(XA1, XB1),
            Part.Line(XB1, XB2),
            Part.Line(XB2, XA2),
            Part.Line(XA1, XA2)]
    print XA1, XB1, XB2, XA2

    YCone = [Part.Line(YA1, YB1),
            Part.Line(YB1, YB2),
            Part.Line(YA2, YB2),
            Part.Line(YA1, YA2)]

    shape1 = Part.Shape(YCone)
    shape2 = Part.Shape(XCone)
    finalShape = shape1.fuse(shape2)
    print Xalpha/deg
    return finalShape
