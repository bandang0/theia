'''Module to initiate all global variables for theia.'''

# Provides:
#   init

def init(dic):
    '''Initiate globals with dictionary.

    dic: dictionary holding values for globals. [dictionary]

    '''
    # these are *all* the theia globals
    global info
    global warning
    global text
    global cad
    global fname
    global fclib
    global antiClip
    global short
    global clipFactor   # portion of beam inside optic to determine whether
                        # clipping has occurred.
    global FCFactor     # factor to compensate for FreeCAD units

    #geometry
    global zero #geometrical 0 distance (for separation)
    global inf  # geometrical infinite
    global flatK    # curvature of a flat surface

    #dictionary of orders in which input is given in .tia
    global inOrder
    global types
    global typeStrings

    #geometry
    zero = 1.e-10
    inf = 1.e15
    flatK = 1.e-5
    clipFactor = 2.
    FCFactor = 0.001

    #order of data in .tia
    inOrder = {

    'bm': ['Wx','Wy','WDistx','WDisty','Wl','P',
            'X','Y','Z','Theta','Phi','Alpha','Ref'],

    'mr': ['X','Y','Z','Theta','Phi','Wedge','Alpha',
            'HRK','ARK','Diameter','Thickness','N','HRr','HRt','ARr','ARt',
            'KeepI', 'Ref'],

    'sp': ['RonHR', 'TonHR', 'RonAR', 'TonAR',
            'X','Y','Z','Theta','Phi','Wedge','Alpha',
            'HRK','ARK','Diameter','Thickness','N','HRr','HRt','ARr','ARt',
            'KeepI', 'Ref'],

    'bs': ['X','Y','Z','Theta','Phi','Wedge','Alpha',
            'HRK','ARK','Diameter','Thickness','N','HRr','HRt','ARr','ARt',
            'KeepI', 'Ref'],

    'th': ['X','Y','Z','Theta','Phi','Focal','Diameter',
            'R','T','KeepI','Ref'],

    'tk': ['X','Y','Z','Theta','Phi','K1','K2','Diameter',
            'Thickness','N','R','T','KeepI','Ref'],

    'bd': ['X','Y','Z','Theta','Phi','Diameter','Thickness', 'Ref'],
    'gh': ['X','Y','Z','Theta','Phi','Diameter', 'Ref'],
    'bo': ['X', 'Y', 'Z']}

    # expected types of inputs
    types = {'X': float, 'Y': float, 'Z': float,
            'Theta': float, 'Phi': float, 'Diameter': float,
            'Thickness': float, 'Ref': str, 'K1': float, 'K2': float,
            'KeepI': bool, 'T': float, 'R': float, 'N': float, 'Focal': float,
            'HRK': float, 'ARK': float,
            'HRr': float, 'HRt': float,'ARr': float,'ARt': float,
            'Wedge': float, 'Alpha': float,
            'RonHR': int, 'TonHR': int, 'RonAR': int, 'TonAR': int,
            'Wx': float, 'Wy': float, 'WDistx': float, 'WDisty': float,
            'Wl': float, 'P': float}

    #strings to print types
    typeStrings = {float: 'float', int: 'int', str: 'string', bool: 'boolean'}

    #parsed from command line
    info = dic['info']
    warning = dic['warning']
    text = dic['text']
    cad = dic['cad']
    fname = dic['fname']
    fclib = dic['fclib']
    antiClip = dic['antiClip']
    short = dic['short']
