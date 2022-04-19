'''Module to define interaction functions for theia.'''

# Provides:
#	usage
#	lhelp
#   shelp
#	welcome
#	errorRecursion
#	errorAtSpecifiedLocation
#	errorWhereIs
#   errorWhereIsNotFound
#	errorUnknown

usage = "Usage: theia [options] FNAME\n\nArguments:\n"\
        + "  FNAME\t\t .tia format input file name."

lhelp = "specify the FreeCAD library location. If none is specified, theia "\
		+ "finds it using the Unix `whereis` command. If option '-c', "\
		+ "'--no-CAD'  is used, the FreeCAD search and import are skipped "\
		+ "as a whole."

shelp = 'Exclude beams propagating inside optics from text output, terminal'\
        + ' output and CAD rendering files. This also changes the way beams'\
        + ' are referenced to in these files and in the terminal output.'

welcome = u'''
\ttheia (C) 2017-2018 Rapha\u00EBl Duque
\tLicense: GNU GPLv3+ <http://gnu.org/licenses/gpl.html>
\tThis is free software: you are free to change and redistribute it.
\tThere is ABSOLUTELY NO WARRANTY, to the extent permitted by law.
'''

errorRecursion = '''

It looks like you reached the maximum recursion depth of your Python
implementation (generally around 1000). The beam tracer builds the beam tree
recursively and in your case the recursion went to far. The order and threshold
simulation parameters were made to prevent this situation. What you can do:

\t1. Make sure you're running with reasonable order and threshold parameters,
\t2. Increase the maximum recursion depth of your Python environment by placing
\t   `sys.setrecursionlimit([whatever you need])`,
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

errorWhereIsNotFound = "theia: Error: It seems that the Unix utility "\
    + "`whereis ` is not installed, thus theia cannot find the FreeCAD "\
    + "libraries.\n"\
    + "Either specify their location with the '-l, --FreeCAD-libs' option, "\
    + "or use the '-c --no-CAD' option to skip the CAD file writing step."

errorUnknown = "theia: Error: %s was used as the source directory for the "\
	+ "FreeCAD library but an error occurred, make sure your FreeCAD build is "\
	+ "correct.\nAborting."
