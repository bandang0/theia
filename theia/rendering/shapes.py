'''Shapes module for theia, provides shape-calculating for 3D rendering.'''

# Provides:
#   mirrorShape
#   beamSplitterShape
#   lensShape
#   beamDumpShape
#   beamShape

import numpy as np
import Part
from FreeCAD import Base
from ..helpers import settings
from ..helpers.units import deg

def mirrorShape(mirror):
    '''Computes the 3D representation of the mirror, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor    #factor for units in CAD
    return Part.makeCylinder((mirror.Dia/2.)/fact, mirror.Thick/fact,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-mirror.HRNorm)))

def beamSplitterShape(bs):
    '''Computes the 3D representation of the beamsplitter, for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor    #factor for units in CAD
    return Part.makeCylinder((bs.Dia/2.)/fact, bs.Thick/fact,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-bs.HRNorm)))


def lensShape(lens):
    '''Computes the 3D representation of the lens, a shape for a CAD file obj.

    lens: lens to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor    #factor for units in CAD
    return Part.makeCylinder((lens.Dia/2.)/fact, max(lens.Thick/fact,0.01/fact),
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-lens.HRNorm)))

def beamDumpShape(beamDump):
    '''Computes the 3D representation of the beamdump, for a CAD file obj.

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
    L = beam.Length if beam.Length > 0. else 1.e6

    #geometrical data of the beam envelope
    theta = np.real(beam.QParam()[2])
    Wx = beam.Wx
    Wy = beam.Wy

    DWx = beam.DWx
    DWy = beam.DWy
    Ux0 = beam.U[0]
    Uy0 = beam.U[1]

    #rotate vectors to find eigendirections of Q:
    Ux = np.cos(theta) * Ux0 + np.sin(theta) * Uy0
    Uy = -np.sin(theta) * Ux0 + np.cos(theta) * Uy0

    #make shape by using points
    Xalpha = (beam.Wl/beam.N)/(np.pi * Wx)
    Xc = np.tan(Xalpha/2.)
    Yalpha = (beam.Wl/beam.N)/(np.pi * Wy)
    Yc = np.tan(Yalpha/2.)
    E2 =  L * beam.Dir/fact

    XA1 = Base.Vector(tuple( - DWx * Xc * Ux/fact))
    XB1 = Base.Vector(tuple(DWx * Xc * Ux/fact \
                                + (0.01 * Ux if DWx == 0. else 0.)))
    XA2 = Base.Vector(tuple(E2 + (L - DWx) * Xc * Ux/fact))
    XB2 = Base.Vector(tuple(E2 - (L - DWx) * Xc * Ux/fact \
                                +(0.01 * Ux if (L -DWx) == 0. else 0.)))

    YA1 = Base.Vector(tuple( - DWy * Yc * Uy/fact))
    YB1 = Base.Vector(tuple( + DWy * Yc * Uy/fact \
                                + (0.01 * Ux if DWx == 0. else 0.)))
    YA2 = Base.Vector(tuple(E2 + (L - DWy) * Yc * Uy/fact))
    YB2 = Base.Vector(tuple(E2 - (L - DWy) * Yc * Uy/fact \
                                +(0.01 * Ux if (L -DWx) == 0. else 0.)))

    L1 = Part.Line(XA1, XB1).toShape()
    L2 = Part.Line(XB1, XB2).toShape()
    L3 = Part.Line(XB2, XA2).toShape()
    L4 = Part.Line(XA1, XA2).toShape()
    L5 = Part.Line(YA1, YB1).toShape()
    L6 = Part.Line(YB1, YB2).toShape()
    L7 = Part.Line(YA2, YB2).toShape()
    L8 = Part.Line(YA1, YA2).toShape()

    try:
        S1 = Part.Face(Part.Wire([L1, L2, L3, L4]))
    except Part.OCCError:
        S1 = L1.fuse(L2).fuse(L3).fuse(L4)

    try:
        S2 = Part.Face(Part.Wire([L5, L6, L7, L8]))
    except Part.OCCError:
        S2 = L5.fuse(L6).fuse(L7).fuse(L8)

    try:
        return S1.fuse(S2)
    except Part.OCCError:
        return Part.makeLine(Base.Vector(0., 0., 0.),
                                Base.Vector(tuple(L * beam.Dir/fact)))
