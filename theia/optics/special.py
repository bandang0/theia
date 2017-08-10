'''Defines the Special class for theia.'''

# Provides:
#   class Special
#       __init__
#       lines

import numpy as np
from ..helpers import geometry, settings
from ..helpers.units import deg, cm, pi
from .optic import Optic

class Special(Optic):
    '''

    Special class.

    This class represents general optics, as their actions on R and T are left
    to the user to input. They are useful for special optics which are neither
    reflective nor transmissive.

    Actions:
        * T on HR: user input
        * R on HR: user input
        * T on AR: user input
        * R on AR: user input

    **Note**: by default the actions of these objects are those of
    beamsplitters (0, 0, 0, 0)

    *=== Additional attributes with respect to the Optic class ===*

    None

    *=== Name ===*

    Special

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

    Name = "Special"
    def __init__(self, Wedge = 0., Alpha = 0., X = 0., Y = 0., Z = 0.,
                Theta = pi/2., Phi = 0., Diameter = 10.e-2,
                HRr = .99, HRt = .01, ARr = .1, ARt = .9,
                HRK = 0.01, ARK = 0, Thickness = 2.e-2,
                N = 1.4585, KeepI = False,
                RonHR = 0, TonHR = 0, RonAR = 0, TonAR = 0,
                Ref = None):
        '''Special optic initializer.

        Parameters are the attributes.

        Returns a special optic.

        '''
        # actions
        TonHR = int(TonHR)
        RonHR = int(RonHR)
        TonAR = int(TonAR)
        RonAR = int(RonAR)

        # Initialize input data
        N = float(N)
        Wedge = float(Wedge)
        Alpha = float(Alpha)
        Theta = float(Theta)
        Phi = float(Phi)
        Diameter = float(Diameter)
        Thickness = float(Thickness)
        HRK = float(HRK)
        ARK = float(ARK)
        HRt = float(HRt)
        HRr = float(HRr)
        ARt = float(ARt)
        ARr = float(ARr)

        #prepare for mother initializer
        HRNorm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        HRCenter = np.array([X, Y, Z], dtype = np.float64)

        #Calculate ARCenter and ARNorm with wedge and alpha and thickness:
        ARCenter = HRCenter\
            - (Thickness + .5 * np.tan(Wedge) * Diameter) * HRNorm

        a,b = geometry.basis(HRNorm)
        ARNorm = -np.cos(Wedge) * HRNorm\
                        + np.sin(Wedge) * (np.cos(Alpha) * a\
                                            + np.sin(Alpha) * b)

        super(Special, self).__init__(ARCenter = ARCenter, ARNorm = ARNorm,
        N = N, HRK = HRK, ARK = ARK, ARr = ARr, ARt = ARt, HRr = HRr, HRt = HRt,
        KeepI = KeepI, HRCenter = HRCenter, HRNorm = HRNorm,
        Thickness = Thickness, Diameter = Diameter,
        Wedge = Wedge, Alpha = Alpha,
        TonHR = TonHR, RonHR = RonHR, TonAR = TonAR, RonAR = RonAR,
        Ref = Ref)

        #Warnings for console output
        if settings.warning:
            self.geoCheck("mirror")

    def lines(self):
        '''Returns the list of lines necessary to print the object.'''
        sph = geometry.rectToSph(self.HRNorm)
        return ["Special: %s {" % str(self.Ref),
        "TonHR, RonHR: %s, %s" % (str(self.TonHR), str(self.RonHR)),
        "TonAR, RonAR: %s, %s" % (str(self.TonAR), str(self.RonAR)),
        "Thick: %scm" % str(self.Thick/cm),
        "Diameter: %scm" % str(self.Dia/cm),
        "Wedge: %sdeg" % str(self.Wedge/deg),
        "Alpha: %sdeg" % str(self.Alpha/deg),
        "HRCenter: %s" % str(self.HRCenter),
        "HRNorm: (%s, %s)deg" % (str(sph[0]/deg), str(sph[1]/deg)),
        "Index: %s" %str(self.N),
        "HRKurv, ARKurv: %s, %s" % (str(self.HRK), str(self.ARK)),
        "HRr, HRt, ARr, ARt: %s, %s, %s, %s" \
            % (str(self.HRr), str(self.HRt), str(self.ARr), str(self.ARt)),
        "}"]
