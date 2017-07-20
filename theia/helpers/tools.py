'''Defines some generic functions for theia.'''

# Provides:
#   class TotalReflectionError
#       __init__
#       __str__
#   class InputError
#       __init__
#       __str___
#   timer
#   formatter

import time as tm

class TotalReflectionError(Exception):
    '''TotalReflectionError class.

    Is raised when an interaction results in total reflection.

    *=== Attributes ===*
    Message: exception message. [string]


    '''

    def __init__(self, message):
        '''TotalReflectionError exception initializer.

        '''
        self.Message = message

    def __str__(self):
        '''Printing error function.

        '''
        return repr(self.Message)

class InputError(Exception):
    '''InputError class.

    Is raised when the input .tia file parsing to input data failed.

    *=== Attributes ===*
    Message: exception message. [string]

    '''

    def __init__(self, message):
        '''InputError exception initializer.

        '''
        self.Message = message

    def __str__(self):
        '''Printing error function

        '''
        return repr(self.Message)

def timer(func):
    '''Decorator function to log execution time of other functions.'''

    def wrapped(*args, **kw):
        t1 = tm.time()
        func(*args, **kw)
        t2 = tm.time()
        dt = t2 -t1
        st = "theia: Debug: %s exec with '%s' in %s ms." \
                % (str(func.__name__), str(*args), str(dt*1000.))
        print st

    return wrapped

def formatter(stringList):
    '''Returns a formatted version of the text formed by the list of lines.'''
    count = 0   # counts '{' and '}'
    ans = ""
    for line in stringList:
        if '}' in line:
            count = count - 1
        ans = ans + count * '\t' + line + '\n'
        if '{' in line:
            count = count + 1

    return ans
