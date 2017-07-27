'''Features module or theia, to represent objects as FreeCAD Python features.'''

# Provides:
#   class FCObject
#   class FCMirror
#   class FCLens
#   class FCBeamDump
#   class FCBeam

from FreeCAD import Base
from ..helpers import settings
from .shapes import mirrorShape, lensShape, beamDumpShape, beamShape

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
        obj.addProperty("App::PropertyAngle", "Wedge", "Mirror",
                "Wedge of the mirror").Wedge = mirror.Wedge
        obj.addProperty("App::PropertyString", "HRK", "Mirror",
                "HR curvature").HRK = str(mirror.HRK) + ' m^-1'
        obj.addProperty("App::PropertyString", "ARK", "Mirror",
                "AR curvature").ARK = str(mirror.ARK) + ' m^-1'
        obj.addProperty("App::PropertyDistance", "Thick", "Mirror",
                "Thickness of mirror").Thick = mirror.Thick/self.fact
        obj.addProperty("App::PropertyFloat", "N", "Mirror",
                "Optical index").N = mirror.N
        obj.addProperty("App::PropertyDistance", "Dia", "Mirror",
                "Diameter").Dia = mirror.Dia/.001
        obj.Placement.Base = Base.Vector(tuple(mirror.HRCenter/self.fact))

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
        obj.addProperty("App::PropertyString", "Order", "Beam",
                "Order of the beam").Order = str(beam.StrayOrder)
        obj.addProperty("App::PropertyString", "P", "Beam",
                "Power of the beam").P = str(beam.P/0.001) + 'mW'
        obj.addProperty("App::PropertyDistance", "WDx", "Beam",
                "Waist distance X").WDx = beam.waistPos()[0]/self.fact
        obj.addProperty("App::PropertyDistance", "WDy", "Beam",
                "Waist distance Y").WDy = beam.waistPos()[1]/self.fact
        obj.addProperty("App::PropertyDistance", "Wx", "Beam",
                "Waist on X").Wx = beam.waistSize()[0]/self.fact
        obj.addProperty("App::PropertyDistance", "Wy", "Beam",
                "Waist on Y").Wy = beam.waistSize()[1]/self.fact
        obj.Placement.Base = Base.Vector(tuple(beam.Pos/self.fact))
