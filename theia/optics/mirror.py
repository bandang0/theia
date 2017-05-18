'''Defines the Mirror class for theia.'''

# Provides:
#   class Mirror
#       __init__
#       lineList
#       hit
#       hitHR
#       hitAR

import numpy as np
from helpers import geometry, settings
from helpers.units import *
from helpers.tools import hitTrue
from optic import Optic
from optics.beam import GaussianBeam as gbeam


class Mirror(Optic):
    '''

    Mirror class.

    This class represents semi reflective mirrors composed of two faces (HR, AR)
    and with a wedge angle. These are the objects with which the beams will
    interqct during the ray tracing. Please see the documentation for details
    on the geometric construction of these mirrors.

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
    Wedge: wedge angle of the mirror, please refer to the documentation for
        detaild on the geometry of mirrors and their implementation here.
        [float]
    Alpha: rotation alngle used in the geometrical construction of the mirror
        (see doc). [float]

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

    def __init__(self, Wedge = 0., Alpha = 0., X = 0. ,Y = 0., Z = 0.,
                Theta = 0., Phi = 0., Diameter = None,
                HRr = None, HRt = None, ARr = None, ARt = None,
                HRK = None, ARK = None, Thickness = None,
                N = None, KeepI = None, Name = None, Ref = None):
        '''Mirror constructor.

        Parameters are the attributes and the angles theta and phi are spherical
        coordinates of HRNorm.

        Returns a mirror.

        '''

        if Wedge is None:
            Wedge = 0.
        if Alpha is None:
            Alpha = 0.
        if Theta is None:
            Theta = 0.
        if Phi is None:
            Phi = 0.
        if Name is None:
            Name = "Mirror"

        Norm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        super(Mirror, self).__init__(ARCenter = None, ARNorm = None, N = N,
            HRK = HRK, ARK = ARK, ARr = ARr, ARt = ARt, HRr = HRr, HRt = HRt,
        KeepI = KeepI, HRCenter = [X, Y, Z], HRNorm = Norm,
        Thickness = Thickness, Diameter = Diameter, Name = Name, Ref = Ref)

        # Keep the constructor data for outputting
        self.Wedge = float(Wedge)
        self.Alpha = float(Alpha)

        #Calculate ARCenter and ARNorm with wedge and alpha and thickness:
        self.ARCenter = self.HRCenter\
            - (self.Thick + .5*np.tan(self.Wedge)*self.Dia)*self.HRNorm

        a,b = geometry.basis(self.HRNorm)
        self.ARNorm = -np.cos(self.Wedge) * self.HRNorm\
                        + np.sin(self.Wedge)*(- np.sin(self.Alpha) * a\
                                            + np.cos(self.Alpha) * b)\

        #Warnings for console output
        if settings.warning:
            self.geoCheck("mirror")

    def lineList(self):
        '''Returns the list of lines necessary to print the object.
        '''
        ans = []
        ans.append("Mirror: " + self.Name + " (" + str(self.Ref) + ") {")
        ans.append("Thick: " + str(self.Thick/cm) + "cm")
        ans.append("Diameter: " + str(self.Dia/cm) + "cm")
        ans.append("Wedge: " + str(self.Wedge/deg) + "deg")
        ans.append("Alpha: " + str(self.Alpha/deg) + "deg")
        ans.append("HRCenter: " + str(self.HRCenter))
        ans.append("HRNorm: " + str(self.HRNorm))
        ans.append("Index: " + str(self.N))
        ans.append("HRKurv, ARKurv: " + str(self.HRK) + ", " + str(self.ARK))
        ans.append("HRr, HRt, ARr, ARt: " +str(self.HRr) + ", " + str(self.HRt)\
            + ", " + str(self.ARr) + ", " + str(self.ARt) )
        ans.append("}")

        return ans

    def isHit(self, beam):
        '''Determine if a beam hits the Optic.

        This is a function for mirrors, using their geometrical
        attributes. This uses the line***Inter functions from the geometry
        module to find characteristics of impact of beams on mirrors.

        beam: incoming beam. [GaussianBeam]

        Returns a dictionary with keys:
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
                                        self.ARNorm, self.Dia)

        SideDict = geometry.lineCylInter(beam.Pos, beam.Dir,
                                    self.HRCenter, self.HRNorm,
                                    self.Thick, self.Dia)

        # face tags
        HRDict['face'] = 'HR'
        ARDict['face'] = 'AR'
        SideDict['face'] = 'Side'


        # determine first hit
        hitFaces = filter(hitTrue, [HRDict, ARDict, SideDict])

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

    def hit(self, beam, order, threshold):
        '''Compute the refracted and reflected beams after interaction.

        The beams returned are those selected after the order and threshold
        criterion.

        beam: incident beam. [GaussianBeam]
        order: maximum strayness of daughter beams, whixh are not returned if
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

        if dic['face'] == 'HR':
            return self.hitHR(beam, dic['intersection point'], order, threshold)
        elif dic['face'] == 'AR':
            return self.hitAR(beam, dic['intersection point'], order, threshold)
        else:
            return self.hitSide(beam)


    def hitHR(self, beam, point, order, threshold):
        '''Compute the daughter beams after interaction on HR at point.

        beam: incident beam. [GaussianBeam]
        point: point in space of interaction. [3D vector]
        order: maximum strayness of daughter beams, whixh are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionary of beams with keys:
            't': refracted beam. [GaussianBeam]
            'r': reflected beam. [GaussianBeam]

        '''

        ans = {}
        d = np.linalg.norm(point - beam.Pos)

        # Calculate the local normal in opposite direction
        if self.HRK == 0.:
            localNorm = self.HRNorm
        else:
            # normal pointing to center of the sphere
            nor = self.HRK * self.HRNorm/np.abs(self.HRK)

            # center of sphere:
            try:
                theta = np.arcsin(self.Dia * self.HRK/2.)   #undertending angle
            except FloatingPointError:
                theta = np.pi/2.
            sphereC = self.HRCenter + np.cos(theta)*nor/self.HRK
            localNorm = sphereC - point
            localNorm = localNorm/np.linalg.norm(localNorm)

        if np.dot(beam.Dir, localNorm) > 0.:
            localNorm = - localNorm

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
        if dir2['TR'] and settings.info:
            print "theia: Info: Total reflection occured on "\
            + "HR face of " + self.Name + " (" + self.Ref + ") by beam "\
            + beam.Name + "."


        # if there is no refracted
        if beam.P * self.HRt < threshold or beam.StrayOrder + 1 > order\
                                        or dir2['t'] is None:
            ans['t'] = None

        # if there is no reflected
        if beam.P * self.HRr < threshold:
            ans['r'] = None

        # we're done if there are two Nones
        if len(ans) == 2:
            if settings.info:
                print "theia: Info: Reached end node of tree by interaction"\
                + " on HR face of " +self.Name + " (" + self.Ref + ") of beam "\
                + beam.Name + "."
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
        C = -np.array([[self.HRK, 0.], [0, self.HRK]])
        Ki = np.array([[np.dot(beam.U[0], Lx), np.dot(beam.U[0], Ly)],
                        [np.dot(beam.U[1], Lx), np.dot(beam.U[1], Ly)]])
        Qi = beam.Q(d)
        Kit = np.transpose(Ki)
        Xi = np.matmul(np.matmul(Kit, Qi), Ki)

        if not 't' in ans:
            Kt = np.array([[np.dot(Uxt, Lx), np.dot(Uxt, Ly)],
                        [np.dot(Uyt, Lx), np.dot(Uyt, Ly)]])
            Ktt = np.transpose(Kt)
            Ktinv = np.linalg.inv(Kt)
            Kttinv = np.linalg.inv(Ktt)
            Xt = (np.dot(localNorm, beam.Dir) -n2*np.dot(localNorm, Uzt)/n1) * C
            Qt = n1*np.matmul(np.matmul(Kttinv, Xi - Xt), Ktinv)/n2

        if not 'r' in ans:
            Kr = np.array([[np.dot(Uxr, Lx), np.dot(Uxr, Ly)],
                        [np.dot(Uyr, Lx), np.dot(Uyr, Ly)]])
            Krt = np.transpose(Kr)
            Krinv = np.linalg.inv(Kr)
            Krtinv = np.linalg.inv(Krt)
            Xr = (np.dot(localNorm, beam.Dir) - np.dot(localNorm, Uzr)) * C
            Qr = np.matmul(np.matmul(Krtinv, Xi - Xr), Krinv)

        # Create new beams
        if not 'r' in ans:
            ans['r'] = gbeam(ortho = False, Q = Qr,
                    Pos = point, Dir = Uzr, Ux = Uxr, Uy = Uyr,
                    N = n1, Wl = beam.Wl, P = beam.P * self.HRr,
                    StrayOrder = beam.StrayOrder, Ref = beam.Ref + 'r')

        if not 't' in ans:
            ans['t'] = gbeam(ortho = False, Q = Qt, Pos = point,
                Dir = Uzt, Ux = Uxt, Uy = Uyt, N = n2, Wl = beam.Wl,
                P = beam.P * self.HRt, StrayOrder = beam.StrayOrder + 1,
                Ref = beam.Ref + 't')

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

        ans = {}
        d = np.linalg.norm(point - beam.Pos)

        # Calculate the local normal
        if self.ARK == 0.:
            localNorm = self.ARNorm
        else:
            # normal pointing to center of the sphere
            nor = self.ARK * self.ARNorm/np.abs(self.ARK)

            # center of sphere:
            try:
                theta = np.arcsin(self.Dia * self.ARK/2.)   #undertending angle
            except FloatingPointError:
                theta = np.pi/2.
            sphereC = self.ARCenter + np.cos(theta)*nor/self.ARK
            localNorm = sphereC - point
            localNorm = localNorm/np.linalg.norm(localNorm)

        if np.dot(beam.Dir, localNorm) > 0.:
            localNorm = - localNorm

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
        if dir2['TR']:
            if settings.info:
                print "theia: Info: Total reflection occured on "\
                + "AR face of " + self.Name + " (" + self.Ref + ") by beam "\
                + beam.Name + "."

        # if there is no refracted
        if beam.P * self.ARt < threshold or dir2['t'] is None:
            ans['t'] = None

        # if there is no reflected
        if beam.P * self.ARr < threshold or beam.StrayOrder + 1 > order:
            ans['r'] = None

        # we're done if there are two Nones
        if len(ans) == 2:
            if settings.info:
                print "theia: Info: Reached end node of tree by interaction "\
                + "on AR face of " + self.Name + " (" + self.Ref + ") of beam "\
                + beam.Name + "."
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
        C = -np.array([[self.ARK, 0.], [0, self.ARK]])
        Ki = np.array([[np.dot(beam.U[0], Lx), np.dot(beam.U[0], Ly)],
                        [np.dot(beam.U[1], Lx), np.dot(beam.U[1], Ly)]])
        Qi = beam.Q(d)
        Kit = np.transpose(Ki)
        Xi = np.matmul(np.matmul(Kit, Qi), Ki)

        if not 't' in ans:
            Kt = np.array([[np.dot(Uxt, Lx), np.dot(Uxt, Ly)],
                            [np.dot(Uyt, Lx), np.dot(Uyt, Ly)]])
            Ktt = np.transpose(Kt)
            Ktinv = np.linalg.inv(Kt)
            Kttinv = np.linalg.inv(Ktt)
            Xt = (np.dot(localNorm, beam.Dir) -n2*np.dot(localNorm, Uzt)/n1) * C
            Qt = n1*np.matmul(np.matmul(Kttinv, Xi - Xt), Ktinv)/n2

        if not 'r' in ans:
            Kr = np.array([[np.dot(Uxr, Lx), np.dot(Uxr, Ly)],
                            [np.dot(Uyr, Lx), np.dot(Uyr, Ly)]])
            Krt = np.transpose(Kr)
            Krinv = np.linalg.inv(Kr)
            Krtinv = np.linalg.inv(Krt)
            Xr = (np.dot(localNorm, beam.Dir) - np.dot(localNorm, Uzr)) * C
            Qr = np.matmul(np.matmul(Krtinv, Xi - Xr), Krinv)

        # Create new beams
        if not 'r' in ans:
            ans['r'] = gbeam(ortho = False, Q = Qr,
                    Pos = point, Dir = Uzr, Ux = Uxr, Uy = Uyr,
                    N = n1, Wl = beam.Wl, P = beam.P * self.ARr,
                    StrayOrder = beam.StrayOrder + 1, Ref = beam.Ref + 'r')

        if not 't' in ans:
            ans['t'] = gbeam(ortho = False, Q = Qt, Pos = point,
                Dir = Uzt, Ux = Uxt, Uy = Uyt, N = n2, Wl = beam.Wl,
                P = beam.P * self.ARt, StrayOrder = beam.StrayOrder,
                Ref = beam.Ref + 't')

        return ans
