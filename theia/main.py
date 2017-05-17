'''Main module of theia, defines the main function.'''

from helpers import settings

def main(options, args):
    '''Main function of theia.'''

    # global variables dic
    dic = {}
    dic['info'] = options.info
    dic['warning'] = options.warning
    dic['text'] = options.text
    dic['cad'] = options.cad
    dic['fname'] = args[1]

    # initiate globals
    settings.init(dic)
