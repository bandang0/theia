'''Defines the ThinLens class for theia.'''

# Provides:
#   class ThinLens
#       __init__
#       lines

import numpy as np
from ..helpers import settings
from ..helpers.units import *
from ..helpers.geometry import rectToSph
from .lens import Lens

class ThinLens(Lens):
    '''

    ThinLens class.

    This class represents thin lenses, which are specified only by their focal
    lengths, diameter, position and orientation. Only the constructor and the
    printing distinguishes thin lenses (in implementation) from other lenses.

    *=== Attributes ===*
    SetupCount (inherited): class attribute, counts all setup components.
        [integer]
    OptCount (inherited): class attribute, counts optical components. [string]
    HRCenter (inherited): center of the 'chord' of the HR surface. [3D vector]
    HRNorm (inherited): unitary normal to the 'chord' of the HR (always pointing
        towards the outside of the component). [3D vector]
    Thick (inherited): thickness of the optic, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
    Name (inherited): name of the component. [string]
    Ref (inherited): reference string (for keeping track with the lab). [string]
    ARCenter (inherited): center of the 'chord' of the AR surface. [3D vector]
    ARNorm (inherited): unitary normal to the 'chord' of the AR (always pointing
        towards the outside of the component). [3D vector]
    N (inherited): refraction index of the material. [float]
    HRK, ARK (inherited): curvature of the HR, AR surfaces. [float]
    HRr, HRt, ARr, ARt (inherited): power reflectance and transmission
        coefficients of the HR and AR surfaces. [float]
    KeepI (inherited): whether of not to keep data of rays for interference
        calculations on the HR. [boolean]
    Focal: Focal length of the lens. [float]

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

    def __init__(self, Focal = 10*cm, KeepI = False, Theta = np.pi/2., Phi = 0.,
                Diameter = 5.*cm, R = .1, T = .9,
                X = 0., Y = 0., Z = 0., Name = "ThinLens", Ref = None):
        '''ThinLens constructor.

        Parameters are the attributes.

        Returns a ThinLens.

        '''
        # initialize focal
        self.Focal = float(Focal)

        #prepare for mother constructor
        HRNorm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)
        Center = np.array([X, Y, Z], dtype = np.float64)
        N = 1.4548

        # thin lens approximation of lensmaker's equation
        HRK = - 0.5/(self.Focal*(N - 1.))
        ARK = HRK
        ARNorm = - HRNorm

        # calculate  ARCenter, ARNorm  and HRCenter with focal
        if self.Focal >= 0.:
            Thickness = settings.zero
        else:
            try:    #arcsin might fail, if it does then the semi angle is pi/2
                theta = np.arcsin(Diameter * HRK/2.)   # half angle
            except FloatingPointError:
                theta = np.pi/2.
            Thickness = settings.zero + 2.*(1.-np.cos(theta))/HRK
        HRCenter = Center + Thickness*HRNorm/2.
        ARCenter = Center - Thickness*HRNorm/2.

        # initialize with lens mother constructor
        super(Lens, self).__init__(ARCenter = ARCenter, ARNorm = ARNorm, N = N,
                HRK = HRK, ARK = ARK,
                ARr = R, ARt = T, HRr = R, HRt = T, KeepI = KeepI,
                HRCenter = HRCenter, HRNorm = HRNorm, Thickness = Thickness,
                Diameter = Diameter, Name = Name, Ref = Ref)

        #warns on geometry
        if settings.warning:
            self.geoCheck("thinlens")


    def lines(self):
        '''Returns the list of lines necessary to print the object.
        '''
        ans = []
        ans.append("ThinLens: " + self.Name + " (" + str(self.Ref) + ") {")
        ans.append("Diameter: " + str(self.Dia/cm) + "cm")
        ans.append("Focal: " + str(self.Focal/mm) + "mm")
        ans.append("Center: " + str(self.HRCenter))
        sph = rectToSph(self.HRNorm)
        ans.append("Norm: (" + str(sph[0]/deg) + ', ' \
                + str(sph[1]/deg) + ')deg')
        ans.append("R, T: " + str(self.HRr) + ", " + str(self.HRt) )
        ans.append("}")

        return ans
