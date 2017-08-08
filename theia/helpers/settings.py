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
                        # clipping has occured.
    global FCFactor     # factor to compensate for FreeCAD units

    #geometry
    global zero #geometrical 0 distance (for seperation)
    global inf  # geometrical infinite
    global flatK    # curvature of a flat surface

    #dictionary of orders in which input is given in .tia
    global inOrder

    #geometry
    zero = 1.e-10
    inf = 1.e15
    flatK = 1.e-5
    clipFactor = 2.
    FCFactor = 0.001

    #order of data in .tia
    inOrder = {}
    inOrder['bm'] = ['Wx','Wy','WDistx','WDisty','Wl','P',
            'X','Y','Z','Theta','Phi','Alpha','Ref']

    inOrder['mr'] = ['X','Y','Z','Theta','Phi','Wedge','Alpha',
            'HRK','ARK','Diameter','Thickness','N','HRr','HRt','ARr','ARt',
            'KeepI', 'Ref']

    inOrder['bs'] = ['X','Y','Z','Theta','Phi','Wedge','Alpha',
            'HRK','ARK','Diameter','Thickness','N','HRr','HRt','ARr','ARt',
            'KeepI', 'Ref']

    inOrder['th'] = ['X','Y','Z','Theta','Phi','Focal','Diameter',
            'R','T','KeepI','Ref']

    inOrder['tk'] = ['X','Y','Z','Theta','Phi','K1','K2','Diameter',
            'Thickness','N','R','T','KeepI','Ref']

    inOrder['bd'] = ['X','Y','Z','Theta','Phi','Diameter','Thickness', 'Ref']
    inOrder['gh'] = ['X','Y','Z','Theta','Phi','Diameter', 'Ref']
    inOrder['bo'] = ['X', 'Y', 'Z']

    #parsed from command line
    info = dic['info']
    warning = dic['warning']
    text = dic['text']
    cad = dic['cad']
    fname = dic['fname']
    fclib = dic['fclib']
    antiClip = dic['antiClip']
    short = dic['short']
