'''Defines the Ghost class for theia.'''

# Provides:
#   class Ghost
#       __init__
#       lines
#       isHit
#       hit

import numpy as np
from ..helpers.geometry import rectToSph, linePlaneInter
from ..helpers.units import deg, pi
from .component import SetupComponent
from .beam import GaussianBeam

class Ghost(SetupComponent):
    '''

    Ghost class.

    This class represents surfaces which don't interact with the beams. They
    just transmit the same beam, and may be useful to monitor the beams on their
    way, without having to calculate the Q yourself if you're looking for the
    Q at another place than the origin of the beam.

    Ghost surfaces basically have a null thickness and transmit the beams.

    *=== Attributes ===*
    SetupCount (inherited): class attribute, counts all setup components.
        [integer]
    Name: class attribute. [string]
    HRCenter (inherited): center of the principal face of the Ghost in space.
        [3D vector]
    HRnorm (inherited): normal unitary vector the this principal face,
        supposed to point outside the media. [3D vector]
    Thick (inherited): thickness of the dump, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
    Ref (inherited): reference string (for keeping track with the lab). [string]

    '''
    Name = "Ghost"
    def __init__(self, X = 0., Y = 0., Z = 0., Theta = pi/2., Phi = 0.,
                Ref = None, Diameter = 5.e-2):
        '''Ghost initializer.

        Parameters are the attributes.

        Returns a Ghost.

        '''
        #Check input
        Diameter = float(Diameter)

        # prepare for mother initializer
        Norm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        HRCenter = np.array([X, Y, Z], dtype = np.float64)

        # initialize from base initializer
        super(Ghost, self).__init__(Ref = Ref,
                Diameter = Diameter, HRCenter = HRCenter, HRNorm = Norm,
                Thickness = 0.)

    def lines(self):
        '''Return the list of lines needed to print the object.
        '''
        ans = []
        ans.append("Ghost: {" %self.Ref)
        ans.append("Diameter: %sm" %str(self.Dia))
        ans.append("Center: %s" %str(self.HRCenter))
        sph = rectToSph(self.HRNorm)
        ans.append("Norm: (%s, %s)deg" %(str(sph[0]/deg), str(sph[1]/deg)))
        ans.append("}")

        return ans

    def isHit(self, beam):
        '''Determine if a beam hits the Ghost surface.

        This uses the linePlaneInter function from the geometry module to find
        characteristics of impact of beams on ghost surfaces.

        beam: incoming beam. [GaussianBeam]

        Returns a dictionary with keys:
            'isHit': whether the beam hits the dump. [boolean]
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

        # Get impact parameters
        HRDict = linePlaneInter(beam.Pos, beam.Dir, self.HRCenter,
                                    self.HRNorm, self.Dia)

        if HRDict['isHit']:
            return {'isHit': True,
                    'intersection point': HRDict['intersection point'],
                    'face': 'HR',
                    'distance': HRDict['distance']
                    }
        else:
            return noInterDict

    def hit(self, beam, order, threshold):
        '''Return the beam simply transmitted by the ghost surface.

        beam: incident beam. [GaussianBeam]
        order: maximum strayness of daughter beams, which are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionary of beams with keys:
            't': Gaussian beam which is the continuity of the incident beam.

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

        # get interaction point as origin of new beam
        interactionPoint = dic['intersection point']

        # and Q tensor at interaction as new Q
        newQ = beam.Q(beam.Length)

        return {'t': GaussianBeam(Q = newQ, N = beam.N, Wl = beam.Wl,
                        P = beam.P, Pos = interactionPoint, Dir = beam.Dir,
                        Ux = beam.U[0], Uy = beam.U[1], Ref = beam.Ref,
                        OptDist = 0., Length = 0., StrayOrder = beam.StrayOrder,
                        Optic = self.Ref, Face = ''),
                'r': None}
