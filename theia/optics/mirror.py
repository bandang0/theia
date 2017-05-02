'''Defines the Mirror class for theia.'''

# Provides:
#   class Mirror

import numpy as np
#from units import *
from component import OpticalComponent
from optics import geometry as geo
from optics import beam as gbeam
import helpers

class Mirror(OpticalComponent):
    '''

    Mirror class.

    This class represents semi reflective mirrors composed of two faces (HR, AR)
    and with a wedge angle. These are the objects with which the beams will
    interqct during the ray tracing. Please see the documentation for details
    on the geometric construction of these mirrors.

    *=== Attributes ===*
    OptCount (inherited): class attribute, counts all optics created. [integer]
    Thick: thickness of the mirror. [float]
    Dia: diameter of the mirror. [float]
    HRCenter: center of the 'chord' of the HR surface. [3D vector]
    HRNorm: unitary normal to the 'chord' of the HR (always pointing towards the
        outside of the component). [3D vector]
    HRK: curvature of the HR surface. [float]
    ARK: idem.
    Wedge: wedge angle (see doc). [float]
    Alpha: rotation angle during construction (see doc). [float]
    RotMatrix: rotation matrix to take [1,0,0] to HRNorm and [-cosW,0,sinW]
        to ARNorm during construction (see doc). [3D np.array matrix]
    HRr, HRt, ARr, ARt: power reflectance and transmission coefficients of
        the HR and AR surfaces.
    N: refraction index of the material. [float]
    Name (inherited): name of mirror. [string]
    Ref (inherited): reference of mirror. [string]
    KeepI: whether of not to keep data of rays for interference calculations
        on the HR. [boolean]

    **Note**: the curvature of ant surfac is positive for a concave surface
    (HR inside the sphere). Thus kurv*HRNorm/|kurv| always points to the center
    of the sphere of the surface, as is the convention for the lineSurfInter of
    geometry module. Same for AR.


    *=== Methods ===*

    '''

    def __init__(self, thickness, diameter, HRCenter =  [0., 0., 0.],
                HRNorm = [1., 0., 0.], HRK = 0., ARK = 0., Wedge = 0.,
                Alpha = 0., HRr = 1., HRt = 0., ARr = 0., ARt = 1., N = 1.4585,
                Name = None, Ref = None, KeepI = True):
        '''Mirror constructor.

        Parameters are the attributes.

        Returns a mirror.

        '''

        super(Mirror, self).__init__(Name, Ref)
        self.Thick = float(thickness)
        self.Dia = float(diameter)
        self.HRCenter = np.array(HRCenter)
        self.HRNorm = np.array(HRNorm)
        self.HRNorm = self.HRNorm/np.linalg.norm(self.HRNorm)
        self.HRK = float(HRK)
        self.ARK = float(ARK)
        self.Wedge = float(Wedge)
        self.Alpha = float(Alpha)
        self.RotMatrix = helpers.rotMatrix(np.array([1., 0., 0.]), HRNorm)
        self.HRr = float(HRr)
        self.HRt = float(HRt)
        self.ARr = float(ARr)
        self.ARt = float(ARt)
        self.N = float(N)
        self.KeepI = KeepI

    def isHit(self, beam):
        '''Determine if a beam hits the mirror.

        This uses the line***Inter functions from the geometry module to find
        characteristics of impact of beams on mirrors.

        beam: incoming beam. [GaussianBeam]

        Returns a dictionnary with keys:
            'isHit': whether the beam hits the mirror. [boolean]
            'intersection point': point in space where it is first hit. [3D vector]
            'face': to indicate which face is first hit, can be 'HR', 'AR' or
                'side'. [string]
            'distance': geometrical distance from beam origin to impact. [float]

        '''

        noInterDict = {'isHit': False,
                        'intersection point': np.array([0., 0., 0.]),
                        'face': None,
                        'distance': 0.}

        # determine ARCenter and ARNorm
        ARCenter = self.HRCenter - self.Thick*self.HRNorm \
                            - self.Dia*np.tan(self.Wedge)*self.HRNorm/2.

        ARNorm = np.matmul(self.RotMatrix,
                        np.array([-np.cos(self.Wedge), 0., np.sin(self.Wedge)]))

        # get impact parameters on HR, AR and side:
        if np.abs(self.HRK) > 0.:
            HRDict = geo.lineSurfInter(beam.Pos,
                                        beam.Dir, self.HRCenter,
                                        self.HRK*self.HRNorm/np.abs(self.HRK),
                                        np.abs(self.HRK),
                                        self.Dia)
        else:
            HRDict = geo.linePlaneInter(beam.Pos, beam.Dir, self.HRCenter,
                                        self.HRNorm, self.Dia)

        if np.abs(self.ARK) > 0.:
            ARDict = geo.lineSurfInter(beam.Pos,
                                        beam.Dir, ARCenter,
                                        self.ARK*ARNorm/np.abs(self.ARK),
                                        np.abs(self.ARK),
                                        self.Dia/np.sin(self.Wedge))
        else:
            ARDict = geo.linePlaneInter(beam.Pos, beam.Dir, ARCenter,
                                        ARNorm, self.Dia)

        SideDict = geo.lineCylInter(beam.Pos, beam.Dir,
                                    self.HRCenter, self.HRNorm,
                                    self.Thick, self.Dia)

        # face tags
        HRDict['face'] = 'HR'
        ARDict['face'] = 'AR'
        SideDict['face'] = 'Side'


        # determine first hit
        hitFaces = filter(helpers.hitTrue, [HRDict, ARDict, SideDict])

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

    def hit(self, beam, order = None, threshold = None):
        '''Compute the refracted and reflected beams after interaction.

        beam: incident beam. [GaussianBeam]
        order: maximum strayness of daughter beams, whixh are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionnary of beams with keys:
            'refr': refracted beam. [GaussianBeam]
            'refl': reflected beam. [GaussianBeam]

        '''
        # get impact parameters
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

        Returns a dictionnary of beams with keys:
            'refr': refracted beam. [GaussianBeam]
            'refl': reflected beam. [GaussianBeam]

        '''

        ans = {}
        d = np.linalg.norm(point - beam.Pos)

        # Calculate the local normal in opposite direction
        if self.HRK == 0.:
            localNor = self.HRNorm
        else:
            # normal pointing to center of the sphere
            nor = self.HRK * self.NRNorm/np.abs(self.HRK)

            # center of sphere:
            theta = np.arcsin(self.Dia * self.HRK/2.)   #undertending angle
            sphereC = self.HRCenter + np.cos(theta)*nor/self.HRK
            localNor = sphereC - point
            localNor = localNor/np.linalg.norm(localNor)

        if np.dot(beamDir, localNorm) > 0.:
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
        dir2 = geo.newDir(beam.Dir, localNorm, n1, n2)

        # if there is no refracted
        if beam.P * self.HRt < threshold or beam.StrayOrder + 1 > order \
                                        or dir2['refr'] is None:
            ans['refr'] = None

        # if there is no reflected
        if beam.P * self.HRr < threshold:
            ans['refl'] = None

        # we're done if there are two Nones
        if len(ans) == 2:
            return ans

        # Calculate new basis
        if not 'refl' in ans:   # for reflected
            Uxr, Uyr = helpers.basis(dir2['refl'])
            Uzr = dir2['refl']

        if not 'refr' in ans:   # for refracted
            Uxt, Uyt = helpers.basis(dir2['refr'])
            Uzt = dir2['refr']

        Lx, Ly = helpers.basis(localNorm)

        # Calculate daughter curv tensors
        C = np.array([self.HRK, 0.], [0, self.HRK])
        Ki = np.array([np.dot(beam.U[0], Lx), np.dot(beam.U[0], Ly)],
                        [np.dot(beam.U[1], Lx), np.dot(beam.U[1], Ly)])
        Qi = beam.Q(d)
        Kit = np.transpose(Ki)
        Xi = np.matmul(np.matmul(Kit, Qi), Ki)

        if not 'refr' in ans:
            Kt = np.array([np.dot(Uxt, Lx), np.dot(Uxt, Ly)],
                            [np.dot(Uyt, Lx), np.dot(Uyt, Ly)])
            Ktt = np.transpose(Kt)
            Ktinv = np.linalg.inv(Kt)
            Kttinv = np.linalg.inv(Ktt)
            Xt = (np.dot(localNorm, beam.Dir) -n2*np.dot(localNorm, Uzt)/n1) * C
            Qt = n1*np.matmul(np.matmul(Kttinv, Xi - Xt), Ktinv)/n2

        if not 'refl' in ans:
            Kr = np.array([np.dot(Uxr, Lx), np.dot(Uxr, Ly)],
                            [np.dot(Uyr, Lx), np.dot(Uyr, Ly)])
            Krt = np.transpose(Kr)
            Krinv = np.linalg.inv(Kr)
            Krtinv = np.linalg.inv(Krt)
            Xr = (np.dot(localNorm, beam.Dir) - np.dot(localNorm, Uzr)) * C
            Qr = np.matmul(np.matmul(Krtinv, Xi - Xr), Krinv)

        # Create new beams
        if not 'refl' in ans:
            ans['refl'] = gbeam.GaussianBeam(ortho = False, Q = Qr,
                    Pos = point, Dir = Uzr, Ux = Uxr, Uy = Uyr,
                    N = n1, Wl = beam.Wl, P = beam.P * self.HRr,
                    StrayOrder = beam.StrayOrder)

        if not 'refr' in ans:
            ans['refr'] = gbeam.GaussianBeam(ortho = False, Q = Qt, Pos = point,
                Dir = Uzt, Ux = Uxt, Uy = Uyt, N = n2, Wl = beam.Wl,
                P = beam.P * self.HRt, StrayOrder = beam.StrayOrder + 1)

        return ans

    def hitAR(self, beam, point, order, threshold):
        '''Compute the daughter beams after interaction on AR at point.

        beam: incident beam. [GaussianBeam]
        point: point in space of interaction. [3D vector]
        order: maximum strayness of daughter beams, which are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionnary of beams with keys:
            'refr': refracted beam. [GaussianBeam]
            'refl': reflected beam. [GaussianBeam]

        '''

        ans = {}
        d = np.linalg.norm(point - beam.Pos)

        # determine ARCenter and ARNorm
        ARCenter = self.HRCenter - self.Thick*self.HRNorm \
                            - self.Dia*np.tan(self.Wedge)*self.HRNorm/2.

        ARNorm = np.matmul(self.RotMatrix,
                        np.array([-np.cos(self.Wedge), 0., np.sin(self.Wedge)]))

        # Calculate the local normal
        if self.ARK == 0.:
            localNorm = ARNorm
        else:
            # normal pointing to center of the sphere
            nor = self.ARK * ARNorm/np.abs(self.ARK)

            # center of sphere:
            theta = np.arcsin(self.Dia * self.ARK/2.)   #undertending angle
            sphereC = ARCenter + np.cos(theta)*nor/self.ARK
            localNorm = sphereC - point
            localNorm = localNorm/np.linalg.norm(localNorm)

        if np.dot(beam.Dir, localNorm) > 0.:
            localNorm = - localNorm

        # determine whether we're entering or exiting the substrate
        if np.dot(beam.Dir, ARNorm) < 0.:
            #entering
            n1 = beam.N
            n2 = self.N
        else:
            #exiting
            n1 = self.N
            n2 = 1.

        # daughter directions
        dir2 = geo.newDir(beam.Dir, localNorm, n1, n2)

        # if there is no refracted
        if beam.P * self.ARt < threshold or dir2['refr'] is None:
            ans['refr'] = None

        # if there is no reflected
        if beam.P * self.ARr < threshold or beam.StrayOrder + 1 > order:
            ans['refl'] = None

        # we're done if there are two Nones
        if len(ans) == 2:
            return ans

        # Calculate new basis
        if not 'refl' in ans:   # for reflected
            Uxr, Uyr = helpers.basis(dir2['refl'])
            Uzr = dir2['refl']

        if not 'refr' in ans:   # for refracted
            Uxt, Uyt = helpers.basis(dir2['refr'])
            Uzt = dir2['refr']

        Lx, Ly = helpers.basis(localNorm)

        # Calculate daughter curv tensors
        C = np.array([[self.ARK, 0.], [0, self.ARK]])
        Ki = np.array([[np.dot(beam.U[0], Lx), np.dot(beam.U[0], Ly)],
                        [np.dot(beam.U[1], Lx), np.dot(beam.U[1], Ly)]])
        Qi = beam.Q(d)
        Kit = np.transpose(Ki)
        Xi = np.matmul(np.matmul(Kit, Qi), Ki)

        if not 'refr' in ans:
            Kt = np.array([[np.dot(Uxt, Lx), np.dot(Uxt, Ly)],
                            [np.dot(Uyt, Lx), np.dot(Uyt, Ly)]])
            Ktt = np.transpose(Kt)
            Ktinv = np.linalg.inv(Kt)
            Kttinv = np.linalg.inv(Ktt)
            Xt = (np.dot(localNorm, beam.Dir) -n2*np.dot(localNorm, Uzt)/n1) * C
            Qt = n1*np.matmul(np.matmul(Kttinv, Xi - Xt), Ktinv)/n2

        if not 'refl' in ans:
            Kr = np.array([[np.dot(Uxr, Lx), np.dot(Uxr, Ly)],
                            [np.dot(Uyr, Lx), np.dot(Uyr, Ly)]])
            Krt = np.transpose(Kr)
            Krinv = np.linalg.inv(Kr)
            Krtinv = np.linalg.inv(Krt)
            Xr = (np.dot(localNorm, beam.Dir) - np.dot(localNorm, Uzr)) * C
            Qr = np.matmul(np.matmul(Krtinv, Xi - Xr), Krinv)

        # Create new beams
        if not 'refl' in ans:
            ans['refl'] = gbeam.GaussianBeam(ortho = False, Q = Qr,
                    Pos = point, Dir = Uzr, Ux = Uxr, Uy = Uyr,
                    N = n1, Wl = beam.Wl, P = beam.P * self.ARr,
                    StrayOrder = beam.StrayOrder + 1)

        if not 'refr' in ans:
            ans['refr'] = gbeam.GaussianBeam(ortho = False, Q = Qt, Pos = point,
                Dir = Uzt, Ux = Uxt, Uy = Uyt, N = n2, Wl = beam.Wl,
                P = beam.P * self.ARt, StrayOrder = beam.StrayOrder)


        return ans

    def hitSide(self, beam):
        '''Compute the daughter beams after interaction on Side at point.

        beam: incident beam. [GaussianBeam]

        Returns {'refr': None, 'refl': None}

        '''
        return {'refr': None, 'refl': None}
