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
    Optic: Ref of optic where the beam departs from (None if laser). [string]
    Face: face of the optic where the beam departs from. [string]

    '''
    BeamCount = 0   # counts beams
    Name = "Beam"

    def __init__(self, Q, N, Wl, P, Pos, Dir, Ux, Uy, Ref, OptDist,
        Length, StrayOrder, Optic, Face):
        '''Beam initializer.

        This is the initializer used internally for beam creation, for user
        inputed beams, see class method userGaussianBeam.

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

        self.__class__.BeamCount = self.__class__.BeamCount + 1

    def __str__(self):
        '''String representation of the beam, when calling print(beam).

        '''
        return formatter(self.lines())

    def lines(self):
        '''Returns the list of lines necessary to print the object.

        '''
        ans = []
        ans.append("Beam: %s {" %self.Ref )
        ans.append("Power: %sW/Index: %s/Wavelength: %snm/Length: %sm") \
                %(str(self.P), str(self.N), str(self.Wl/nm), str(self.Length))
        ans.append("Order: %s" %str(self.StrayOrder))
        ans.append("Origin: %s" %str(self.Pos))

        sph = geometry.rectToSph(self.Dir)
        ans.append("Direction: (%s, %s)deg" %(str(sph[0]/deg), str(sph[1]/deg)))

        sphx = geometry.rectToSph(self.U[0])
        ans.append("Ux: (%s, %s)deg" %(str(sphx[0]/deg), str(sphx[1]/deg) ))

        sphy = geometry.rectToSph(self.U[1])
        ans.append("Uy: (%s, %s)deg" %(str(sphy[0]/deg), str(sphy[1]/deg)))
        ans.append("Waist Pos: %sm" % str(self.waistPos()) )
        ans.append("Waist Size: (%s, %s)mm" \
                    %(str(self.waistSize()[0]/mm), str(self.waistSize()[1]/mm)))
        ans.append("Rayleigh: %sm" % str(self.rayleigh()) )
        ans.append("ROC: " + str(self.ROC()))
        ans.append("}")

        return ans

    def Q(self, d = 0.):
        '''Return the Q tensor at a distance d of origin.

        '''
        d = float(d)
        I = np.array([[1., 0.], [0., 1.]], dtype=np.float64)
        return np.matmul(np.linalg.inv(I + d * self.QTens), self.QTens)

    def QParam(self, d = 0.):
        '''Compute the complex parameters q1 and q2 and theta of beam.

            Returns a dictionary with keys:
            '1': q1 [complex]
            '2': q2 [complex]
            'theta': theta [float]
        '''
        d = float(d)

        a = self.Q(d)[0][0]
        b = self.Q(d)[0][1]
        d = self.Q(d)[1][1]

        q1inv = .5*(a + d + np.sqrt((a - d)**2. + 4.*b**2.))
        q2inv = .5*(a + d - np.sqrt((a - d)**2. + 4.*b**2.))

        if q1inv == q2inv:
            theta = 0.
        else:
            theta = .5*np.arcsin(2.*b/(q1inv - q2inv))

        try:
            a = 1/q1inv
        except ZeroDivisionError:
            a = np.inf
        try:
            b = 1/q2inv
        except ZeroDivisionError:
            b = np.inf
        return {'1': a, '2': b, 'theta':theta}

    def ROC(self, dist = 0.):
        '''Return the tuple of ROC of the beam.

        '''
        dist = float(dist)
        Q = self.QParam(dist)
        try:
            a = 1./np.real(1./Q['1'])
        except FloatingPointError:
            a = np.inf
        try:
            b = 1./np.real(1./Q['2'])
        except FloatingPointError:
            b = np.inf

        return  (a, b)

    def waistPos(self):
        '''Return the tuple of positions of the waists of the beam along Dir.

        '''
        Q = self.QParam(0.)
        return (-np.real(Q['1']), -np.real(Q['2']))

    def rayleigh(self):
        '''Return the tuple of Rayleigh ranges of the beam.

        '''
        Q = self.QParam()
        return (np.abs(np.imag(Q['1'])), np.abs(np.imag(Q['2'])))

    def width(self, d = 0.):
        '''Return the tuple of beam widths.

        '''
        d = float(d)
        lam = self.Wl/self.N
        zR = self.rayleigh()
        D = self.waistPos()

        return (np.sqrt((lam/pi)*((d - D[0])**2. + zR[0]**2.)/zR[0]) ,
                np.sqrt((lam/pi)*((d - D[1])**2. + zR[1]**2.)/zR[1]))

    def waistSize(self):
        '''Return a tuple with the waist sizes in x and y.

        '''
        pos = self.waistPos()
        return (self.width(pos[0])[0], self.width(pos[1])[1] )

    def gouy(self, d = 0.):
        '''Return the tuple of Gouy phases.

        '''
        d = float(d)
        zR = self.rayleigh()
        WDist = self.waistPos()
        return (np.arctan((d-WDist[0])/zR[0]),
                np.arctan((d-WDist[1])/zR[1]))

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
    Wl = float(Wl)
    Wx = float(Wx)
    Wy = float(Wy)
    qx = complex(- float(WDistx)  + 1.j * pi*Wx**2./Wl )
    qy = complex(- float(WDisty)  + 1.j * pi*Wy**2./Wl )
    QTens = np.array([[1./qx, 0.],[0., 1./qy]],
                        dtype = np.complex64)

    if Ref is None:
        Ref = "Beam" + str(GaussianBeam.BeamCount)
    else:
        Ref = Ref

    return GaussianBeam(Q = QTens, N = 1., Wl = Wl, P = P,
        Pos = Pos, Dir = Dir,
        Ux = u, Uy = v, Ref = Ref, OptDist = 0.,
        Length = 0., StrayOrder = 0, Optic = 'Laser', Face = 'Out')
