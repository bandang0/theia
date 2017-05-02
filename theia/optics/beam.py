'''Defines the GaussianBeam class for theia.'''

# Provides:
#   class GaussianBeam
#       __init__(self, Qx, Qy, Pos = np.array([0., 0., 0.]),
#           Dir = np.array([1., 0., 0.]), Alpha = 0.,
#           Name = 'Beam', N = 1., Wl = 1064.*nm, P = 1*W,
#           OptDist = 0.*m, Length = 0.*m,
#           Gouyx = 0., Gouyy = 0., StrayOrder = 0):
#       propDeltas(self,d)
#       width(self, dist = 0.)
#       waistPos(self)
#       waistSize(self)
#       Rayleigh(self)
#       ROC(self, dist = 0.)


import numpy as np
from units import *
import tools

class GaussianBeam(object):
    '''

    GaussianBeam class.

    This class represents general astigmatic Gaussian beams in 3D space.
    These are the objects that are intended to interact with the optical
    components during the ray tracing and that are rendered in 3D thanks to
    FreeCAD.

    *=== Attributes ===*
    BeamCount: class attribute, counts beams. [integer]
    QTens: gerenal strigmatic complex curvature tensor at the origin.
        [np. array of complex]
    #Wx: Beam width in the x direction at waist. [float]
    #Wy: Beam width in the y direction at waist. [float]
    #WDistx: Geometrical position of the waist in the x direction counted from
        the origin of the beam and along Dir. [float]
    #WDisty: Geometrical position of the waist in the y direction counted from
        the origin of the beam and along Dir. [float]
    N: Refraction index of the medium in which the beam is placed. [float]
    Wl: Wave-length in vacuum of the beam (frequency never changes). [float]
    P: Power of the beam. [float]
    Pos: Position in 3D space of the origin of the beam. [3D vector]
    Dir: Normalized direction in 3D space of the beam axis. [3D vector]
    U: A tuple of unitary vectors which along with Dir form a direct orthonormal
        basis in which the Q tensor is expressed. [tuple of 3D vectors]
    Name: Name of the beam if any. [string]
    OptDist: Optical length. [float]
    Length: Geometrical length of the beam. [float]
    StrayOrder: Number representing the *strayness* of the beam. If the beams
        results from a transmission on a HR surface or a reflection on a AR
        surface, then its StrayOrder is the StrayOrder of the parent beam + 1.
        [integer]

    *=== Methods ===*


    '''
    BeamCount = 0   # counts beams

    def __init__(self, Wx = None, Wy = None, WDistx = None, WDisty = None,
        Q = None, ortho = True, N = 1.,
        Wl = 1064.*nm, P = 1*W, Pos = [0., 0., 0.], Dir = [1., 0., 0.],
        Ux = [0., -1., 0.], Uy = None, Name = None, OptDist = 0.*m,
        Length = 0.*m, StrayOrder = 0):
        '''Beam constructor.

        This constructor allows to construct *orthogonal* Gaussian beams if the
        ortho parameter is True, or a general astigmatic beam if it is False.
        If ortho is True, a pair of waists and waist distances has to be given
        and the corresponding orthogonal beam is returned
        if it is False a general tensor attribute can directly be given.

        The Ux vector which is input is the second of the orthonormal basis.

        Returns a Gaussian beam with attributes as the parameters.

        '''

        # external params
        self.N = float(N)
        self.Wl = float(Wl)
        self.P = float(P)
        self.OptDist = float(OptDist)
        self.Length = float(Length)
        self.StrayOrder = StrayOrder

        # name
        if Name is not None:
            self.Name = Name
        else:
            self.Name = 'Beam' + str(self.__class__.BeamCount)

        # orthonormal basis in which Q is expressed
        self.Pos = np.array(Pos)
        self.Dir = np.array(Dir)
        self.Dir = self.Dir/np.linalg.norm(Dir)
        u = np.array(Ux)
        u = u/np.linalg.norm(u)

        if Uy is not None:
            v = np.array(Uy)
        else:
            v = np.cross(self.Dir, u)
            v = v/np.linalg.norm(v)

        self.U = (u, v)


        # curvature tensor
        if ortho:
            lam = self.Wl/N
            Wx = float(Wx)
            qx = complex(- float(WDistx)  + 1.j * np.pi*Wx**2./lam )
            qy = complex(- float(WDisty)  + 1.j * np.pi*Wy**2./lam )
            # Q tensor for orthogonal beam
            self.QTens = np.array([[1./qx, 0.],[0., 1./qy]], dtype = np.complex64)

        elif not ortho:
            self.QTens = Q

        self.__class__.BeamCount = self.__class__.BeamCount + 1

    

    def Q(self, d = 0.):
        '''Return the Q tensor at a distance d of origin.

        '''
        d = float(d)
        I = np.array([[1., 0.], [0., 1.]])
        return np.matmul(np.linalg.inv(I + d * self.QTens),self.QTens)
