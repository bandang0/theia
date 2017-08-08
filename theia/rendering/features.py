'''Features module or theia, to represent objects as FreeCAD Python features.'''

# Provides:
#   class FCObject
#   class FCMirror
#   class FCBeamSplitter
#   class FCLens
#   class FCBeamDump
#   class FCBeam

from FreeCAD import Base
from ..helpers import settings
from ..helpers.units import deg
from .shapes import mirrorShape, lensShape, beamDumpShape, beamShape
from .shapes import beamSplitterShape

class FCObject(object):
    '''Mother class for all FreeCAD objects.

    fact: Factor to compensate for unit difference with FreeCAD. [float]
    '''
    fact = settings.FCFactor
    def __init__(self, obj):
        '''Custom properties of the object.
        '''
        obj.Proxy = self

class FCMirror(FCObject):
    def __init__(self, obj, mirror):
        super(FCMirror, self).__init__(obj)
        obj.Shape = mirrorShape(mirror)
        obj.addProperty("App::PropertyString", "Wedge", "Mirror",
                "Wedge of the mirror").Wedge = str(mirror.Wedge/deg) + ' deg'
        obj.addProperty("App::PropertyString", "HRK", "Mirror",
                "HR curvature").HRK = str(mirror.HRK) + ' m^-1'
        obj.addProperty("App::PropertyString", "ARK", "Mirror",
                "AR curvature").ARK = str(mirror.ARK) + ' m^-1'
        obj.addProperty("App::PropertyDistance", "Thick", "Mirror",
                "Thickness of mirror").Thick = mirror.Thick/self.fact
        obj.addProperty("App::PropertyString", "N", "Mirror",
                "Optical index").N = str(mirror.N)
        obj.addProperty("App::PropertyDistance", "Dia", "Mirror",
                "Diameter").Dia = mirror.Dia/.001
        obj.Placement.Base = Base.Vector(tuple(mirror.HRCenter/self.fact))

class FCBeamSplitter(FCObject):
    def __init__(self, obj, beamSplitter):
        super(FCBeamSplitter, self).__init__(obj)
        obj.Shape = beamSplitterShape(beamSplitter)
        obj.addProperty("App::PropertyString", "Wedge", "BeamSplitter",
            "Wedge of the beam splitter").Wedge = str(beamSplitter.Wedge/deg) \
            + ' deg'
        obj.addProperty("App::PropertyString", "HRK", "BeamSplitter",
            "HR curvature").HRK = str(beamSplitter.HRK) + ' m^-1'
        obj.addProperty("App::PropertyString", "ARK", "BeamSplitter",
            "AR curvature").ARK = str(beamSplitter.ARK) + ' m^-1'
        obj.addProperty("App::PropertyDistance", "Thick", "BeamSplitter",
            "Thickness of beam splitter").Thick = beamSplitter.Thick/self.fact
        obj.addProperty("App::PropertyString", "N", "BeamSplitter",
            "Optical index").N = str(beamSplitter.N)
        obj.addProperty("App::PropertyDistance", "Dia", "BeamSplitter",
            "Diameter").Dia = beamSplitter.Dia/.001
        obj.Placement.Base = Base.Vector(tuple(beamSplitter.HRCenter/self.fact))

class FCLens(FCObject):
    def __init__(self, obj, lens):
        super(FCLens, self).__init__(obj)
        obj.Shape = lensShape(lens)
        if lens.Name == "ThinLens":
            obj.addProperty("App::PropertyDistance", "Focal", "Lens",
                    "FocalLength").Focal = lens.Focal/self.fact
        else:
            obj.addProperty("App::PropertyString", "K1", "Lens",
                    "K1 curvature").K1 = str(lens.HRK) + ' m^-1'
            obj.addProperty("App::PropertyString", "K2", "Lens",
                    "K2 curvature").K2 = str(lens.ARK) + ' m^-1'
            obj.addProperty("App::PropertyDistance", "Thick", "Lens",
                    "Thickness of lens").Thick = lens.Thick/self.fact
            obj.addProperty("App::PropertyFloat", "N", "Lens",
                    "Optical index").N = lens.N

        obj.addProperty("App::PropertyDistance", "Dia", "Lens",
                "Diameter").Dia = lens.Dia/self.fact
        obj.Placement.Base = Base.Vector(tuple(lens.HRCenter/self.fact))

class FCBeamDump(FCObject):
    def __init__(self, obj, beamDump):
        super(FCBeamDump, self).__init__(obj)
        obj.Shape = beamDumpShape(beamDump)
        obj.addProperty("App::PropertyDistance", "Thick", "BeamDump",
                "Thickness of beamdump").Thick = beamDump.Thick/self.fact
        obj.addProperty("App::PropertyDistance", "Dia", "BeamDump",
                "Diameter").Dia = beamDump.Dia/self.fact
        obj.Placement.Base = Base.Vector(tuple(beamDump.HRCenter/self.fact))

class FCBeam(FCObject):
    def __init__(self, obj, beam):
        super(FCBeam, self).__init__(obj)
        obj.Shape = beamShape(beam)

        #general
        obj.addProperty("App::PropertyString", "Order", "Beam",
                "Order of the beam").Order = str(beam.StrayOrder)
        obj.addProperty("App::PropertyString", "Ref", "Beam",
                "Full Reference of the beam").Ref = str(beam.Ref)
        obj.addProperty("App::PropertyString", "P", "Beam",
                "Power of the beam").P = str(beam.P/0.001) + 'mW'
        obj.addProperty("App::PropertyString", "L", "Beam",
                "Length of beam").L = str(beam.Length) + 'm'\
                                    if beam.Length > 0. else 'open'
        obj.addProperty("App::PropertyString", "WDx", "Beam",
                "Waist distance X").WDx = str(beam.DWx) + 'm'
        obj.addProperty("App::PropertyString", "WDy", "Beam",
                "Waist distance Y").WDy = str(beam.DWy) + 'm'
        obj.addProperty("App::PropertyString", "Wx", "Beam",
                "Waist on X").Wx = str(beam.Wx/0.001) + 'mm'
        obj.addProperty("App::PropertyString", "Wy", "Beam",
                "Waist on Y").Wy = str(beam.Wy/0.001) + 'mm'

        #origin
        obj.addProperty("App::PropertyString", "OriginOptic", "Origin",
                "Origin Optic").OriginOptic = beam.Optic
        obj.addProperty("App::PropertyString", "OriginFace", "Origin",
                "Origin Face").OriginFace = beam.Face
        obj.addProperty("App::PropertyString", "IWx", "Origin",
                "Origin width on X").IWx = str(beam.IWx/0.001) + 'mm'
        obj.addProperty("App::PropertyString", "IWy", "Origin",
                "Origin width on Y").IWy = str(beam.IWy/0.001) + 'mm'

        #target
        obj.addProperty("App::PropertyString", "TargetOptic", "Target",
                "Target Optic").TargetOptic = beam.TargetOptic \
                if beam.TargetOptic is not None else 'open'
        obj.addProperty("App::PropertyString", "TargetFace", "Target",
                "Target Face").TargetFace = beam.TargetFace \
                if beam.TargetFace is not None else 'open'
        obj.addProperty("App::PropertyString", "TWx", "Target",
                "Target width on X").TWx = str(beam.TWx/0.001) + 'mm'\
                if beam.TWx is not None else 'open'
        obj.addProperty("App::PropertyString", "TWy", "Target",
                "Target width on Y").TWy = str(beam.TWy/0.001) + 'mm'\
                if beam.TWy is not None else 'open'

        #placement
        obj.Placement.Base = Base.Vector(tuple(beam.Pos/self.fact))
