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
    global zero #geometrical 0 distance (for seperation)
    global inf  # geometrical infinite
    global flatK    # curvature of a flat surface

    #geometry
    zero = 1.e-10
    inf = 1.e15
    flatK = 1.e-5

    #parsed from command line
    info = dic['info']
    warning = dic['warning']
    text = dic['text']
    cad = dic['cad']
    fname = dic['fname']
