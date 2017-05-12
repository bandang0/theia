'''Defines the Lens class for theia.'''

# Provides:
#   class Lens
#       hit
#       hitActive

import numpy as np
from optics.optic import Optic
from optics import geometry as geo
from optics.beam import GaussianBeam as gbeam
import helpers

class Lens(Optic):
    '''

    Lens class.

    This class is a base class for lenses. It implements the hit and hitActive
    methods for all lenses.

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

    '''

    def hit(self, beam, order, threshold):
        '''Compute the refracted and reflected beams after interaction.

        This function is valid for all types of lenses.
        The beams returned are those selected after the order and threshold
        criterion.

        beam: incident beam. [GaussianBeam]
        order: maximum strayness of daughter beams, whixh are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionnary of beams with keys:
            't': refracted beam. [GaussianBeam]
            'r': reflected beam. [GaussianBeam]

        '''
        # get impact parameters and update beam
        dic = self.isHit(beam)
        beam.Length = dic['distance']
        beam.OptDist = beam.N * beam.Length

        if dic['face'] == 'HR' or dic['face'] == 'AR':
            return self.hitActive(beam, dic['intersection point'], dic['face'],
                                order, threshold)
        else:
            return self.hitSide(beam)


    def hitActive(self, beam, point, faceTag, order, threshold):
        '''Compute the daughter beams after interaction on HR or AR at point.

        AR andHr are the 'active' surfaces of the lens.
        This function is valid for all types of lenses.

        beam: incident beam. [GaussianBeam]
        point: point in space of interaction. [3D vector]
        faceTag: either 'AR' or 'HR' depending on the face. [string]
        order: maximum strayness of daughter beams, whixh are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionnary of beams with keys:
            't': refracted beam. [GaussianBeam]
            'r': reflected beam. [GaussianBeam]

        '''

        ans = {}
        d = np.linalg.norm(point - beam.Pos)

        # determine global norm and center
        if faceTag == 'AR':
            Norm = self.ARNorm
            Center = self.ARCenter
        else:
            Norm = self.HRNorm
            Center = self.HRCenter

        # Calculate the local normal in opposite direction
        if self.HRK == 0.:
            localNorm = Norm
        else:
            # normal pointing to center of the sphere
            nor = self.HRK * Norm/np.abs(self.HRK)

            # center of sphere:
            theta = np.arcsin(self.Dia * self.HRK/2.)   #undertending angle
            sphereC = Center + np.cos(theta)*nor/self.HRK
            localNorm = sphereC - point
            localNorm = localNorm/np.linalg.norm(localNorm)

        if np.dot(beam.Dir, localNorm) > 0.:
            localNorm = - localNorm

        # determine whether we're entering or exiting the substrate
        if np.dot(beam.Dir, Norm) < 0.:
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
        if beam.P * self.HRt < threshold or dir2['t'] is None:
            ans['t'] = None

        # if there is no reflected
        if beam.P * self.HRr < threshold or beam.StrayOrder + 1 > order :
            ans['r'] = None

        # we're done if there are two Nones
        if len(ans) == 2:
            return ans

        # Calculate new basis
        if not 'r' in ans:   # for reflected
            Uxr, Uyr = helpers.basis(dir2['r'])
            Uzr = dir2['r']

        if not 't' in ans:   # for refracted
            Uxt, Uyt = helpers.basis(dir2['t'])
            Uzt = dir2['t']

        Lx, Ly = helpers.basis(localNorm)

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
                    StrayOrder = beam.StrayOrder + 1, Ref = beam.Ref + 'r')

        if not 't' in ans:
            ans['t'] = gbeam(ortho = False, Q = Qt, Pos = point,
                Dir = Uzt, Ux = Uxt, Uy = Uyt, N = n2, Wl = beam.Wl,
                P = beam.P * self.HRt, StrayOrder = beam.StrayOrder,
                Ref = beam.Ref + 't')

        return ans
