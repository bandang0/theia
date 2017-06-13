'''Defines the Optic class for theia.'''

# Provides:
#   class Optic
#       __init__
#       hitSide
#       collision
#       geoCheck

import numpy as np
from ..helpers import settings
from .component import SetupComponent

class Optic(SetupComponent):
    '''

    Optic class.

    This class is a base class for optics which may interact with Gaussian
    beams and return transmitted and reflected beams (mirrors, lenses, etc.)


    *=== Attributes ===*
    SetupCount (inherited): class attribute, counts all setup components.
        [integer]
    OptCount: class attribute, counts optical components. [integer]
    Name: class attribute. [string]
    HRCenter (inherited): center of the 'chord' of the HR surface. [3D vector]
    HRNorm (inherited): unitary normal to the 'chord' of the HR (always pointing
     towards the outside of the component). [3D vector]
    Thick (inherited): thickness of the optic, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
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
    Name = "Optic"

    def __init__(self, ARCenter, ARNorm, N, HRK, ARK, ARr, ARt, HRr,
                HRt, KeepI, HRCenter, HRNorm, Thickness, Diameter, Ref):
        '''Optic base initializer.

        Parameters are the attributes of the object to construct.

        Returns an Optic.

        '''
        # allow empty initializer
        if Ref is None:
            Ref = "Opt" + str(Optic.OptCount)

        # initialize with input data
        self.ARCenter = np.array(ARCenter, dtype = np.float64)
        self.ARNorm = np.array(ARNorm, dtype = np.float64)
        self.ARNorm = self.ARNorm/np.linalg.norm(self.ARNorm)
        self.N = N
        self.HRK = HRK
        self.ARK = ARK
        self.HRr = HRr
        self.HRt = HRt
        self.ARr = ARr
        self.ARt = ARt
        self.KeepI = KeepI

        #call mother initializer
        super(Optic, self).__init__(HRCenter = HRCenter, HRNorm = HRNorm,
                Ref = Ref, Thickness = Thickness,
                Diameter = Diameter)
        Optic.OptCount = Optic.OptCount + 1

    def hitSide(self, beam):
        '''Compute the daughter beams after interaction on Side at point.

        Generic function: all sides stop beams.

        beam: incident beam. [GaussianBeam]

        Returns {'t': None, 'r': None}

        '''
        if settings.info:
            print "theia: Info: Reached leaf of tree by interaction ("\
            + beam.Ref + " on " + self.Ref + ', ' + 'Side).'
        return {'t': None, 'r': None}

    def collision(self):
        '''Determine whether the HR and AR surfaces intersect.

        Returns True if there is an intersection, False if not.

        '''

        if self.ARK <= 0. and self.HRK <= 0.:
            # no collision if negative curvatures
            return False

        try:    # the arcsin may fail because dia/2. > ROC
            theta1 = np.arcsin(self.Dia * self.HRK/2.)  #semi angles

            if self.HRK == 0.:
                apex1 = self.HRcenter
            else:
                apex1 = self.HRCenter - (1-np.cos(theta1))*self.HRNorm/self.HRK

        except FloatingPointError:
            #if it fails then the whole semisphere is in the mirror and apex
            # is a radius away from Center.
            apex1 = self.HRCenter - self.HRNorm/self.HRK

        try:    #same
            theta2 = np.arcsin(self.Dia * self.ARK/2.)

            if self.ARK == 0.:
                apex2 = self.ARCenter
            else:
                apex2 = self.ARCenter - (1-np.cos(theta2))*self.ARNorm/self.ARK

        except FloatingPointError:
            apex2 = self.ARCenter - self.ARNorm/self.ARK
        #vector from apex1 to apex2
        vec = apex2 - apex1

        return np.dot(vec, self.HRNorm) > 0.

    def geoCheck(self, word):
        '''Makes geometrical checks on surfaces and warns when necessary.

        '''
        if self.HRt + self.HRr > 1.:
            print "theia: Warning: In " + word + " %s (%s) on HR, R + T > 1."\
                    %(self.Name, self.Ref)

        if self.ARt + self.ARr > 1.:
            print "theia: Warning: In " + word + " %s (%s) on AR, R + T > 1."\
                    %(self.Name, self.Ref)

        if self.N < 1.:
            print "theia: Warning: In " + word + " %s (%s), optical index < 1."\
                    %(self.Name, self.Ref)

        if self.HRK != 0. and np.abs(1./self.HRK) < self.Dia/2.:
            print "theia: Warning: In " + word + " %s (%s), the diameter of " \
                %(self.Name, self.Ref)\
                +"the "+word+" exceeds the diameter of the HR surface."\

        if self.ARK != 0. and np.abs(1./self.ARK) < self.Dia/2.:
            print "theia: Warning: In " + word + " %s (%s), the diameter of " \
                %(self.Name, self.Ref)\
                +"the "+word+" exceeds the diameter of the AR surface."\

        if self.collision():
            print "theia: Warning: In " + word + " %s (%s), HR and AR surfaces"\
                %(self.Name, self.Ref)\
                +" intersect."
