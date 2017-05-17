'''Defines the BeamDump class for theia.'''

# Provides:
#   class BeamDump
#       __init__
#       lineList
#       isHit
#       hit

import numpy as np
from helpers import settings
from helpers import geometry as geo
from helpers.tools import formatter, hitTrue
from component import SetupComponent

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

    def __init__(self, Center = None, Norm = None,
                Name = None, Ref = None, Thickness = None, Diameter = None):
        '''BeamDump constructor.

        Parameters are the attributes.

        Returns a BeamDump.

        '''
        if Name is None:
            Name = "BeamDump"
        # initialize from base constructor
        super(BeamDump, self).__init__(Name = Name, Ref = Ref,
                HRCenter = Center, HRNorm = Norm, Thickness = Thickness)



    def lineList(self):
        '''Return the list of lines needed to print the object.
        '''
        ans = []
        ans.append("BeamDump: " + self.Name + " (" + self.Ref + ") {")
        ans.append("Thick: " + str(self.Thick) + "m")
        ans.append("Diameter: " + str(self.Dia) + "m")
        ans.append("Center: " + str(self.HRCenter))
        ans.append("Norm: " + str(self.HRNorm))
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
        HRDict = geo.linePlaneInter(beam.Pos, beam.Dir, self.HRCenter,
                                    self.HRNorm, self.Dia)

        SideDict = geo.lineCylInter(beam.Pos, beam.Dir,
                                    self.HRCenter, self.HRNorm,
                                    self.Thick, self.Dia)

        ARCenter = self.HRCenter - self.Thick*self.HRNorm

        ARDict = geo.linePlaneInter(beam.Pos, beam.Dir, ARCenter,
                                    - self.HRNorm, self.Dia)

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
            print "theia: Info: reached end node of tree by interaction on "\
            + self.Name + " (" + self.Ref + ") of beam "\
            + beam.Name + "."

        return {'r': None, 't': None}
