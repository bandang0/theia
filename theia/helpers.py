'''Defines some generic functions for theia.'''

# Provides:


import numpy as np
import time as tm

def hitTrue(dic):
    '''To filter dicts according to their 'isHit' key.

    dic: dictionnary with 'isHit' key. [dict]

    Returns dic['isHit']

    '''
    return dic['isHit']

def rotMatrix(a,b):
    '''Provides the rotation matrix which maps a (unit) to b (unit).

    a,b: unit 3D vectors. [3D np.arrays]

    Returns an np.array such that np.matmul(M,a) == b.

    '''

    if np.abs(np.dot(a,b)) == 1.:
        return np.dot(a,b) *np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])

    v = np.cross(a,b)
    vx = np.array([0., -v[2], v[1]], [v[2], 0., -v[0]], [-v[1], v[0], 0.])

    return np.array([1., 0., 0.], [0., 1., 0.], [0., 0., 1.]) \
            + vx + (1.0/(1.0 + np.dot(a,b)))*np.matmul(vx,vx)

def basis(a):
    '''Returns two vectors u and v such that (a, u, v) is an orthonormal basis.

    '''
    if np.abs(np.dot(a, np.array([1., 0., 0.]))) == 1.:
        u = np.array([0., -1., 0.])
    else:
        u = np.cross(a, np.array([1., 0., 0. ]))
        u = u/np.linalg.norm(u)

    v = np.cross(a, u)

    return u, v

class TotalReflectionError(Exception):
    '''TotalReflectionError class.

    Is raised when an interaction results in total reflection.

    *=== Attributes ===*
    Message: exception message. [string]

    *=== Methods ===*
    __init__(self, message)

    '''

    def __init__(self, message):
        '''TotalReflectionError exception constructor.

        '''
        self.Message = message

    def __str__(self):
        '''Printing error function.

        '''
        return repr(self.Message)

def timer(func):
    '''Decorator function to log execution time of other functions.'''

    def wrapped(*args, **kw):
        t1 = tm.time()
        func(*args, **kw)
        t2 = tm.time()
        dt = t2 -t1
        st = str(func.__name__) + " exec with '" + str(*args) + "' in " \
                        + str(dt*1000.) + "ms."
        print st

    return wrapped

def formatter(stringList):
    '''Returns a formatted version of the text formed by the list of lines.
    '''
    count = 0   # counts '{' and '}'
    ans = ""
    for line in stringList:
        if '}' in line:
            count = count - 1
        ans = ans + count * '\t' + line + '\n'
        if '{' in line:
            count = count + 1


    return ans
