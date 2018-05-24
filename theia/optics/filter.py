'''Defines the Filter class for theia.'''

# Provides:
#   class Mirror
#       __init__
#       lines
#       hit

import numpy as np
from ..helpers import geometry, settings
from ..helpers.units import deg, cm, pi, nm
from .optic import Optic
from .beam import GaussianBeam

class Filter(Optic):
    '''

    Filter class.

    This class represents filters which transmit power only if the wavelength of
    the incoming beam and that of the filter match.

    Actions:
        * T on HR: 0
        * R on HR: 0
        * T on AR: 0
        * R on AR: 0

    *=== Additional attributes with respect to the Optic class ===*

    Wl: Passing wavelength of the filter. [float]

    *=== Name ===*

    Filter

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

    Name = "Filter"
    def __init__(self, X = 0., Y = 0., Z = 0.,
                Theta = pi/2., Phi = 0., Diameter = 1.e-1,
                Thickness = 2.e-2, Wl = 800 * nm, Ref = None):
        '''Mirror initializer.

        Parameters are the attributes.

        Returns a mirror.

        '''
        # actions
        TonHR = 0
        RonHR = 0
        TonAR = 0
        RonAR = 0

        # Initialize input data
        Theta = float(Theta)
        Phi = float(Phi)
        Diameter = float(Diameter)
        Thickness = float(Thickness)
        Wl = float(Wl)

        #prepare for mother initializer
        HRNorm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        HRCenter = np.array([X, Y, Z], dtype = np.float64)

        #Calculate ARCenter and ARNorm with wedge and alpha and thickness:
        ARCenter = HRCenter - Thickness * HRNorm
        ARNorm = - HRNorm

        super(Filter, self).__init__(ARCenter = ARCenter, ARNorm = ARNorm,
        N = 1., HRK = 0., ARK = 0., ARr = 0., ARt = 1., HRr = 0., HRt = 1.,
        KeepI = True, HRCenter = HRCenter, HRNorm = HRNorm,
        Thickness = Thickness, Diameter = Diameter,
        Wedge = 0., Alpha = 0.,
        TonHR = TonHR, RonHR = RonHR, TonAR = TonAR, RonAR = RonAR,
        Ref = Ref)

        #Warnings for console output
        if settings.warning:
            self.geoCheck("filter")

        self.Wl = Wl

    def lines(self):
        '''Returns the list of lines necessary to print the object.'''
        sph = geometry.rectToSph(self.HRNorm)

        return ["Filter: %s {" %str(self.Ref),
        "Wavelength : %snm" %str(self.Wl/nm),
        "Thick: %scm" %str(self.Thick/cm),
        "Diameter: %scm" %str(self.Dia/cm),
        "HRCenter: %s" %str(self.HRCenter),
        "HRNorm: (%s, %s)deg" % (str(sph[0]/deg), str(sph[1]/deg)),
        "}"]

    def hit(self, beam, order, threshold):
        '''Compute the refracted and reflected beams after interaction.

        In the case of filters, the transmitted beam is just the incoming beam
        if the wavelengths match, and None in any other case.

        beam: incident beam. [GaussianBeam]
        order: maximum strayness of daughter beams, which are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionary of beams with keys:
            't': refracted beam. [GaussianBeam]
            'r': reflected beam. [GaussianBeam]

        '''
        # get impact parameters and update beam
        dic = self.isHit(beam)
        beam.Length = dic['distance']
        beam.OptDist = beam.N * beam.Length
        beam.TargetOptic = self.Ref
        beam.TargetFace = dic['face']
        endSize = beam.width(beam.Length)
        beam.TWx = endSize[0]
        beam.TWy = endSize[1]

        if self.Wl != beam.Wl or dic['face'] == 'Side':
            return {'r': None, 't': None}

        return {'r': None,
                't': GaussianBeam(Q = beam.Q(beam.Length), #curvature
				            Pos = dic['intersection point'], # position
				            Dir = beam.Dir, Ux = beam.U[0], Uy = beam.U[1],
				            N = beam.N, Wl = beam.Wl, P = beam.P,
                            StrayOrder = beam.StrayOrder,
				            Ref = beam.Ref + 't',
                            Optic = self.Ref, Face = dic['face'],
				            Length = 0., OptDist = 0.)}
