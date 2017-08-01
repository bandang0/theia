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
    ap = lens.apexes()
    Cyl = Part.makeCylinder((lens.Dia/2.)/fact, lens.Thick/fact,
                                 Base.Vector(0,0,0),
                                 Base.Vector(tuple(-lens.HRNorm)))

    Cone1 = Part.makeCone(lens.Dia/2./fact, 0.,
                            np.linalg.norm(ap[0] - lens.HRCenter)/fact,
                            Base.Vector(0., 0., 0.),
                            Base.Vector(tuple(lens.HRCenter)))

    Cone2 = Part.makeCone(lens.Dia/2./fact, 0.,
                            np.linalg.norm(ap[1] - lens.ARCenter)/fact,
                            Base.Vector(tuple(lens.ARCenter/fact \
                                - lens.HRCenter/fact)),
                            Base.Vector(tuple(lens.ARCenter)))

    if lens.HRK > 0.:
        rtn =  Cyl.cut(Cone1)
    else:
        rtn = Cyl.fuse(Cone1)

    if lens.ARK > 0.:
        return rtn.cut(Cone2)
    else:
        return rtn.fuse(Cone2)

    return rtn

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
    L = beam.Length if beam.Length > 0. else 1.e6

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
    Yalpha = (beam.Wl/beam.N)/(np.pi * Wy)
    Yc = np.tan(Yalpha/2.)
    E2 =  L * beam.Dir/fact

    XA1 = Base.Vector(tuple( - DWx * Xc * Ux/fact))
    XB1 = Base.Vector(tuple(DWx * Xc * Ux/fact ))
    XA2 = Base.Vector(tuple(E2 + (L - DWx) * Xc * Ux/fact))
    XB2 = Base.Vector(tuple(E2 - (L - DWx) * Xc * Ux/fact))

    YA1 = Base.Vector(tuple( - DWy * Yc * Uy/fact))
    YB1 = Base.Vector(tuple( + DWy * Yc * Uy/fact ))
    YA2 = Base.Vector(tuple(E2 + (L - DWy) * Yc * Uy/fact))
    YB2 = Base.Vector(tuple(E2 - (L - DWy) * Yc * Uy/fact))

    S1 = Part.Face(Part.Wire([Part.Line(XA1, XB1).toShape(),
    Part.Line(XB1, XB2).toShape(),
    Part.Line(XB2, XA2).toShape(),
    Part.Line(XA1, XA2).toShape()]))

    S2 = Part.Face(Part.Wire([Part.Line(YA1, YB1).toShape(),
    Part.Line(YB1, YB2).toShape(),
    Part.Line(YA2, YB2).toShape(),
    Part.Line(YA1, YA2).toShape()]))

    return S1.fuse(S2)
