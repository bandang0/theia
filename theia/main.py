'''Main module of theia, defines the main function.'''

# Provides:
#   main

import os
import sys
from .helpers import settings, interaction
from .helpers.tools import InputError
from .running import simulation

def main(options, args):
    '''Main function of theia.'''

    # global variables dic
    dic = {}
    dic['info'] = options.info
    dic['warning'] = options.warning
    dic['text'] = options.text
    dic['cad'] = options.cad
    dic['fname'] = os.path.splitext(args[1])[0] #basename

    # initiate globals
    settings.init(dic)

    #exit with error if file not found
    if not os.path.isfile(settings.fname + '.tia'):
        print "theia: Error: "+ settings.fname + '.tia: No such file.\nAborting.'
        sys.exit(1)

    #create simulation object
    simu = simulation.Simulation(settings.fname)

    #welcome to theia
    print interaction.welcomeString

    #load initial data
    print "theia: Run: Reading input data."
    try:
        simu.load()
    except InputError as IE:
        print "theia: Error: " + IE.Message + "\nAborting."
        sys.exit(1)

    print "theia: Run: Done."

    #run simulation
    print "theia: Run: Running simulation."
    simu.run()
    print "theia: Run: Done."

    #write results to .out file
    if settings.text:
        print "theia: Run: Writing output file."
        simu.writeOut()
        print "theia: Run: Done."

    #write CAD file
    if settings.cad:
        print "theia: Run: Writing CAD file."
        simu.writeCAD()
        print "theia: Run: Done."

    sys.exit(0)
