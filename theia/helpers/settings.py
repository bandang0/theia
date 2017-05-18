'''Module to initiate all global variables for theia.'''

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

    #geometry
    global zero #geometrical 0 distance (for seperation)
    global inf  # geometrical infinite
    global flatK    # curvature of a flat surface

    #distionary of orders in which input is given in .tia
    global inOrder

    #geometry
    zero = 1.e-10
    inf = 1.e15
    flatK = 1.e-5

    #order of data in .tia
    inOrder = {}
    inOrder['bm'] = ['Wx','Wy','WDistx','WDisty','Wl','P',
            'X','Y','Z','Theta','Phi','Alpha','Name','Ref']

    inOrder['mr'] = ['X','Y','Z','Theta','Phi','Wedge','Alpha',
            'HRK','ARK','Diameter','Thickness','N','HRr','HRt','ARr','ARt',
            'KeepI', 'Name','Ref']

    inOrder['th'] = ['X','Y','Z','Theta','Phi','Focal','Diameter',
            'R','T','KeepI','Name','Ref']

    inOrder['tk'] = ['X','Y','Z','Theta','Phi','K1','K2','Diameter',
            'Thickness','N','R','T','KeepI','Name','Ref']

    inOrder['bd'] = ['X','Y','Z','Theta','Phi','Diameter','Thickness']

    #parsed from command line
    info = dic['info']
    warning = dic['warning']
    text = dic['text']
    cad = dic['cad']
    fname = dic['fname']
