'''Defines the ThinLens class for theia.'''

# Provides:
#   class ThinLens
#       __init__
#       lineList

import numpy as np
from units import *
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

    def __init__(self, Focal = 10*cm, KeepI = None,
                Diameter = None, R = None, T = None,
                Norm = None, Center = None, Name = None, Ref = None):
        '''ThinLens constructor.

        Parameters are the attributes.

        Returns a ThinLens.

        '''
        # initialize with lens mother constructor
        super(Lens, self).__init__(ARCenter = None, ARNorm = None, N = None,
                HRK = None, ARK = None,
                ARr = R, ARt = T, HRr = R, HRt = T, KeepI = KeepI,
                HRCenter = Center, HRNorm = Norm, Thickness = None,
                Diameter = Diameter, Name = Name, Ref = Ref)

        # initialize focal and curvatures for thin lenses
        self.Focal = float(Focal)
        self.HRK = - 0.5/self.Focal
        self.ARK = self.HRK
        self.ARNorm = - self.HRNorm

        # calculate  ARCenter, ARNorm  and HRCenter with focal
        if self.Focal >= 0.:
            self.Thick = 1.e-10
            self.ARCenter = self.HRCenter + 1.e-10 * self.ARNorm #separate AR/HR
        else:
            theta = np.arcsin(self.Dia * self.HRK/2.)   # half angle
            self.Thick = 1.e-10 + 2.*(1.-np.cos(theta))*self.HRK
            cen = self.HRCenter
            self.HRCenter = cen + self.Thick*self.HRNorm/2.
            self.ARCenter = cen - self.Thick*self.HRNorm/2.

    def lineList(self):
        '''Returns the list of lines necessary to print the object.
        '''
        ans = []
        ans.append("Lens: " + self.Name + " (" + str(self.Ref) + ") {")
        ans.append("Diameter: " + str(self.Dia/cm) + "cm")
        ans.append("Focal: " + str(self.Focal/mm) + "mm")
        ans.append("Center: " + str(self.HRCenter))
        ans.append("Norm: " + str(self.HRNorm))
        ans.append("R, T: " + str(self.HRr) + ", " + str(self.HRt) )
        ans.append("}")

        return ans
