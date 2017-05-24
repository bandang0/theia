'''Defines the ThinLens class for theia.'''

# Provides:
#   class ThinLens
#       __init__
#       lineList

import numpy as np
from helpers import settings
from helpers.units import *
from helpers.geometry import rectToSph
from optics.lens import Lens

class ThinLens(Lens):
    '''

    ThinLens class.

    This class represents thin lenses, which are specified only by their focal
    lengths, diameter, position and orientation. Only the constructor and the
    printing distinguishes thin lenses (in implementation) from other lenses.

    *=== Attributes ===*
    SetupCount (inherited): class attribute, counts all setup components.
        [integer]
    OptCount (inherited): class attribute, counts optical components. [string]
    HRCenter (inherited): center of the 'chord' of the HR surface. [3D vector]
    HRNorm (inherited): unitary normal to the 'chord' of the HR (always pointing
        towards the outside of the component). [3D vector]
    Thick (inherited): thickness of the optic, counted in opposite direction to
        HRNorm. [float]
    Dia (inherited): diameter of the component. [float]
    Name (inherited): name of the component. [string]
    Ref (inherited): reference string (for keeping track with the lab). [string]
    ARCenter (inherited): center of the 'chord' of the AR surface. [3D vector]
    ARNorm (inherited): unitary normal to the 'chord' of the AR (always pointing
        towards the outside of the component). [3D vector]
    N (inherited): refraction index of the material. [float]
    HRK, ARK (inherited): curvature of the HR, AR surfaces. [float]
    HRr, HRt, ARr, ARt (inherited): power reflectance and transmission
        coefficients of the HR and AR surfaces. [float]
    KeepI (inherited): whether of not to keep data of rays for interference
        calculations on the HR. [boolean]
    Focal: Focal length of the lens. [float]

    **Note**: the curvature of any surface is positive for a concave surface
    (coating inside the sphere).
    Thus kurv*HRNorm/|kurv| always points to the center
    of the sphere of the surface, as is the convention for the lineSurfInter of
    geometry module. Same for AR.

    *******     HRK > 0 and ARK > 0     *******           HRK > 0 and ARK < 0
     *****                               ********         and |ARK| > |HRK|
     H***A                               H*********A
     *****                               ********
    *******                             *******

    '''

    def __init__(self, Focal = 10*cm, KeepI = None, Theta = None, Phi = None,
                Diameter = None, R = None, T = None,
                X = 0., Y = 0., Z = 0., Name = None, Ref = None):
        '''ThinLens constructor.

        Parameters are the attributes.

        Returns a ThinLens.

        '''
        # empty constructor
        if Theta is None:
            Theta = np.pi/2.
        if Phi is None:
            Phi = 0.
        if Focal is None:
            Focal = 10*cm
        if R is None:
            R = .1
        if T is None:
            T = .9
        if Name is None:
            Name = "ThinLens"

        Norm = np.array([np.sin(Theta)*np.cos(Phi),
                        np.sin(Theta) * np.sin(Phi),
                        np.cos(Theta)], dtype = np.float64)

        # initialize with lens mother constructor
        super(Lens, self).__init__(ARCenter = None, ARNorm = None, N = None,
                HRK = None, ARK = None,
                ARr = R, ARt = T, HRr = R, HRt = T, KeepI = KeepI,
                HRCenter = [X, Y, Z], HRNorm = Norm, Thickness = None,
                Diameter = Diameter, Name = Name, Ref = Ref)

        # initialize focal and curvatures for thin lenses
        self.Focal = float(Focal)
        # thin lens approximation of lensmaker's equation
        self.HRK = - 0.5/(self.Focal*(self.N - 1.))
        self.ARK = self.HRK
        self.ARNorm = - self.HRNorm

        # calculate  ARCenter, ARNorm  and HRCenter with focal
        if self.Focal >= 0.:
            self.Thick = settings.zero
            #separate AR/HR
            self.ARCenter = self.HRCenter + settings.zero * self.ARNorm
        else:
            try:    #arcsin might fail, if it does then the semi angle is pi/2
                theta = np.arcsin(self.Dia * self.HRK/2.)   # half angle
            except FloatingPointError:
                theta = np.pi/2.
            self.Thick = settings.zero + 2.*(1.-np.cos(theta))/self.HRK
            cen = self.HRCenter
            self.HRCenter = cen + self.Thick*self.HRNorm/2.
            self.ARCenter = cen - self.Thick*self.HRNorm/2.

        #warns on geometry
        if settings.warning:
            self.geoCheck("thinlens")


    def lines(self):
        '''Returns the list of lines necessary to print the object.
        '''
        ans = []
        ans.append("ThinLens: " + self.Name + " (" + str(self.Ref) + ") {")
        ans.append("Diameter: " + str(self.Dia/cm) + "cm")
        ans.append("Focal: " + str(self.Focal/mm) + "mm")
        ans.append("Center: " + str(self.HRCenter))
        sph = rectToSph(self.HRNorm)
        ans.append("Norm: (" + str(sph[0]/deg) + ', ' \
                + str(sph[1]/deg) + ')deg')
        ans.append("R, T: " + str(self.HRr) + ", " + str(self.HRt) )
        ans.append("}")

        return ans
