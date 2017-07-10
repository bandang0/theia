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
        obj.addProperty("App::PropertyString", "HRK", "Mirror",
                "HR curvature").HRK = str(mirror.HRK) + ' m^-1'
        obj.addProperty("App::PropertyString", "ARK", "Mirror",
                "AR curvature").ARK = str(mirror.ARK) + ' m^-1'
        obj.addProperty("App::PropertyDistance", "Thick", "Mirror",
                "Thickness of mirror").Thick = mirror.Thick/0.001
        obj.addProperty("App::PropertyFloat", "N", "Mirror",
                "Optical index").N = mirror.N
        obj.addProperty("App::PropertyDistance", "Dia", "Mirror",
                "Diameter").Dia = mirror.Dia/.001

class FCLens(FCObject):
    def __init__(self, obj, lens):
        super(FCLens, self).__init__(obj)
        if lens.Name == "ThinLens":
            obj.addProperty("App::PropertyDistance", "Focal", "Lens",
                    "FocalLength").Focal = lens.Focal/0.001
        else:
            obj.addProperty("App::PropertyString", "K1", "Lens",
                    "K1 curvature").K1 = str(lens.HRK) + ' m^-1'
            obj.addProperty("App::PropertyString", "K2", "Lens",
                    "K2 curvature").K2 = str(lens.ARK) + ' m^-1'
            obj.addProperty("App::PropertyDistance", "Thick", "Lens",
                    "Thickness of lens").Thick = lens.Thick/0.001
            obj.addProperty("App::PropertyFloat", "N", "Lens",
                    "Optical index").N = lens.N

        obj.addProperty("App::PropertyDistance", "Dia", "Lens",
                "Diameter").Dia = lens.Dia/0.001

class FCBeamDump(FCObject):
    def __init__(self, obj, beamDump):
        super(FCBeamDump, self).__init__(obj)
        obj.addProperty("App::PropertyDistance", "Thick", "BeamDump",
                "Thickness of beamdump").Thick = beamDump.Thick/0.001
        obj.addProperty("App::PropertyDistance", "Dia", "BeamDump",
                "Diameter").Dia = beamDump.Dia/0.001

class FCBeam(FCObject):
    def __init__(self, obj, beam):
        super(FCBeam, self).__init__(obj)
        obj.addProperty("App::PropertyString", "Order", "Beam",
                "Order of the beam").Order = str(beam.StrayOrder)
        obj.addProperty("App::PropertyString", "P", "Beam",
                "Power of the beam").P = str(beam.P/0.001) + 'mW'
        obj.addProperty("App::PropertyDistance", "WDx", "Beam",
                "Waist distance X").WDx = beam.waistPos()[0]/0.001
        obj.addProperty("App::PropertyDistance", "WDy", "Beam",
                "Waist distance Y").WDy = beam.waistPos()[1]/0.001
        obj.addProperty("App::PropertyDistance", "Wx", "Beam",
                "Waist on X").Wx = beam.waistSize()[0]/0.001
        obj.addProperty("App::PropertyDistance", "Wy", "Beam",
                "Waist on Y").Wy = beam.waistSize()[1]/0.001
