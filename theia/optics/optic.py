'''Defines the Optic class for theia.'''

# Provides:
#   class Optic
#       __init__
#       isHitDics
#       isHit
#       hit
#       hitHR
#       hitAR
#       hitSide
#       apexes
#       collision
#       geoCheck
#       translate

import numpy as np
from ..helpers import settings, geometry
from ..helpers.tools import shortRef
from .component import SetupComponent
from .beam import GaussianBeam

class Optic(SetupComponent):
    '''

    Optic class.

    This class is a base class for optics which may interact with Gaussian
    beams and return transmitted and reflected beams (mirrors, lenses, etc.)

    The way an optic interacts with a beam (if it adds to the order of a beam
    upon reflection or transmission on HR or AR etc) is specified by the
    action integers RonHR, TonHR, RonAR, TonAR of the optic. A beam which
    reflects on HR will have its order increased by RonHR, etc.

    All the optics which transmit or reflect beams (beam splitters, mirrors,
    thin and thick lenses and special optics) inherit from this class. A
    particular type of optic is characterized by its action integers and by the
    inputs provided to the constructors by the users. Everything else of the
    optics follow the shape of this Optic class.


    *=== Attributes ===*
    SetupCount (inherited): class attribute, counts all setup components.
        [integer]
    OptCount: class attribute, counts optical components. [integer]
    Name: class attribute. [string]
    HRCenter (inherited): center of the 'chord' of the HR surface. [3D vector]
    ARCenter (inherited): center of the 'chord' of the AR surface. [3D vector]
    HRNorm (inherited): unitary normal to the 'chord' of the HR (always pointing
     towards the outside of the component). [3D vector]
    Thick (inherited): thickness of the optic, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
    Ref (inherited): reference string (for keeping track with the lab). [string]
    ARNorm: unitary normal to the 'chord' of the AR (always pointing
     towards the outside of the component). [3D vector]
    N: refraction index of the material. [float]
    HRK, ARK: curvature of the HR, AR surfaces. [float]
    HRr, HRt, ARr, ARt: power reflectance and transmission coefficients of
        the HR and AR surfaces. [float]
    KeepI: whether of not to keep data of rays for interference calculations
            on the HR. [boolean]
    Wedge: wedge angle on the optic. [float]
    Alpha: angle of the rotation to describe the orientation of the wedge.
        See the documentation for details on this angle. [float]
    TonHR, RonHR, TonAR, RonAR: amount by which the orders of the beams will
        be increased upon reflection or transmission on AR or HR surfaces.
        These are the principal parameters which distinguish mirrors and lenses
        and beamsplitters, etc.

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

    def __init__(self, ARCenter, HRCenter, HRNorm, ARNorm, N, HRK, ARK, ARr,
                ARt, HRr, HRt, KeepI, Thickness, Diameter, Wedge, Alpha,
                RonHR, TonHR, RonAR, TonAR, Ref):
        '''Optic base initializer.

        Parameters are the attributes of the object to construct.

        Returns an Optic.

        '''
        # allow empty initializer
        if Ref is None:
            Ref = "Opt" + str(Optic.OptCount)

        # initialize with input data
        self.ARNorm = ARNorm
        self.N = N
        self.HRK = HRK
        self.ARK = ARK
        self.HRr = HRr
        self.HRt = HRt
        self.ARr = ARr
        self.ARt = ARt
        self.KeepI = KeepI
        self.Wedge = Wedge
        self.Alpha = Alpha
        self.RonHR = RonHR
        self.TonHR = TonHR
        self.RonAR = RonAR
        self.TonAR = TonAR

        #call mother initializer
        super(Optic, self).__init__(HRCenter = HRCenter, HRNorm = HRNorm,
                Ref = Ref, Thickness = Thickness,
                Diameter = Diameter, ARCenter = ARCenter)
        Optic.OptCount = Optic.OptCount + 1

    def isHitDics(self, beam):
        '''Determine the dictionaries to evaluate if a beam hits the optic.

        Uses the line***Inter functions from the geometry module to calculate
        the dictionaries of data on interaction with HR and AR and side of
        optics.

        Returns a tuple of 3 dictionaries with keys:
            'isHit': whether the optic is hit by the beam. [bool]
            'intersection point': 3D point where the beam impacts.
                [3D np-array]
            'distance': distance from beam origin to interaction point. [float]
        '''

        # get impact parameters on HR, AR and side:
        if np.abs(self.HRK) > 0.:
            HRDict = geometry.lineSurfInter(beam.Pos,
                                        beam.Dir, self.HRCenter,
                                        self.HRK*self.HRNorm/np.abs(self.HRK),
                                        np.abs(self.HRK),
                                        self.Dia)
        else:
            HRDict = geometry.linePlaneInter(beam.Pos, beam.Dir, self.HRCenter,
                                        self.HRNorm, self.Dia)

        if np.abs(self.ARK) > 0.:
            ARDict = geometry.lineSurfInter(beam.Pos,
                                        beam.Dir, self.ARCenter,
                                        self.ARK*self.ARNorm/np.abs(self.ARK),
                                        np.abs(self.ARK),
                                        self.Dia/np.cos(self.Wedge))
        else:
            ARDict = geometry.linePlaneInter(beam.Pos, beam.Dir, self.ARCenter,
                                        self.ARNorm,
                                        self.Dia/np.cos(self.Wedge))

        SideDict = geometry.lineCylInter(beam.Pos, beam.Dir,
                                    self.HRCenter, self.HRNorm,
                                    self.Thick, self.Dia)

        return HRDict, ARDict, SideDict

    def isHit(self, beam):
        '''Determine if a beam hits the Optic.

        This is a function uses the dictionaries provided by isHitDics to
        find the closest face hit by the beam.

        beam: incoming beam. [GaussianBeam]

        Returns a dictionary with keys:
            'isHit': whether the beam hits the optic. [boolean]
            'intersection point': point in space where it is first hit.
                    [3D vector]
            'face': to indicate which face is first hit, can be 'HR', 'AR' or
                'Side'. [string]
            'distance': geometrical distance from beam origin to impact. [float]

        '''

        # Get isHit dictionaries
        HRDict, ARDict, SideDict = self.isHitDics(beam)

        # face tags
        HRDict['face'] = 'HR'
        ARDict['face'] = 'AR'
        SideDict['face'] = 'Side'

        # determine first hit
        hitFaces = filter(lambda dic: dic['isHit'], [HRDict, ARDict, SideDict])

        if len(hitFaces) == 0:
            return {'isHit': False,
                    'intersection point': np.array([0., 0., 0.],
                                                dtype=np.float64),
                    'face': None,
                    'distance': 0.}

        ans = hitFaces[0]
        for dic in hitFaces:
            if dic['distance'] < ans['distance']:
                ans = dic

        return {'isHit': True,
                'intersection point': ans['intersection point'],
                'face': ans['face'],
                'distance': ans['distance']
                }

    def hit(self, beam, order, threshold):
        '''Compute the refracted and reflected beams after interaction.

        The beams returned are those selected after the order and threshold
        criterion.

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

        return {
            'HR': lambda beam: self.hitHR(beam,
                                dic['intersection point'], order, threshold),
            'AR': lambda beam: self.hitAR(beam,
                                dic['intersection point'], order, threshold),
            'Side': lambda beam: self.hitSide(beam)
                }[dic['face']](beam)

    def hitHR(self, beam, point, order, threshold):
        '''Compute the daughter beams after interaction on HR at point.

        beam: incident beam. [GaussianBeam]
        point: point in space of interaction. [3D vector]
        order: maximum strayness of daughter beams, which are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionary of beams with keys:
            't': refracted beam. [GaussianBeam]
            'r': reflected beam. [GaussianBeam]

        '''
        ans = dict()

        # Reference to beam according to settings
        BRef = beam.Ref if not settings.short else shortRef(beam.Ref)

        # Calculate the local normal in opposite direction
        if self.HRK == 0.:
            localNorm = self.HRNorm
        else:#undertending angle
            theta = np.arcsin(self.Dia * self.HRK/2.)\
                if np.abs(self.Dia * self.HRK/2.) < 1. else np.pi/2.

            sphereC = self.HRCenter + np.cos(theta)*self.HRNorm/self.HRK
            localNorm = (sphereC - point)/np.linalg.norm(sphereC - point)

        if np.dot(beam.Dir, localNorm) > 0.:
            localNorm = - localNorm
            K = np.abs(self.HRK)
        else:
            K = -np.abs(self.HRK)

        # determine whether we're entering or exiting the substrate
        if np.dot(beam.Dir, self.HRNorm) < 0.:
            #entering
            n1 = beam.N
            n2 = self.N
        else:
            #exiting
            n1 = self.N
            n2 = 1.

        # daughter directions
        dir2 = geometry.newDir(beam.Dir, localNorm, n1, n2)

        #warn on total reflection
        if dir2['TR'] and settings.info \
                and (beam.N == 1. or not settings.short):
            print "theia: Info: Total reflection of %s on HR of %s." \
                    % (BRef, self.Ref)

        # if there is no refracted
        if beam.P * self.HRt < threshold\
                or beam.StrayOrder + self.TonHR > order or dir2['t'] is None:
            ans['t'] = None

        # if there is no reflected
        if beam.P * self.HRr < threshold\
                or beam.StrayOrder + self.RonHR > order:
            ans['r'] = None

        # we're done if there are two Nones
        if len(ans) == 2:
            #warn if its due to power
            if settings.info\
                    and (beam.P * self.HRt < threshold\
                    or beam.P * self.HRr < threshold)\
                    and (beam.N == 1. or not settings.short):
                print ("theia: Info: Reached power threshold by interaction"\
                +" (%s on %s, HR).") %(BRef, self.Ref)
            return ans

        # Calculate new basis
        if not 'r' in ans:   # for reflected
            Uxr, Uyr = geometry.basis(dir2['r'])
            Uzr = dir2['r']

        if not 't' in ans:   # for refracted
            Uxt, Uyt = geometry.basis(dir2['t'])
            Uzt = dir2['t']

        Lx, Ly = geometry.basis(localNorm)

        # Calculate daughter curv tensors
        d = np.linalg.norm(point - beam.Pos)
        C = np.array([[K, 0.], [0, K]])
        Ki = np.array([[np.dot(beam.U[0], Lx), np.dot(beam.U[0], Ly)],
                        [np.dot(beam.U[1], Lx), np.dot(beam.U[1], Ly)]])
        Qi = beam.Q(d)
        Kit = np.transpose(Ki)
        Xi = np.dot(np.dot(Kit, Qi), Ki)

        if not 't' in ans:
            Kt = np.array([[np.dot(Uxt, Lx), np.dot(Uxt, Ly)],
                        [np.dot(Uyt, Lx), np.dot(Uyt, Ly)]])
            Ktt = np.transpose(Kt)
            Ktinv = np.linalg.inv(Kt)
            Kttinv = np.linalg.inv(Ktt)
            Xt = (np.dot(localNorm, beam.Dir) -n2*np.dot(localNorm, Uzt)/n1) * C
            Qt = n1*np.dot(np.dot(Kttinv, Xi - Xt), Ktinv)/n2

        if not 'r' in ans:
            Kr = np.array([[np.dot(Uxr, Lx), np.dot(Uxr, Ly)],
                        [np.dot(Uyr, Lx), np.dot(Uyr, Ly)]])
            Krt = np.transpose(Kr)
            Krinv = np.linalg.inv(Kr)
            Krtinv = np.linalg.inv(Krt)
            Xr = (np.dot(localNorm, beam.Dir) - np.dot(localNorm, Uzr)) * C
            Qr = np.dot(np.dot(Krtinv, Xi - Xr), Krinv)

        # Create new beams
        if not 'r' in ans:
            ans['r'] = GaussianBeam(Q = Qr,
                    Pos = point, Dir = Uzr, Ux = Uxr, Uy = Uyr,
                    N = n1, Wl = beam.Wl, P = beam.P * self.HRr,
                    StrayOrder = beam.StrayOrder + self.RonHR,
                    Ref = beam.Ref + 'r',
                    Optic = self.Ref, Face = 'HR',
                    Length = 0., OptDist = 0.)

        if not 't' in ans:
            ans['t'] = GaussianBeam(Q = Qt, Pos = point,
                Dir = Uzt, Ux = Uxt, Uy = Uyt, N = n2, Wl = beam.Wl,
                P = beam.P * self.HRt,
                StrayOrder = beam.StrayOrder + self.TonHR,
                Ref = beam.Ref + 't', Optic = self.Ref, Face = 'HR',
                Length = 0., OptDist = 0.)

        return ans

    def hitAR(self, beam, point, order, threshold):
        '''Compute the daughter beams after interaction on AR at point.

        beam: incident beam. [GaussianBeam]
        point: point in space of interaction. [3D vector]
        order: maximum strayness of daughter beams, which are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionary of beams with keys:
            't': refracted beam. [GaussianBeam]
            'r': reflected beam. [GaussianBeam]

        '''

        ans = dict()

        # Reference according to settings
        BRef = beam.Ref if not settings.short else shortRef(beam.Ref)

        # Calculate the local normal
        if self.ARK == 0.:
            localNorm = self.ARNorm
        else:   #undertending angle
            theta = np.arcsin(self.Dia * self.ARK/2.)\
                if np.abs(self.Dia * self.ARK/2.) < 1. else pi/2.

            sphereC = self.ARCenter + np.cos(theta)*self.ARNorm/self.ARK
            localNorm = (sphereC - point)/np.linalg.norm(sphereC - point)

        if np.dot(beam.Dir, localNorm) > 0.:
            localNorm = - localNorm
            K = np.abs(self.ARK)
        else:
            K = - np.abs(self.ARK)
        # determine whether we're entering or exiting the substrate
        if np.dot(beam.Dir, self.ARNorm) < 0.:
            #entering
            n1 = beam.N
            n2 = self.N
        else:
            #exiting
            n1 = self.N
            n2 = 1.

        # daughter directions
        dir2 = geometry.newDir(beam.Dir, localNorm, n1, n2)

        #warn on total reflection
        if dir2['TR'] and settings.info\
                and (beam.N == 1. or not settings.short):
            print "theia: Info: Total reflection of %s on AR of %s." \
                    % (BRef, self.Ref)

        # if there is no refracted
        if beam.P * self.ARt < threshold\
            or beam.StrayOrder + self.TonAR > order or dir2['t'] is None:
            ans['t'] = None

        # if there is no reflected
        if beam.P * self.ARr < threshold\
            or beam.StrayOrder + self.RonAR > order:
            ans['r'] = None

        # we're done if there are two Nones
        if len(ans) == 2:
            if settings.info and (beam.N == 1. or not settings.short):
                print ("theia: Info: Reached leaf of tree by interaction"\
                +" (%s on %s, HR).") % (BRef, self.Ref)
            return ans

        # Calculate new basis
        if not 'r' in ans:   # for reflected
            Uxr, Uyr = geometry.basis(dir2['r'])
            Uzr = dir2['r']

        if not 't' in ans:   # for refracted
            Uxt, Uyt = geometry.basis(dir2['t'])
            Uzt = dir2['t']

        Lx, Ly = geometry.basis(localNorm)

        # Calculate daughter curv tensors
        d = np.linalg.norm(point - beam.Pos)
        C = np.array([[K, 0.], [0, K]])
        Ki = np.array([[np.dot(beam.U[0], Lx), np.dot(beam.U[0], Ly)],
                        [np.dot(beam.U[1], Lx), np.dot(beam.U[1], Ly)]])
        Qi = beam.Q(d)
        Kit = np.transpose(Ki)
        Xi = np.dot(np.dot(Kit, Qi), Ki)

        if not 't' in ans:
            Kt = np.array([[np.dot(Uxt, Lx), np.dot(Uxt, Ly)],
                            [np.dot(Uyt, Lx), np.dot(Uyt, Ly)]])
            Ktt = np.transpose(Kt)
            Ktinv = np.linalg.inv(Kt)
            Kttinv = np.linalg.inv(Ktt)
            Xt = (np.dot(localNorm, beam.Dir) -n2*np.dot(localNorm, Uzt)/n1) * C
            Qt = n1*np.dot(np.dot(Kttinv, Xi - Xt), Ktinv)/n2

        if not 'r' in ans:
            Kr = np.array([[np.dot(Uxr, Lx), np.dot(Uxr, Ly)],
                            [np.dot(Uyr, Lx), np.dot(Uyr, Ly)]])
            Krt = np.transpose(Kr)
            Krinv = np.linalg.inv(Kr)
            Krtinv = np.linalg.inv(Krt)
            Xr = (np.dot(localNorm, beam.Dir) - np.dot(localNorm, Uzr)) * C
            Qr = np.dot(np.dot(Krtinv, Xi - Xr), Krinv)

        # Create new beams
        if not 'r' in ans:
            ans['r'] = GaussianBeam(Q = Qr,
                Pos = point, Dir = Uzr, Ux = Uxr, Uy = Uyr,
                N = n1, Wl = beam.Wl, P = beam.P * self.ARr,
                StrayOrder = beam.StrayOrder + self.RonAR,
                Ref = beam.Ref + 'r',
                Optic = self.Ref, Face = 'AR',
                Length = 0., OptDist = 0.)

        if not 't' in ans:
            ans['t'] = GaussianBeam(Q = Qt, Pos = point,
                Dir = Uzt, Ux = Uxt, Uy = Uyt, N = n2, Wl = beam.Wl,
                P = beam.P * self.ARt,
                StrayOrder = beam.StrayOrder + self.TonAR,
                Ref = beam.Ref + 't', Optic = self.Ref, Face = 'AR',
                Length = 0., OptDist = 0.)

        return ans

    def hitSide(self, beam):
        '''Compute the daughter beams after interaction on Side at point.

        Generic function: all sides stop beams.

        beam: incident beam. [GaussianBeam]

        Returns {'t': None, 'r': None}

        '''
        if settings.info  and (beam.N == 1. or not settings.short):
            print ("theia: Info: Reached leaf of tree by interaction "\
            +"(%s on %s, Side).") %(beam.Ref\
                if not settings.short else shortRef(beam.Ref), self.Ref)
        return {'t': None, 'r': None}

    def apexes(self):
        '''Returns the positions of the apexes of HR and AR as a tuple.'''
        if self.HRK == 0.:
            apex1 = self.HRCenter
        else:
            theta1 = np.arcsin(self.Dia * self.ARK/2.)\
                if np.abs(self.Dia * self.ARK/2.) < 1. else np.pi/2.
            apex1 = self.HRCenter - (1-np.cos(theta1))*self.HRNorm/self.HRK

        if self.ARK == 0.:
            apex2 = self.ARCenter
        else:
            theta2 = np.arcsin(self.Dia * self.ARK/(2.*np.cos(self.Wedge)))\
                if np.abs(self.Dia * self.ARK/(2.*np.cos(self.Wedge))) < 1.\
                else np.pi/2.
            apex2 = self.ARCenter - (1-np.cos(theta2))*self.ARNorm/self.ARK

        return apex1, apex2

    def collision(self):
        '''Determine whether the HR and AR surfaces intersect.

        Returns True if there is an intersection, False if not.

        '''

        if self.ARK <= 0. and self.HRK <= 0.:
            # no collision if negative curvatures
            return False

        apex = self.apexes()

        #vector from apex1 to apex2
        vec = apex[1] - apex[0]

        return np.dot(vec, self.HRNorm) > 0.

    def geoCheck(self, word):
        '''Makes geometrical checks on surfaces and warns when necessary.'''

        if self.HRt + self.HRr > 1.:
            print "theia: Warning: In %s %s on HR, R + T > 1." %(word, self.Ref)

        if self.ARt + self.ARr > 1.:
            print "theia: Warning: In %s %s on AR, R + T > 1." %(word, self.Ref)

        if self.N < 1.:
            print "theia: Warning: In %s %s, optical index < 1."\
                    % (word, self.Ref)

        if self.HRK != 0. and np.abs(1./self.HRK) < self.Dia/2.:
            print ("theia: Warning: In %s, the diameter of the %s exceeds the"\
            + " diameter of the HR surface.") % (self.Ref, word)

        if self.ARK != 0. and np.abs(1./self.ARK) < self.Dia/2.:
            print ("theia: Warning: In %s, the diameter of the %s exceeds the"\
            + " diameter of the AR surface.") % (self.Ref, word)

        if self.collision():
            print "theia: Warning: In %s, HR and AR surfaces intersect."\
            %self.Ref

    def translate(self, X = 0., Y = 0., Z = 0.):
        '''Move the optic to (current position + (X, Y, Z)).

        This version takes care of HRcenter and ARCenter and overwrites the
        SetupComponent version.

        X, Y, Z: components of the translation vector.

        No return value.
        '''
        self.HRCenter = self.HRCenter + np.array([X, Y, Z], dtype = np.float64)
        self.ARCenter = self.ARCenter + np.array([X, Y, Z], dtype = np.float64)
