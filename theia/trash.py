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
