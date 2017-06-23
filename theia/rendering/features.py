'''Features module or theia, to represent objects as FreeCAD Python features.'''

# Provides:
#   class FCObject
#   class FCMirror
#   class FCLens
#   class FCBeamDump
#   class FCBeam

import Part
from FreeCAD import Base

class FCObject(object):
    '''Mother class for all FeaturePython objects.

    This is to define the mandatory execute method, which is ran for every
        object of the document on the recompute function.

    '''
    def __init__(self, obj):
        '''Custom properties of the object.
        '''
        obj.Proxy = self

    def execute(self, fp):
        '''We're not doing anything on recompute yet.
        '''
        pass

class FCMirror(FCObject):
    def __init__(self, obj, mirror):
        super(FCMirror, self).__init__(obj)
        obj.addProperty("App::PropertyAngle", "Wedge", "Mirror",
                "Wedge of the mirror").Wedge = mirror.Wedge
        obj.addProperty("App::PropertyFloat", "HRK", "Mirror",
                "HR curvature").HRK = mirror.HRK
        obj.addProperty("App::PropertyFloat", "ARK", "Mirror",
                "AR curvature").ARK = mirror.ARK
        obj.addProperty("App::PropertyFloat", "Thick", "Mirror",
                "Thickness of mirror").Thick = mirror.Thick
        obj.addProperty("App::PropertyFloat", "N", "Mirror",
                "Optical index").N = mirror.N
        obj.addProperty("App::PropertyFloat", "Dia", "Mirror",
                "Diameter").Dia = mirror.Dia

class FCLens(FCObject):
    def __init__(self, obj, lens):
        super(FCLens, self).__init__(obj)
        if lens.Name == "ThinLens":
            obj.addProperty("App::PropertyFloat", "Focal", "Lens",
                    "FocalLength").Focal = lens.Focal
        else:
            obj.addProperty("App::PropertyFloat", "K1", "Lens",
                    "K1 curvature").K1 = lens.HRK
            obj.addProperty("App::PropertyFloat", "K2", "Lens",
                    "K2 curvature").K2 = lens.ARK
            obj.addProperty("App::PropertyFloat", "Thick", "Lens",
                    "Thickness of lens").Thick = lens.Thick
            obj.addProperty("App::PropertyFloat", "N", "Lens",
                    "Optical index").N = lens.N

        obj.addProperty("App::PropertyFloat", "Dia", "Mirror",
                "Diameter").Dia = lens.Dia

class FCBeamDump(FCObject):
    def __init__(self, obj, beamDump):
        super(FCBeamDump, self).__init__(obj)
        obj.addProperty("App::PropertyFloat", "Thick", "BeamDump",
                "Thickness of beamdump").Thick = beamDump.Thick
        obj.addProperty("App::PropertyFloat", "Dia", "BeamDump",
                "Diameter").Dia = beamDump.Dia

class FCBeam(FCObject):
    def __init__(self, obj, beam):
        super(FCBeam, self).__init__(obj)
        obj.addProperty("App::PropertyInteger", "Order", "Beam",
                "Order of the beam").Order = beam.StrayOrder
        obj.addProperty("App::PropertyFloat", "P", "Beam",
                "Power of the beam").P = beam.P
        obj.addProperty("App::PropertyDistance", "WDx", "Beam",
                "Waist distance X").WDx = beam.waistPos()[0]
        obj.addProperty("App::PropertyDistance", "WDy", "Beam",
                "Waist distance Y").WDy = beam.waistPos()[1]
        obj.addProperty("App::PropertyDistance", "Wx", "Beam",
                "Waist on X").Wx = beam.waistSize()[0]
        obj.addProperty("App::PropertyDistance", "Wy", "Beam",
                "Waist on Y").Wy = beam.waistSize()[1]
