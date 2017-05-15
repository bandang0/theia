'''Defines the Optic class for theia.'''

# Provides:
#   class Optic
#       __init__
#       isHit
#       hitSide

import numpy as np
from component import SetupComponent
from optics import geometry as geo

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
        # allow empty constructor
        if ARCenter is None:
            ARCenter = [0.02, 0., 0.]
        if ARNorm is None:
            ARNorm = [1., 0., 0.]
        if N is None:
            N = 1.4585
        if HRK is None:
            HRK = 0.
        if ARK is None:
            ARK = 0.
        if ARr is None:
            ARr = 0.1
        if ARt is None:
            ARt = 0.9
        if HRr is None:
            HRr = 0.9
        if HRt is None:
            HRt = 0.1
        if KeepI is None:
            KeepI = False

        # initialize data from base constructor
        super(Optic, self).__init__(HRCenter = HRCenter, HRNorm = HRNorm,
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
        if Name is None:
            self.Name = "Optic"
        else:
            self.Name = Name

        if Ref is None:
            self.Ref = "Opt" + str(Optic.OptCount)
        else:
            self.Ref = Ref

        Optic.OptCount = Optic.OptCount + 1

    

    def hitSide(self, beam):
        '''Compute the daughter beams after interaction on Side at point.

        Generic function: all sides stop beams.

        beam: incident beam. [GaussianBeam]

        Returns {'t': None, 'r': None}

        '''
        return {'t': None, 'r': None}
