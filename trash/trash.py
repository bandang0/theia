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


if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
	usage()
	sys.exit(0)

runArgs = 	{'info': True,
			'warning': True,
			'text': True,
			'CAD': True,
			'fname': None}

if '-i' in sys.argv or '--no-info' in sys.argv:
	runArgs['info'] = False
if '-w' in sys.argv or '--no-warn' in sys.argv:
	runArgs['warning'] = False
if '-t' in sys.argv or '--no-text' in sys.argv:
	runArgs['text'] = False
if '-c' in sys.argv or '--no-cad' in sys.argv:
	runArgs['CAD'] = False

runArgs['fname'] = sys.argv[len(sys.argv) - 1]


beam2 = beam.GaussianBeam(Wx = .5*mm, Wy = .5*mm, Dir = [1, -.1, 0],
			WDistx = -1*cm, WDisty = 1*cm,
			ortho = True, Pos = [10*cm ,10*cm, 0], Ref = 'OTHER')



        with open(name, 'r') as inF:
            for line in inF.lineList():
                line = line.translate(None, ' ')  #no spaces
                if line.find('#') > -1:
                    line = line[0:line.find('#')] #no comments
                if line == '':
                    continue
                elif line[0:5] == 'order':
                    self.Order = int(line[6:line.find('\n')])
                elif line[0:9] == 'threshold':
                    self.Threshold = float(eval(line[10:line.find('\n')]))
                elif line[0:2] == 'bm':
                    toEv = 'GaussianBeam('+line[3:line.find('\n')]+')'
                    self.OptList.append(eval(toEv))
                elif line[0:2] == 'mr':
                    toEv = 'Mirror('+line[3:line.find('\n')]+')'
                    self.OptList.append(eval(toEv))
                elif line[0:2] == 'th':
                    toEv = 'ThinLens('+line[3:line.find('\n')]+')'
                    self.OptList.append(eval(toEv))
                elif line[0:2] == 'tk':
                    toEv = 'ThickLens('+line[3:line.find('\n')]+')'
                    self.OptList.append(eval(toEv))
                elif line[0:2] == 'bd':
                    toEv = 'BeamDump('+line[3:line.find('\n')]+')'
                    self.OptList.append(eval(toEv))
                else:
                    self.LName = line[0:line.find('\n')]


# Create optical objects
mirror1 = mirror.Mirror(Thickness = 1*cm, Diameter = 1*m,
			HRCenter = [1*m,0, 0], Theta = np.pi/2., Phi = np.pi,
            HRK = 0.0, ARK = 0, Wedge = 0, HRr = 0.90,
            HRt = 0.10, ARr = 0.10, ARt = .90, Name = 'Mirror1', Ref = 'M1')
print mirror1.HRNorm
#mirror2 = mirror.Mirror(Thickness = 1* cm, Diameter = 5*cm,
#            HRCenter = [0.*cm, 20*cm, 0], HRK = 0.90,
#            ARK = 0, Wedge = 0, HRr = 0.90, HRt = 0.1, ARr = 0.1, ARt = 0.90,
#            Name = 'Mirror2', Ref = 'M2')


lens = thinlens.ThinLens(Focal = 10*cm, Diameter = 15*cm, Center = [2., 0,0.],
		Ref = 'len', Norm = [-1., 0., 0.])

print lens.HRNorm
print lens.ARNorm
print lens.HRK
print lens.ARK
print lens.HRCenter
print lens.ARCenter

# beams
beam1 = beam.GaussianBeam(Wx = .5*cm, Wy = .5*cm, WDistx = 0, WDisty = 0,
            ortho = True, Pos = [0,0,0], Dir = [1., 0., 0.], Ref = 'ORI')



inBeams = [beam1]
optList = [mirror1, lens]

# parameters
threshold = -0.5*mW
order = 2


print lens.Thick
    if lens.HRK == 0.:
        R1 = 1./settings.flatK
    else:
        R1 = 1./lens.HRK

    if lens.ARK == 0.:
        R2 = 1./settings.flatK
    else:
        R2 = 1./lens.ARK

    apex = lens.apexes()

    C1 = Base.Vector(tuple(apex[0] + R1 * lens.HRNorm))
    C2 = Base.Vector(tuple(apex[1] + R2 * lens.ARNorm))
    S1 = Part.makeSphere(np.abs(R1), C1)
    S2 = Part.makeSphere(np.abs(R2), C2)

    if R1 > 0. and R2 > 0.:
        Cyl = Part.makeCylinder(lens.Dia/2., lens.Thick,
                                Base.Vector(tuple(lens.HRCenter)),
                                Base.Vector(tuple(-lens.HRNorm)))
        return Cyl.cut(S1.fuse(S2))
    if R1 < 0. and R2 < 0.:
        Cyl = Part.makeCylinder(lens.Dia/2., lens.Thick \
                                            + np.abs(R1) + np.abs(R2),
                                Base.Vector(tuple(apex[0])),
                                Base.Vector(tuple(-lens.HRNorm)))
        return S1.common(S2).common(Cyl)
    if R1 < 0. and R2 > 0.:
        Cyl = Part.makeCylinder(lens.Dia/2., lens.Thick + np.abs(R1),
                                Base.Vector(tuple(lens.ARCenter)),
                                Base.Vector(tuple(-lens.ARNorm)))
        return Cyl.common(S1.cut(S2))
    if R1 > 0. and R2 < 0.:
        Cyl = Part.makeCylinder(lens.Dia/2., lens.Thick + np.abs(R2),
                                Base.Vector(tuple(lens.HRCenter)),
                                Base.Vector(tuple(-lens.HRNorm)))
        return Cyl.common(S2.cut(S1))

def ghostShape(ghost):
    '''Computes the 3D representation of the beam, a shape for a CAD file obj.

    beam: beam to represent. [GaussianBeam]

    Returns a shape for a CAD file object.

    '''
    fact = settings.FCFactor    #factor for units in CAD
    return Part.makeCylinder((ghost.Dia/2.)/fact, 0.01/fact,
                                Base.Vector(0,0,0),
                                Base.Vector(tuple(-ghost.HRNorm)))
