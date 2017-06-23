'''Main module of theia, defines the main function.'''

# Provides:
#   main

import os
import sys
import subprocess
from .helpers import settings
from .helpers.interaction import welcome, errorRecursion, errorUnknown
from .helpers.interaction import errorAtSpecifiedLocation, errorWhereIs
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
    dic['fname'] = os.path.splitext(args[1])[0] #relative path without '.tia'
    dic['fclib'] = options.fclib

    # initiate globals
    settings.init(dic)

    #exit with error if file not found
    if not os.path.isfile(settings.fname + '.tia'):
        print "theia: Error: %s.tia: No such file.\nAborting." %settings.fname
        sys.exit(1)

    #create simulation object with name the basename (not path)
    FName = settings.fname.split('/')[len(settings.fname.split('/')) - 1]
    simu = simulation.Simulation(FName)

    #welcome to theia
    print welcome

    #load initial data
    print "theia: Run: Reading input data."
    try:
        simu.load()
    except InputError as IE:
        print "theia: Error: %s\nAborting." %IE.Message
        sys.exit(1)

    print "theia: Run: Done."

    #run simulation
    print "theia: Run: Running simulation."
    try:
        simu.run()
    except RuntimeError:
        print "theia: Error: Maximum recursion depth reached."\
                    + errorRecursion + "\nAborting."
        sys.exit(1)
    print "theia: Run: Done."

    #write results to .out file
    if settings.text:
        print "theia: Run: Writing output file."
        simu.writeOut()
        print "theia: Run: Done."

    #write CAD file
    if settings.cad:
        if settings.fclib is not None:
            print "theia: Run: Loading FreeCAD library from specified location."
            FREECADPATH = settings.fclib
            sys.path.append(FREECADPATH)
            try:
                import FreeCAD as App
                import Part
            except ImportError:
                print errorAtSpecifiedLocation %settings.fclib
                sys.exit(1)
            print "theia: Run: Done."
        else:
            print "theia: Run: Searching for FreeCAD library."
            cmd = "whereis freecad"
            output = subprocess.check_output(cmd, shell = True).split()
            if len(output) < 3:
                print errorWhereIs
                sys.exit(1)
            else:
                FREECADPATH = output[2] + '/lib'
                sys.path.append(FREECADPATH)
                print "theia: Run: Loading FreeCAD library from %s." \
                        %FREECADPATH
                try:
                    import FreeCAD as App
                    import Part
                except ImportError:
                    print errorUnknown %FREECADPATH
                    sys.exit(1)
                print "theia: Run: Done."

        print "theia: Run: Writing CAD file."
        simu.writeCAD()
        print "theia: Run: Done."

    sys.exit(0)
