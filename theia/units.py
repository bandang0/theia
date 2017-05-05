'''Various units for theia.'''

import numpy as np
pi = np.pi

# Length units
km = 1.e3
m = 1.0
cm = 0.01
mm = 1.e-3
um = 1.e-6
nm = 1.e-9


# Power units
kW = 1.e3
W = 1.0
mW = 1.e-3
uW = 1.e-6

# Frequencies
THz = 1.e12
GHz = 1.e9
MHz = 1.e6
kHz = 1.e3
Hz = 1.0
mHz = 1.e-3
uHz = 1.e-6

# Other
ppm = 1.e-6
rad = 1.0
deg = 1.7453292519943295e-2

# Conversion Functions

def rad2deg(rad):
    return rad * 180.0 / pi

def deg2rad(deg):
    return deg * pi /180.0
