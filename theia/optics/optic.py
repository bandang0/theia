'''Defines the Optic class for theia.'''

# Provides:
#   class Optic
#       __init__
#       isHit
#       hitSide

import numpy as np
from units import *
from component import SetupComponent

class Optic(SetupComponent):
    '''

    Optic class.

    This class is a base class for optics which may interact with Gaussian
    beams and return transmitted and reflected beams (mirrors, lenses, etc.)


    *=== Attributes ===*
    SetupCount (inherited): class attribute, counts all setup components.
        [integer]
    OptCount: class attribute, counts optical components. [string]
    HRCenter (inherited): center of the 'chord' of the HR surface. [3D vector]
    HRNorm (inherited): unitary normal to the 'chord' of the HR (always pointing
     towards the outside of the component). [3D vector]
    Thick (inherited): thickness of the optic, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
    Name (inherited): name of the component. [string]
    Ref (inherited): reference string (for keeping track with the lab). [string]
    ARCenter: center of the 'chord' of the AR surface. [3D vector]
    ARNorm: unitary normal to the 'chord' of the AR (always pointing
     towards the outside of the component). [3D vector]
    N: refraction index of the material. [float]
    HRK, ARK: curvature of the HR, AR surfaces. [float]
    HRr, HRt, ARr, ARt: power reflectance and transmission coefficients of
        the HR and AR surfaces. [float]
    KeepI: whether of not to keep data of rays for interference calculations
            on the HR. [boolean]

    **Note**: the curvature of any surface is positive for a concave surface
    (coating inside the sphere).
    Thus kurv*HRNorm/|kurv| always points to the center
    of the sphere of the surface, as is the convention for the lineSurfInter of
    geometry module. Same for AR.

    *******     HRK > 0 and ARK > 0     *******           HRK > 0 and ARK < 0
     *****                               ********         and |ARK| > |HRK|
     H***A                               H*********A
     *****                               ********
    *******                             *******

    '''

    OptCount = 0   #counts the setup components

    def __init__(self, ARCenter = [0.02, 0., 0.], ARNorm = [1., 0., 0.],
                N = 1.4585, HRK = 0., ARK = 0., ARr = 0.1, ARt = 0.9, HRr = 0.9,
                HRt = 0.1, KeepI = False, HRCenter = None, HRNorm = None,
                Thickness = None, Diameter = None, Name = None, Ref = None):
        '''Optic base constructor.

        Parameters are the attributes of the object to construct.

        Returns an Optic.

        '''
        # initialize data from base constructor
        super(Optic, self).__init__(HRCenter = HRCenter, HRNorm = HRnorm
                Name = Name, Ref = Ref, Thickness = Thickness,
                Diameter = Diameter)

        # initilaize with input data
        self.ARCenter = np.array(ARCenter, dtype = np.float64)
        self.ARNorm = np.array(ARNorm, dtype = np.float64)
        self.ARNorm = self.ARNorm/np.linalg.norm(self.ARNorm)
        self.N = float(N)
        self.HRK = float(HRK)
        self.ARK = float(ARK)
        self.HRr = float(HRr)
        self.HRt = float(HRt)
        self.ARr = float(ARr)
        self.ARt = float(ARt)
        self.KeepI = KeepI

        # override base names and refs
        if Name is not None:
            self.Name = Name
        else:
            self.Name = "Optics"

        if Ref is not None:
            self.Ref = Ref
        else:
            self.Ref = "Opt" + str(self.__class__.OptCount)

        self.__class__.OptCount = self.__class__.OptCount + 1

    def isHit(self, beam):
        '''Determine if a beam hits the Optic.

        This is a generic function for all optics, using their geometrical
        attributes. This uses the line***Inter functions from the geometry
        module to find characteristics of impact of beams on optics.

        beam: incoming beam. [GaussianBeam]

        Returns a dictionnary with keys:
            'isHit': whether the beam hits the optic. [boolean]
            'intersection point': point in space where it is first hit.
                    [3D vector]
            'face': to indicate which face is first hit, can be 'HR', 'AR' or
                'side'. [string]
            'distance': geometrical distance from beam origin to impact. [float]

        '''
        noInterDict = {'isHit': False,
                        'intersection point': np.array([0., 0., 0.],
                                                    dtype=np.float64),
                        'face': None,
                        'distance': 0.}

        # get impact parameters on HR, AR and side:
        if np.abs(self.HRK) > 0.:
            HRDict = geo.lineSurfInter(beam.Pos,
                                        beam.Dir, self.HRCenter,
                                        self.HRK*self.HRNorm/np.abs(self.HRK),
                                        np.abs(self.HRK),
                                        self.Dia)
        else:
            HRDict = geo.linePlaneInter(beam.Pos, beam.Dir, self.HRCenter,
                                        self.HRNorm, self.Dia)

        if np.abs(self.ARK) > 0.:
            ARDict = geo.lineSurfInter(beam.Pos,
                                        beam.Dir, self.ARCenter,
                                        self.ARK*self.ARNorm/np.abs(self.ARK),
                                        np.abs(self.ARK),
                                        self.Dia/np.cos(self.Wedge))
        else:
            ARDict = geo.linePlaneInter(beam.Pos, beam.Dir, self.ARCenter,
                                        self.ARNorm, self.Dia)

        SideDict = geo.lineCylInter(beam.Pos, beam.Dir,
                                    self.HRCenter, self.HRNorm,
                                    self.Thick, self.Dia)

        # face tags
        HRDict['face'] = 'HR'
        ARDict['face'] = 'AR'
        SideDict['face'] = 'Side'


        # determine first hit
        hitFaces = filter(helpers.hitTrue, [HRDict, ARDict, SideDict])

        if len(hitFaces) == 0:
            return noInterDict

        dist = hitFaces[0]['distance']
        j=0

        for i in range(len(hitFaces)):
            if hitFaces[i]['distance'] < dist:
                dist = hitFaces[i]['distance']
                j=i

        return {'isHit': True,
                'intersection point': hitFaces[j]['intersection point'],
                'face': hitFaces[j]['face'],
                'distance': hitFaces[j]['distance']
                }

    def hitSide(self, beam):
        '''Compute the daughter beams after interaction on Side at point.

        Generic function: all sides stop beams.

        beam: incident beam. [GaussianBeam]

        Returns {'t': None, 'r': None}

        '''
        return {'t': None, 'r': None}
