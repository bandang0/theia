'''Defines the BeamDump class for theia.'''

# Provides:
#   class BeamDump
#       __init__
#       lines
#       isHit
#       hit

import numpy as np
from ..helpers import settings
from ..helpers.geometry import rectToSph, linePlaneInter, lineCylInter
from ..helpers.units import deg, pi
from ..helpers.tools import shortRef
from .component import SetupComponent

class BeamDump(SetupComponent):
    '''

    BeamDump class.

    This class represents components on which rays stop. They have cylindrical
    symmetry and stop beams on all their faces. They can represent baffles
    for example.

    *=== Attributes ===*
    SetupCount (inherited): class attribute, counts all setup components.
        [integer]
    Name: class attribute. [string]
    HRCenter (inherited): center of the principal face of the BeamDump in space.
        [3D vector]
    HRnorm (inherited): normal unitary vector the this principal face,
        supposed to point outside the media. [3D vector]
    Thick (inherited): thickness of the dump, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
    Ref (inherited): reference string (for keeping track with the lab). [string]

    '''
    Name = "BeamDump"
    def __init__(self, X = 0., Y = 0., Z = 0., Theta = pi/2., Phi = 0.,
                Ref = None,
                Thickness = 2.e-2, Diameter = 5.e-2):
        '''BeamDump initializer.

        Parameters are the attributes.

        Returns a BeamDump.

        '''
        #Check input
        Thickness = float(Thickness)
        Diameter = float(Diameter)

        # prepare for mother initializer
        Norm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        HRCenter = np.array([X, Y, Z], dtype = np.float64)
        ARCenter = HRCenter - Thickness * Norm

        # initialize from base initializer
        super(BeamDump, self).__init__(Ref = Ref,
                Diameter = Diameter, HRCenter = HRCenter, HRNorm = Norm,
                Thickness = Thickness, ARCenter = ARCenter)

    def lines(self):
        '''Return the list of lines needed to print the object.
        '''
        ans = []
        ans.append("BeamDump: %s {" %self.Ref)
        ans.append("Thick: %sm" %str(self.Thick))
        ans.append("Diameter: %sm" %str(self.Dia))
        ans.append("Center: %s" %str(self.HRCenter))
        sph = rectToSph(self.HRNorm)
        ans.append("Norm: (%s, %s)deg" %(str(sph[0]/deg), str(sph[1]/deg)))
        ans.append("}")

        return ans

    def isHit(self, beam):
        '''Determine if a beam hits the BeamDump.

        This uses the line***Inter functions from the geometry module to find
        characteristics of impact of beams on beamdumps.

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

        SideDict =lineCylInter(beam.Pos, beam.Dir,
                                    self.HRCenter, self.HRNorm,
                                    self.Thick, self.Dia)

        ARCenter = self.HRCenter - self.Thick*self.HRNorm

        ARDict = linePlaneInter(beam.Pos, beam.Dir, ARCenter,
                                    - self.HRNorm, self.Dia)

        # face tags
        HRDict['face'] = 'HR'
        ARDict['face'] = 'AR'
        SideDict['face'] = 'Side'

        # determine first hit
        hitFaces = filter(lambda dic: dic['isHit'], [HRDict, ARDict, SideDict])

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

        BeamDumps always stop beams.

        beam: incident beam. [GaussianBeam]
        order: maximum strayness of daughter beams, which are not returned if
            their strayness is over this order. [integer]
        threshold: idem for the power of the daughter beams. [float]

        Returns a dictionary of beams with keys:
            't': None
            'r': None

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

        if settings.info and (beam.N == 1. or not settings.short):
            print "theia: Info: Reached beam stop (%s on %s)." \
                    %(beam.Ref if not settings.short else shortRef(beam.Ref),
                        self.Ref)

        return {'r': None, 't': None}
