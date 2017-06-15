'''Features module or theia, to represent objects as FreeCAD Python features.'''

# Provides:
#   class FCObject
#   class FCMirror
#   class FCLens
#   class FCBeamDump
#   class FCBeam

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

class FCLens(FCObject):
    def __init__(self, obj, lens):
        super(FCLens, self).__init__(obj)

class FCBeamDump(FCObject):
    def __init__(self, obj, beamdump):
        super(FCBeamDump, self).__init__(obj)

class FCBeam(FCObject):
    def __init__(self, obj, beam):
        super(FCBeam, self).__init__(obj)
