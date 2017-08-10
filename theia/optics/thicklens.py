'''Defines the ThickLens class for theia.'''

# Provides:
#   class ThickLens
#       __init__
#       lines

import numpy as np
from ..helpers import settings
from ..helpers.geometry import rectToSph
from ..helpers.units import cm, deg, pi
from .optic import Optic

class ThickLens(Optic):
    '''

    ThickLens class.

    This class represents thick lenses, specified by curvatures and thickness
    instead of focal length.

    Actions:
        * T on HR: 0
        * R on HR: + 1
        * T on AR: 0
        * R on AR: + 1

    *=== Additional attributes with respect to the Optic class ===*

    None

    *=== Name ===*

    ThickLens

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
    initializer is the thickness *on the optical axis*, and not the thickness
    on the side of the component (like mirrors).

    **Note**: in the case of thicklenses, the center provided to the initializer
    is the *apex* of the principal face, and not the chord of the HR surface.

    '''
    Name = "ThickLens"

    def __init__(self, K1 = 0.01, K2 = 0.01, X = 0., Y = 0., Z = 0.,
                Theta = pi/2., Phi = 0.,
                Thickness = 2.e-2, N = 1.4585, KeepI = False,
                Diameter = 5.e-2, R = 0.1, T = .9, Ref = None):
        '''ThickLens initializer.

        Parameters are the attributes.

        Returns a ThickLens.

        '''
        # actions
        TonHR = 0
        RonHR = 1
        TonAR = 0
        RonAR = 1

        #check input
        K1 = float(K1)
        K2 = float(K2)
        Theta = float(Theta)
        Phi = float(Phi)
        Thickness = float(Thickness)
        N = float(N)
        Diameter = float(Diameter)
        R = float(R)
        T = float(T)
        Wedge = 0.
        Alpha = 0.

        # prepare for mother initializer
        HRNorm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta)*np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)
        Apex1 = np.array([X, Y, Z], dtype = np.float64)

        # Normals are always opposite
        ARNorm = - HRNorm
        Apex2 = Apex1 + Thickness * ARNorm    #thickness on axis

        # half angles
        theta1 = np.abs(np.arcsin(Diameter * K1/2. ))\
            if np.abs(Diameter * K1 /2.) < 1. else pi/2.
        theta2 = np.abs(np.arcsin(Diameter * K2/2. ))\
            if np.abs(Diameter * K2 /2.) < 1. else pi/2.

        # real HR and AR centers
        HRCenter = Apex1 + (1. - np.cos(theta1))*HRNorm/K1\
            if np.abs(K1) > 0. else Apex1
        HRCenter = Apex2 + (1. - np.cos(theta2))*HRNorm/K2\
            if np.abs(K2) > 0. else Apex2

        # initialize with base initializer
        super(ThickLens, self).__init__(ARCenter = ARCenter, ARNorm = ARNorm,
                N = N,
                HRK = K1, ARK = K2,
                ARr = R, ARt = T, HRr = R, HRt = T, KeepI = KeepI,
                HRCenter = HRCenter, HRNorm = HRNorm, Thickness = Thickness,
                Diameter = Diameter, Wedge = Wedge, Alpha = Alpha,
                TonHR = TonHR, RonHR = RonHR, TonAR = TonAR, RonAR = RonAR,
                Ref = Ref)

        #Warnings for console output
        if settings.warning:
            self.geoCheck("thick lens")

    def lines(self):
        '''Returns the list of lines necessary to print the object.
        '''
        sph = rectToSph(self.HRNorm)
        return ["ThickLens: %s{" % str(self.Ref),
        "Thick: %scm" % str(self.Thick/cm),
        "Diameter: %scm" % str(self.Dia/cm) ,
        "Center: %s" % str(self.HRCenter),
        "Norm: (%s, %s)deg" % (str(sph[0]/deg), str(sph[1]/deg)),
        "Index: %s" % str(self.N),
        "HRKurv, ARKurv: %s, %s" % (str(self.HRK), str(self.ARK)),
        "R, T: %s, %s" % (str(self.HRr),str(self.HRt)),
        "}"]
