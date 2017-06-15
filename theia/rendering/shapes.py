'''Shapes module for theia, provides shape-calculating for 3D rendering.'''

# Provides:
#   mirrorShape
#   lensShape
#   beamDumpShape
#   ghostShape
#   beamShape

import Part

def mirrorShape(mirror):
    return Part.makeBox(1,1,1)

def lensShape(lens):
    return Part.makeBox(1,1,1)

def beamDumpShape(beamDump):
    return Part.makeBox(1,1,1)

def ghostShape(ghost):
    return Part.makeBox(1,1,1)

def beamShape(beam):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object

    '''
    start = beam.Pos
    if beam.Length > 0.:
        end = start + beam.Length * beam.Dir
    else:
        end = start + 1.e7 * beam.Dir

    return Part.makeLine(tuple(start), tuple(end))
