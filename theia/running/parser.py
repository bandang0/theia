'''Module for the parsing on input data from .tia file.'''

# Provides:
#   readIn
#   dicOf

import numpy as np
from ..helpers import settings
from ..helpers.units import *
from ..helpers.tools import InputError

# these defs are for evaluation from input file
pi = np.pi
cos = np.cos
sin = np.sin
tan = np.tan
arcsin = np.arcsin
arccos = np.arccos
arctan = np.arctan
sqrt = np.sqrt
exp = np.exp

def readIn(name):
    '''Finds the input data in a file.

    Returns a list of tuples where tuple[0] identifies the object of which data
    has been found and tuple[1] the data itself. tuple[1] may be a simple value
    or a dictionary for constructors, etc.

    Example return value: [ ('bd', {'X': 0., 'Y': 0., 'Z': 1.}),    #constructor
                            ('LName', 'foo')]   #string data.

    name: file to read. [string]

    May raise an InputError.

    Returns a list of tuples.

    '''

    #error messages
    malformed = "Malformed input in %s, line %s. Could not %s '%s'"

    #possible tags in beginning of lines
    tags = ['bm', 'mr', 'bs', 'sp', 'bo', 'th', 'tk', 'bd', 'gh']
    ans = list()

    with open(name, 'r') as inF:
        for (j, line) in enumerate(inF):
            line = line.translate(None, '\t \n')  #no spaces or tabs or newline
            if '#' in line:
                line = line[0:line.find('#')]   #no comments
            if len(line) < 2:
                continue
            elif line[0:5] == 'order':
                word = line[6:]
                try:
                    ans.append(('order', int(eval(word))))
                except (SyntaxError, NameError):
                    raise InputError((malformed + '.') \
                                    %(fileName, str(j + 1), 'parse', word))
                except TypeError:
                    raise InputError((malformed + 'to int') \
                                    %(fileName, str(j + 1), 'cast', word))

            elif line[0:9] == 'threshold':
                word = line[10:]
                try:
                    ans.append(('threshold', float(eval(word))))
                except (SyntaxError, NameError):
                    raise InputError(malformed + "."\
                                    %(fileName, str(j + 1), 'parse', word))
                except TypeError:
                    raise InputError((malformed + "to float.") \
                                    %(fileName, str(j + 1), 'cast', word))

            elif line[0:2] in tags:
                ans.append((line[0:2], dicOf(line[0:2], line[2:], name, j + 1)))
            else:
                ans.append(('LName', line[0:]))

    return ans

def dicOf(st, line, fileName, lineNumber):
    '''Extract the initializer dictionary from a line.

    st: object tag, 'bm', 'th', ... [string]
    line: line of data in .tia format (supposed no spaces nor tabs nor comments)
    and without the obect tag. [string]
    fileName: name of file (used to write errors). [string]
    lineNumber: number fo this line in the file (used to write errors). [int]

	May raise an InputError
	Returns a dictionary ready for construction.

    '''
    #error message
    malformed = "Malformed input in %s, line %s, entry %s"
    ans = dict()

    #allow empty constructor
    if line == '':
        return ans

    words = line.split(',')
    explicit = False

    if len(words) > len(settings.inOrder[st]):
        raise InputError(
        "Malformed input in %s, line %s. To many arguments given."\
                        % (fileName, str(lineNumber)))

    for (i, word) in enumerate(words):
        if '=' in word:
            explicit = True
        if explicit and not '=' in word:
             raise InputError(
      (malformed + ". Found non explicit entry '%s' among explicit entries.")\
            % (fileName, lineNumber, str(i + 1), word))

        if explicit:
            var, val = word[:word.find('=')], word[word.find('=') + 1:]
            if var not in settings.inOrder[st]:
                raise InputError(
                (malformed + ". Unknown constructor parameter '%s'.")\
                    % (fileName, lineNumber, str(i + 1), var))
        else:
            var, val = settings.inOrder[st][i], word

        try:
            ans[var] = settings.types[var](eval(val))
        except SyntaxError:
           raise InputError((malformed + ". Could not parse '%s'.")\
                %(fileName, lineNumber, str(i + 1), val))
        except NameError:
            raise InputError(
                (malformed + ". Did not recognize reference in '%s'.")\
                    % (fileName, lineNumber, str(i + 1), val))
        except ValueError:
            raise InputError(
                (malformed + ". Expected %s for parameter %s, "\
                            + "but got '%s' which evaluates to %s.")\
                    % (fileName, lineNumber, str(i + 1),
                        settings.typeStrings[settings.types[var]], var, val,
                        settings.typeStrings[type(eval(val))]))
    return ans
