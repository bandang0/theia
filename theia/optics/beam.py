'''Defines the GaussianBeam class for theia.'''

# Provides:
#   class GaussianBeam
#       __init__
#       __str__
#       lines
#       Q
#       QParam
#       ROC
#       waistPos
#       rayleigh
#       width
#       waistSize
#       gouy
#       initGaussianData
#       translate
#   userGaussianBeam

import numpy as np
from ..helpers import geometry
from ..helpers.tools import formatter
from ..helpers.units import pi, nm, deg, mm

class GaussianBeam(object):
    '''

    GaussianBeam class.

    This class represents general astigmatic Gaussian beams in 3D space.
    These are the objects that are intended to interact with the optical
    components during the ray tracing and that are rendered in 3D thanks to
    FreeCAD.

    *=== Attributes ===*
    BeamCount: class attribute, counts beams. [integer]
    Name: class attribute. [string]
    QTens: general astigmatic complex curvature tensor at the origin.
        [np. array of complex]
    N: Refraction index of the medium in which the beam is placed. [float]
    Wl: Wave-length in vacuum of the beam (frequency never changes). [float]
    P: Power of the beam. [float]
    Pos: Position in 3D space of the origin of the beam. [3D vector]
    Dir: Normalized direction in 3D space of the beam axis. [3D vector]
    U: A tuple of unitary vectors which along with Dir form a direct orthonormal
        basis in which the Q tensor is expressed. [tuple of 3D vectors]
    Ref: Reference to the beam. [string]
    OptDist: Optical length. [float]
    Length: Geometrical length of the beam. [float]
    StrayOrder: Number representing the *strayness* of the beam. If the beams
        results from a transmission on a HR surface or a reflection on a AR
        surface, then its StrayOrder is the StrayOrder of the parent beam + 1.
        [integer]
    Optic: Ref of optic where the beam departs from ('Laser' if laser). [string]
    Face: Face of the optic where the beam departs from. [string]
    TargetOptic: Ref of the optic where the beam terminates (None if open
        beam). [string]
    TargetFace: Face of the target optic where the beam terminates. [string]
    DWx: Distance of waist on X. [float]
    DWy: Distance of waist on Y. [float]
    Wx: Waist on X. [float]
    Wy: Waist on Y. [float]
    IWx: Width of beam on X at origin. [float]
    IWy: Width of beam on Y at origin. [float]
    TWx: Width of beam on X at target surface (None if open beam). [float]
    TWy: Width of beam on Y at target surface (None if open beam).

    '''
    BeamCount = 0   # counts beams
    Name = "Beam"

    def __init__(self, Q, N, Wl, P, Pos, Dir, Ux, Uy, Ref, OptDist,
        Length, StrayOrder, Optic, Face):
        '''Beam initializer.

        This is the initializer used internally for beam creation, for user
        inputed beams, see function userGaussianBeam.

        Returns a Gaussian beam with attributes as the parameters.

        '''

        # external params
        self.N = N
        self.Wl = Wl
        self.P = P
        self.OptDist = OptDist
        self.Length = Length
        self.StrayOrder = StrayOrder

        self.Ref = Ref

        self.Pos = Pos
        self.Dir = Dir

        # orthonormal basis in which Q is expressed
        self.U = (Ux, Uy)

        # Curvature tensor
        self.QTens = np.array(Q, dtype = np.complex64)

        #origin optics
        self.Optic = Optic
        self.Face = Face

        # target optics
        self.TargetOptic = None
        self.TargetFace = None

        # initialize gaussian data
        self.initGaussianData()
        self.TWx = None
        self.TWy = None

        self.__class__.BeamCount = self.__class__.BeamCount + 1

    def __str__(self):
        '''String representation of the beam, when calling print(beam).

        '''
        return formatter(self.lines())

    def lines(self):
        '''Returns the list of lines necessary to print the object.

        '''
        sph = geometry.rectToSph(self.Dir)
        sphx = geometry.rectToSph(self.U[0])
        sphy = geometry.rectToSph(self.U[1])

        return ["Beam: %s {" %self.Ref,
        "Power: %sW/Index: %s/Wavelength: %snm/Length: %sm" \
                % (str(self.P), str(self.N), str(self.Wl/nm), str(self.Length)),
        "Order: %s" %str(self.StrayOrder),
        "Origin: %s" %str(self.Pos),
        "Direction: (%s, %s)deg" % (str(sph[0]/deg), str(sph[1]/deg)),
        "Ux: (%s, %s)deg" % (str(sphx[0]/deg), str(sphx[1]/deg) ),
        "Uy: (%s, %s)deg" % (str(sphy[0]/deg), str(sphy[1]/deg)),
        "Waist Pos: (%s, %s)m" % ( str(self.DWx), str(self.DWy) ),
        "Waist Size: (%s, %s)mm" % (str(self.Wx/mm), str(self.Wy/mm)),
        "Rayleigh: %sm" % str(self.rayleigh()),
        "ROC: " + str(self.ROC()),
        "}"]

    def Q(self, d = 0.):
        '''Return the Q tensor at a distance d of origin.

        '''
        d = float(d)
        I = np.array([[1., 0.], [0., 1.]], dtype=np.float64)
        return np.dot(np.linalg.inv(I + d * self.QTens), self.QTens)

    def QParam(self, d = 0.):
        '''Compute the complex parameters q1 and q2 and theta of beam.

        What is implemented here is a straightforward calculation to extract
        the q1, q2, and theta of the normal form of Q.

            Returns a tuple q1, q2, theta
        '''
        Q = self.Q(float(d))

        a = Q[0][0]
        b = Q[0][1]
        c = Q[1][1]

        if a == c:
            theta = pi/4.
            qxinv = (a + b)
            qyinv = (a - b)

        else:
            theta = .5*np.arctan(2*b/(a-c))
            qxinv = 0.5*(a + c + (a - c)/np.cos(2 *theta))
            qyinv = 0.5*(a + c - (a - c)/np.cos(2 *theta))

        q1 = np.inf if qxinv == 0. else 1./qxinv
        q2 = np.inf if qyinv == 0. else 1./qyinv

        return  q1, q2, theta

    def ROC(self, dist = 0.):
        '''Return the tuple of ROC of the beam.

        '''
        dist = float(dist)
        q1, q2, _ = self.QParam(dist)
        try:
            a = 1./np.real(1./q1)
        except FloatingPointError:
            a = np.inf
        try:
            b = 1./np.real(1./q2)
        except FloatingPointError:
            b = np.inf

        return (a, b)

    def waistPos(self):
        '''Return the tuple of positions of the waists of the beam along Dir.

        '''
        q1, q2, q3 = self.QParam(0.)
        return (-np.real(q1), -np.real(q2))

    def rayleigh(self):
        '''Return the tuple of Rayleigh ranges of the beam.

        '''
        q1, q2, _ = self.QParam(0.)
        return (np.abs(np.imag(q1)), np.abs(np.imag(q2)))

    def width(self, d = 0.):
        '''Return the tuple of beam widths at distance d.

        '''
        lam = self.Wl/self.N
        q1, q2, _ = self.QParam(float(d))

        return (np.sqrt((lam/pi)*((d - np.real(q1))**2.\
                    + np.imag(q1)**2.)/np.imag(q1)),
                np.sqrt((lam/pi)*((d - np.real(q2))**2.\
                    + np.imag(q2)**2.)/np.imag(q2)))

    def waistSize(self):
        '''Return a tuple with the waist sizes in x and y.

        '''
        q1, q2, _ = self.QParam()
        lam = self.Wl/self.N

        return (np.sqrt(lam/pi)*np.abs(q1)/np.sqrt(np.imag(q1)) ,
                np.sqrt(lam/pi)*np.abs(q2)/np.sqrt(np.imag(q2)))

    def gouy(self, d = 0.):
        '''Return the tuple of Gouy phases.

        '''
        q1, q2, _ = self.QParam(float(d))

        return (np.arctan(np.real(q1)/np.imag(q1)),
                np.arctan(np.real(q2)/np.imag(q2)))

    def initGaussianData(self):
        '''Writes the relevant DW, W, IW data with Q.

        Is called upon construction to write the data of waist position and
        size, initial widths once and for all.

        '''
        dist = self.waistPos()
        size = self.waistSize()
        initWidth = self.width(0.)
        self.DWx = dist[0]
        self.DWy = dist[1]
        self.Wx = size[0]
        self.Wy = size[1]
        self.IWx = initWidth[0]
        self.IWy = initWidth[1]

    def translate(self, X = 0., Y = 0., Z = 0.):
        '''Move the beam to (current position + (X, Y, Z)).

        X, Y, Z: components of the translation vector.

        No return value.
        '''
        self.Pos = self.Pos + np.array([X, Y, Z], dtype = np.float64)

def userGaussianBeam(Wx = 1.e-3, Wy = 1.e-3, WDistx = 0., WDisty = 0.,
                    Wl = 1064.e-9, P = 1., X = 0., Y = 0., Z = 0.,
                    Theta = pi/2., Phi = 0., Alpha = 0.,
                    Ref = None):
    '''Constructor used for user inputed beams, separated from the class
    initializer because the internal state of a beam is very different from
    the input of this user-defined beam.

    Input parameters are processed to make arguments for the class
    contructor and then the corresponding beam is returned.
    '''

    #externs
    P = float(P)
    Pos = np.array([X, Y, Z], dtype = np.float64)
    Dir = np.array([np.sin(Theta) * np.cos(Phi),
            np.sin(Theta) * np.sin(Phi),
            np.cos(Theta)], dtype = np.float64)

    # basis for Q tensor
    Alpha = float(Alpha)
    (u1,v1) = geometry.basis(Dir)
    v = np.cos(Alpha)*v1 - np.sin(Alpha)*u1
    u = np.cos(Alpha)*u1 + np.sin(Alpha)*v1

    # Q tensor for orthogonal beam
    Wl = np.abs(float(Wl))
    Wx = float(Wx)
    Wy = float(Wy)
    qx = complex(- float(WDistx)  + 1.j * pi*Wx**2./Wl )
    qy = complex(- float(WDisty)  + 1.j * pi*Wy**2./Wl )
    QTens = np.array([[1./qx, 0.],[0., 1./qy]],
                        dtype = np.complex64)

    Ref = "Beam%s-" %str(GaussianBeam.BeamCount) if Ref is None else Ref + '-'

    return GaussianBeam(Q = QTens, N = 1., Wl = Wl, P = P,
        Pos = Pos, Dir = Dir,
        Ux = u, Uy = v, Ref = Ref, OptDist = 0.,
        Length = 0., StrayOrder = 0, Optic = 'Laser', Face = 'Out')
