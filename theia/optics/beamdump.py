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
from ..helpers.tools import formatter
from ..helpers.units import *
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
    HRCenter (inherited): center of the principal face of the BeamDump in space.
        [3D vector]
    HRnorm (inherited): normal unitary vector the this principal face,
        supposed to point outside the media. [3D vector]
    Thick (inherited): thickness of the dump, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
    Name (inherited): name of the component. [string]
    Ref (inherited): reference string (for keeping track with the lab). [string]

    '''

    def __init__(self, X = 0., Y = 0., Z = 0., Theta = np.pi/2., Phi = 0.,
                Name = 'BeamDump', Ref = None,
                Thickness = 2.*cm, Diameter = 5.*cm):
        '''BeamDump constructor.

        Parameters are the attributes.

        Returns a BeamDump.

        '''
        # prepare for mother constructor
        Norm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        HRCenter = np.array([X, Y, Z], dtype = np.float64)

        # initialize from base constructor
        super(BeamDump, self).__init__(Name = Name, Ref = Ref,
                HRCenter = HRcenter, HRNorm = Norm, Thickness = Thickness)

    def lines(self):
        '''Return the list of lines needed to print the object.
        '''
        ans = []
        ans.append("BeamDump: " + self.Name + " (" + self.Ref + ") {")
        ans.append("Thick: " + str(self.Thick) + "m")
        ans.append("Diameter: " + str(self.Dia) + "m")
        ans.append("Center: " + str(self.HRCenter))
        sph = rectToSph(self.HRNorm)
        ans.append("Norm: (" + str(sph[0]/deg) + ', ' \
                + str(sph[1]/deg) + ')deg')
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
        if settings.info:
            print "theia: Info: Reached beam stop (" + beam.Ref + ' on '\
            + self.Ref + ').'

        return {'r': None, 't': None}
