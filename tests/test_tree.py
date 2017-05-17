'''Test the tree module.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)

from helpers import settings
from helpers.units import *
from optics import beam, beamdump, thinlens, thicklens, mirror

# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
		'fname': 'test_optics'}

settings.init(dic)
