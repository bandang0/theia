'''Defines the ThinLens class for theia.'''

# Provides:
#   class ThinLens
#       __init__
#       lines

import numpy as np
from ..helpers import settings
from ..helpers.units import mm, cm, deg, pi
from ..helpers.geometry import rectToSph
from .optic import Optic

class ThinLens(Optic):
    '''

    ThinLens class.

    This class represents thin lenses, which are specified only by their focal
    lengths, diameter, position and orientation. Only the initializer and the
    printing distinguishes thin lenses (in implementation) from other lenses.

    Actions:
        * T on HR: 0
        * R on HR: + 1
        * T on AR: 0
        * R on AR: + 1

    *=== Additional attributes with respect to the Optic class ===*

    Focal: focal length of the lens  as given in initializer. [float]

    *=== Name ===*

    ThinLens

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

    Name = "ThinLens"

    def __init__(self, Focal = 10.e-2, KeepI = False, Theta = pi/2., Phi = 0.,
                Diameter = 5.e-2, R = .1, T = .9,
                X = 0., Y = 0., Z = 0., Ref = None):
        '''ThinLens initializer.

        Parameters are the attributes.

        Returns a ThinLens.

        '''
        # actions
        TonHR = 0
        RonHR = 1
        TonAR = 0
        RonAR = 1

        # initialize focal and check data
        self.Focal = float(Focal)
        Theta = float(Theta)
        Phi = float(Phi)
        Diameter = float(Diameter)
        R = float(R)
        T = float(T)
        Wedge = 0.
        Alpha = 0.

        #prepare for mother initializer
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
                theta = pi/2.
            Thickness = 2.*settings.zero + 2.*(1.-np.cos(theta))/HRK
        HRCenter = Center + Thickness*HRNorm/2.
        ARCenter = Center - Thickness*HRNorm/2.

        # initialize with lens mother initializer
        super(ThinLens, self).__init__(ARCenter = ARCenter, ARNorm = ARNorm,
                N = N,
                HRK = HRK, ARK = ARK,
                ARr = R, ARt = T, HRr = R, HRt = T, KeepI = KeepI,
                HRCenter = HRCenter, HRNorm = HRNorm, Thickness = Thickness,
                Diameter = Diameter, Wedge = Wedge, Alpha = Alpha,
                TonHR = TonHR, RonHR = RonHR, TonAR = TonAR, RonAR = RonAR,
                Ref = Ref)

        #warns on geometry
        if settings.warning:
            self.geoCheck("thinlens")

    def lines(self):
        '''Returns the list of lines necessary to print the object.
        '''
        sph = rectToSph(self.HRNorm)
        return ["ThinLens: %s {" % str(self.Ref),
        "Diameter: %scm" % str(self.Dia/cm),
        "Focal: %smm" % str(self.Focal/mm),
        "Center: %s" % str(self.HRCenter),
        "Norm: (%s, %s)deg" % (str(sph[0]/deg), str(sph[1]/deg)),
        "HRKurv, ARKurv: %s, %s" % (str(self.HRK), str(self.ARK)),
        "R, T: %s, %s" % (str(self.HRr),str(self.HRt)),
        "}"]
