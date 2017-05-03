'''Trash code.'''

def ROC(self, dist = 0.):
    '''Return the tuples of ROC of the beam.

    '''
    dist = float(dist)
    Q = self.Q(dist)
    return (1./np.real(1./Q[0]),
            1./np.real(1./Q[1]) )

def width(self, d = 0.):
    '''Return the tuple of beam widths.

    '''
    d = float(d)
    lam = self.Wl/self.N
    Q = self.Q(d)
    return (1./np.sqrt(np.pi*np.imag(1./Q[0])/lam) ,
            1./np.sqrt(np.pi*np.imag(1./Q[1])/lam))

def gouy(self, d = 0.):
    '''Return the tuple of Gouy phases.

    '''
    zR = self.rayleigh
    return (np.arctan((d-self.WDistx)/zR[0]),
            np.arctan((d-self.WDisty)/zR[1]))


def waistPos(self):
    '''Return the tuple of positions of the waists of the beam along Dir.

    '''
    return (self.WDistx, self.WDisty)

def waistSize(self):
    '''Return a tuple with the waist sizes in x and y.

    '''
    return (self.Wx, self.Wy)

def rayleigh(self):
    '''Return the tuple of Rayleigh ranges of the beam.

    '''
    lam = self.Wl/self.N
    return (-np.pi*self.Wx**2./lam, -np.pi*self.Wy**2./lam)


pos1 = [0.5, 0., 0.]
pos2 = [2., 0., 0.]
pos3 = [0., 2., 0.]
pos4 = [0., 0., 0.]
pos5 = [0., 0., 0.]

dirV1 = [1., 0., 0.]
dirV2 = [-1., 0., 0.]
dirV3 = [0., 1., 0.]
dirV4 = [0., -1, 0.]

planeC1 = [4, 0, 0]
planeC2= [0., 4., 0.]

normV1 = [1., 0., 0.]
normV2 = [-1, 0., 0.]
normV3 = [0., 0., 1]

diameter1 = 4.
diameter2 = 2

chordC = [0., 3., 0.]
chordNorm1 = [0., 1., 0.]
chordNorm2 = [0., -1., 0.]

kurv1 = 1.0e-6
kurv2 = .01

# tests
print geo.linePlaneInter(pos1, dirV1, planeC1, normV1, diameter1)
print geo.linePlaneInter(pos2, dirV1, planeC1, normV1, diameter1)
print geo.linePlaneInter(pos1, dirV1, planeC1, normV2, diameter2)
print geo.linePlaneInter(pos2, dirV2, planeC2, normV3, diameter1)

print geo.lineSurfInter(pos1, dirV3, chordC, chordNorm1, kurv2, diameter1)
print geo.lineSurfInter(pos1, dirV3, chordC, chordNorm2, kurv2, diameter1)
print geo.lineSurfInter(pos1, dirV3, chordC, chordNorm1, kurv1, diameter1)
