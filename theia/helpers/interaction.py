'''Module to define interaction functions for theia.'''

# Provides:
#	usage
#	welcome
#	errorRecursion
#	errorAtSpecifiedLocation
#	errorWhereIs
#	errorUnknown

usage = "Usage: theia [options] FNAME\n\nArguments:\n"\
	+ "  FNAME\t\t .tia format input file name."

welcome = '''
\ttheia Copyright (C) 2017 R. Duque
\tLicense: GNU GPLv3+ <http://gnu.org/licenses/gpl.html>
\tThis is free software: you are free to change and redistribute it.
\tThere is ABSOLUTELY NO WARRANTY, to the extent permitted by law.
'''

errorRecursion = '''

It looks like you reached the maximum recursion depth of your Python
implementation (generally around 1000). The beam tracer builds the beam tree
recursively and in your case the recursion went to far. The order and threshold
simulation parameters were made to prevent this situation. What you can do:

\t1. Make sure you're running with reasonable order and threshold parameters;
\t2. Increase the maximum recursion depth of your Python environment by placing
\t   `sys.setrecursionlimit([whatever you need])`
\t   right under the `"if __name__ == '__main__'` line in bin/theia, rebuild
\t   theia with `make build-theia` in the project root and rerun your simulation;
\t3. Contact your local administrator to increase the maximum recursion depth
\t   on a system-wide basis and rerun your simulation.
'''

errorAtSpecifiedLocation = "theia: Error: The FreeCAD library was not found "\
	+ "at the specified location %s. Usually it is in /usr/lib/freecad/lib. "\
	+ "If you are not sure, omit the '-l', '--FREECAD-lib' option and theia "\
	+ "will find the library on its own.\nAborting."

errorWhereIs = "theia: Error: Unix command 'whereis freecad' did not yield "\
	+ "any directory. Please make sure you have FreeCAD installed and that "\
	+ "library location is in your $PATH.\nAborting"

errorUnknown = "theia: Error: %s was used as the source directory for the "\
	+ "FreeCAD library but an error occured, make sure your FreeCAD build is "\
	+ "correct.\nAborting."
