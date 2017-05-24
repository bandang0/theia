'''Defines the ThickLens class for theia.'''

# Provides:
#   class ThickLens
#       __init__
#       lineList

import numpy as np
from helpers import settings
from helpers.geometry import rectToSph
from helpers.units import *
from optics.lens import Lens

class ThickLens(Lens):
    '''

    ThickLens class.

    This class represents thick lenses, specified by curvatures and thickness
    instead of focal length.

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

    **Note**: in the case of thicklenses, the thickness provided to and by the
    constructor is the thickness *on the optical axis*, and not the thickness
    on the side of the component (like mirrors).

    **Note**: in the case of thicklenses, the center provided to the constructor
    is the *apex* of the principal face, and not the chord of the HR surface.

    '''

    def __init__(self, K1 = None, K2 = None, X = 0., Y = 0., Z = 0.,
                Theta = None, Phi = None,
                Thickness = None, N = None, KeepI = None,
                Diameter = None, R = None, T = None,
                Name = None, Ref = None):
        '''ThickLens constructor.

        Parameters are the attributes.

        Returns a ThickLens.

        '''
        if Theta is None:
            Theta = np.pi/2.
        if Phi is None:
            Phi = 0.
        if R is None:
            R = .1
        if T is None:
            T = .9
        if Name is None:
            Name = "ThickLens"

        Norm = np.array([np.sin(Theta)*np.cos(Phi), np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        # initialize with base constructor
        super(Lens, self).__init__(ARCenter = None, ARNorm = None, N = None,
                HRK = K1, ARK = K2,
                ARr = R, ARt = T, HRr = R, HRt = T, KeepI = KeepI,
                HRCenter = [X, Y, Z], HRNorm = Norm, Thickness = None,
                Diameter = Diameter, Name = Name, Ref = Ref)

        # Normals are always opposite
        self.ARnorm = - self.HRNorm

        # half angles
        try:
            theta1 = np.abs(np.arcsin(self.Dia * self. HRK/2. ))
        except FloatingPointError:
            theta1 = np.pi/2.
        try:
            theta2 = np.abs(np.arcsin(self.Dia * self. ARK/2. ))
        except FloatingPointError:
            theta2 = np.pi/2.

        apex2 = self.HRCenter + self.Thick * self.ARNorm    #thickness on axis

        # real HR andAR centers
        if np.abs(self.HRK) > 0.:
            self.HRCenter = self.HRCenter\
                        + (1. - np.cos(theta1))*self.HRNorm/self.HRK

        if np.abs(self.ARK) > 0.:
            self.ARCenter = apex2\
                        + (1. - np.cos(theta2))*self.ARNorm/self.ARK

        #Warnings for console output
        if settings.warning:
            self.geoCheck("thicklens")

    def lines(self):
        '''Returns the list of lines necessary to print the object.
        '''
        ans = []
        ans.append("ThickLens: " + self.Name + " (" + str(self.Ref) + ") {")
        ans.append("Thick: " + str(self.Thick/cm) + "cm")
        ans.append("Diameter: " + str(self.Dia/cm) + "cm")
        ans.append("Center: " + str(self.HRCenter))
        sph = rectToSph(self.HRNorm)
        ans.append("Norm: (" + str(sph[0]/deg) + ', ' \
                + str(sph[1]/deg) + ')deg')
        ans.append("Index: " + str(self.N))
        ans.append("HRKurv, ARKurv: " + str(self.HRK) + ", " + str(self.ARK))
        ans.append("R, T: " + str(self.HRr) + ", " + str(self.HRt) )
        ans.append("}")

        return ans
