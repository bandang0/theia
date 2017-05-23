'''Geometry module for theia.'''

# Provides:
#   refrAngle
#   linePlaneInter
#   lineSurfInter
#   lineCylInter
#   newDir

import numpy as np
np.seterr(divide = 'raise', invalid = 'raise')  # np raises FloatingPointError

from tools import TotalReflectionError
from . import settings

def refrAngle(theta, n1, n2):
    '''Returns the refraction angle at n1/n2 interface for incoming theta.

        May raise a TotalReflectionError.
    '''
    try:
        return np.arcsin(n1*np.sin(theta)/n2)
    except FloatingPointError:
        msg = 'Total reflection occured.'
        raise TotalReflectionError(msg)

def linePlaneInter(pos, dirV, planeC, normV, diameter):
    '''Computes the intersection between a line and a plane.

    pos: position of the begining of the line. [3D vector]
    dirV: directing vector of the line. [3D vector]
    planeC: position of the center of the plane. [3D vector]
    normV: vector normal to the plane. [3D vector]
    diameter: diameter of the plane.

    Returns a dictionary with keys:
        'isHit': whether of not the plane is hit. [boolean]
        'distance': geometrical distance from line origin to intersection point.
            [float]
        'intersection point': position of intersection point. [3D vector]


    '''
    noInterDict = {'isHit': False,  # return this if no intersect
            'distance': 0.,
            'intersection point': np.array([0., 0., 0.], dtype=np.float64)
            }

    # If plane and dirV are orthogonal then no intersection
    if np.dot(normV, dirV) == 0.:
        return noInterDict

    # If not then there is a solution to pos + lam*dirV in plane, it is:
    lam = np.dot(normV, planeC - pos)/np.dot(normV, dirV)

    # If lam is *negative* no intersection
    if lam <= settings.zero:
        return noInterDict

    # find intersection point:
    intersect = pos + lam * dirV
    dist = np.linalg.norm(intersect - planeC)

    # if too far from center, no intersection:
    if dist >= diameter / 2.:
        return noInterDict

    return {'isHit': True,
            'distance': lam,
            'intersection point': intersect}


def lineSurfInter(pos, dirV, chordC, chordNorm, kurv, diameter):
    '''Computes the intersection between a line and a spherical surface.

    The spherical surface is supposed to have a cylindrical symmetry around
        the vector normal to the 'chord', ie the plane which undertends
        the surface.

    Note: the normal vector always looks to the center of the sphere and the
        surface is supposed to occupy less than a semi-sphere

    pos: position of the begingin of the line. [3D vector]
    dirV: direction of the line. [3D vector]
    chordC: position of the center of the 'chord'. [3D vector]
    chordNorm: normal vector the the chord in its center. [3D vector]
    kurv: curvature (1/ROC) of the surface. [float]
    diameter: diameter of the surface. [float]

    Returns a dictionary with keys:
        'is Hit': whether the surface is hit or not. [boolean]
        'distance': distance to the intersection point from pos. [float]
        'intersection point': position of intersection point. [3D vector]

    '''
    noInterDict = {'isHit': False,  # return this if no intersect
            'distance': 0.,
            'intersection point': np.array([0., 0., 0.], dtype=np.float64)}

    # if surface is too plane, it is a plane
    if np.abs(kurv) < settings.flatK:
        return linePlaneInter(pos, dirV, chordC, chordNorm, diameter)


    # find center of curvature of surface:
    try:
        theta = np.arcsin(diameter*kurv/2.)  # this is half undertending angle
    except FloatingPointError:
        theta = np.pi/2.
    sphereC = chordC + np.cos(theta)*chordNorm/kurv
    R = 1/kurv  # radius
    PC = sphereC - pos  # vector from pos to center of curvature

    # first find out if there is a intersection between the line and the whole
    # sphere. a point pos + lam * dirV is on the sphere if and only if it is
    # at distance R from sphereC.

    # discriminant of polynomial ||pos + lam*dirV - sphereC||**2 = R**2
    delta = 4.*(np.dot(dirV,PC))**2. + 4.*(R**2. - np.linalg.norm(PC)**2.)

    if delta <= 0.:
        # no intersection at all or beam is tangent to surface
        return noInterDict

    # intersection parameters
    lam1 = ( 2.*np.dot(dirV, PC) - np.sqrt(delta))/2.  # < lam2
    lam2 = ( 2.*np.dot(dirV, PC) + np.sqrt(delta))/2.

    if lam1 < settings.zero and lam2 < settings.zero:
        # sphere is behind
        return noInterDict

    if lam1 < settings.zero and lam2 > settings.zero:
        # we found a point and have to verify that its on the surface (we
        # already know its on the sphere)
        intersect = pos + lam2 * dirV
        localNorm = sphereC - intersect
        localNorm = localNorm/np.linalg.norm(localNorm)

        # compare angles theta and thetai (between chordN and localN) to
        # to know if the point is on the coated surface
        if np.dot(localNorm, chordNorm) < 0.:
            # the intersection point is on the wrong semi-sphere:
            return noInterDict

        if np.linalg.norm(np.cross(localNorm, chordNorm)) < diameter * kurv/2. :
            # it is on the surface
            return {'isHit': True,
                    'distance': lam2,
                    'intersection point': intersect}

    if lam1 > settings.zero and lam2 > settings.zero:
        # we got two points, take the closest which is on the surface
        intersect = pos + lam1 * dirV
        localNorm = sphereC - intersect
        localNorm = localNorm/np.linalg.norm(localNorm)

        if np.dot(localNorm, chordNorm) > 0. :
            if np.linalg.norm(np.cross(localNorm, chordNorm))\
                            < diameter * kurv/2.:
                            # the first is on the surface
                return {'isHit': True,
                        'distance': lam1,
                        'intersection point': intersect}

        # try the second
        intersect = pos + lam2 * dirV
        localNorm = sphereC - intersect
        localNorm = localNorm/np.linalg.norm(localNorm)

        if np.dot(localNorm, chordNorm) > 0. :
            if np.linalg.norm(np.cross(localNorm, chordNorm))\
                            < diameter * kurv/2. :
                # the second is on the surface
                return {'isHit': True,
                    'distance': lam2,
                    'intersection point': intersect}

    return noInterDict

def lineCylInter(pos, dirV, faceC, normV, thickness, diameter):
    '''Computes the intersection of a line and a cylinder in 3D space.

    The cylinder is specified by a disk of center faceC, an outgoing normal
    normV, a thickness (thus behind the normal) and a diameter.

    pos: origin of the line. [3D vector]
    dirV: directing vector of the line. [3D vector]
    faceC: center of the face of the cylinder where lies the normal vector.
        [3D vector]
    normV: normal vector to this face (outgoing). [3D vector]
    thickness: thickness of the cylinder (counted from faceC and behind normV)
        [float]
    diameter: of the cylinder. [float]

    Returns a dictionary with keys:
        'isHit': whether of not. [boolean]
        'distance': geometrical distance of the intersection point from pos.
            [float]
        'intersection point': point of intersection. [3D vector]

    '''
    diameter = float(diameter)
    thickness = float(thickness)

    noInterDict = {'isHit': False,  # return this if no intersect
            'distance': 0.,
            'intersection point': np.array([0., 0., 0.], dtype=np.float64)}

    # if the line is parallel to the axis of the cylinder, no intersection
    if np.abs(np.dot(dirV,normV)) == 1.:
        return noInterDict

    # parameters
    PC = faceC - pos
    dirn = np.dot(dirV, normV)
    PCn = np.dot(PC, normV)
    PCdir = np.dot(PC, dirV)
    PC2 = np.dot(PC,PC)
    R = diameter/2
    center = faceC - thickness*normV/2.    # center of cylinder
    dist = np.sqrt(R**2. + thickness**2./4.)    # distance from center to edge

    # the cylinder's axis is faceC + x*normV for x real. this axis is at
    # a distance R to pos + lam*dirV if a P(lam)=0 whose discriminant is:
    delta = 4.*(dirn*PCn - PCdir)**2. - 4.*(1.-dirn**2.)*(PC2 - R**2. - PCn**2.)

    if delta <= 0.:
        #no intersection or line is tangent
        return noInterDict

    # intersection parameters
    lam1 = (2.*(PCdir - dirn*PCn) - np.sqrt(delta))/(2.*(1. - dirn**2.))# < lam2
    lam2 = (2.*(PCdir - dirn*PCn) + np.sqrt(delta))/(2.*(1. - dirn**2.))

    if lam1 < settings.zero and lam2 < settings.zero:
        # cylinder is behind
        return noInterDict

    if lam1 < settings.zero and lam2 > settings.zero:
        # we found a point and have to verify that its on the physical surface
        intersect = pos + lam2 * dirV

        # check if it is at distance sqrt(R**2 + dia**2/4) or less to center:
        if np.linalg.norm(intersect - center) < dist:
            # it is on the cylinder
            return {'isHit': True,
                    'distance': lam2,
                    'intersection point': intersect}

    if lam1 > settings.zero and lam2 > settings.zero:
        # we got two points, take the closest which is on the surface
        intersect = pos + lam1 * dirV

        if np.linalg.norm(intersect - center) < dist:
            # the first is on the surface
            return {'isHit': True,
                    'distance': lam1,
                    'intersection point': intersect}

        # try the second
        intersect = pos + lam2 * dirV

        if np.linalg.norm(intersect - center) < dist :
            # the second is on the surface
            return {'isHit': True,
                    'distance': lam2,
                    'intersection point': intersect}

    return noInterDict


def newDir(inc, nor, n1, n2):
    '''Computes the refl and refr directions produced by inc at interface n1/n2.

    inc: director vector of incoming beam. [3D vector]
    nor: normal to the interface at the intersection point. [3D vector]
    n1: refractive index of the first medium. [float]
    n2: idem.

    Returns a dictionary with keys:
        'r': normalized direction of reflected beam. [3D vector]
        't': normalized direction of refracted beam. [3D vector]
        'TR': was there total reflection?. [boolean]

    Note: if total reflection then refr is None.

    '''
    # normal incidence case:
    if np.abs(np.dot(inc,nor)) == 1.:
        return {'r': nor,
                't': inc,
                'TR': False}

    # reflected (see documentation):
    refl = inc - 2.*np.dot(inc,nor)*nor
    refl = refl/np.linalg.norm(refl)

    # incident and refracted angles
    theta1 = np.arccos(- np.dot(nor,inc))
    try:
        theta2 = refrAngle(theta1, n1, n2)
    except TotalReflectionError :
        return {'r': refl,
                't': None,
                'TR': True}

    # sines and cosines
    c1 = np.cos(theta1)
    c2 = np.cos(theta2)
    s1 = np.sin(theta1)

    alpha = n1/n2
    beta = n1*c1/n2 - c2

    # refracted:
    refr = (alpha*inc + beta*nor)
    refr = refr/np.linalg.norm(refr)
    return {'r': refl,
            't': refr,
            'TR': False}

def rotMatrix(a,b):
    '''Provides the rotation matrix which maps a (unit) to b (unit).

    a,b: unit 3D vectors. [3D np.arrays]

    Returns an np.array such that np.matmul(M,a) == b.

    '''

    if np.abs(np.dot(a,b)) == 1.:
        return np.dot(a,b) *np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]],
                                    dtype=np.float64)

    v = np.cross(a,b)
    vx = np.array([0., -v[2], v[1]], [v[2], 0., -v[0]], [-v[1], v[0], 0.],
                    dtype=np.float64)

    return np.array([1., 0., 0.], [0., 1., 0.], [0., 0., 1.], dtype=np.float64)\
            + vx + (1.0/(1.0 + np.dot(a,b)))*np.matmul(vx,vx)

def basis(a):
    '''Returns two vectors u and v such that (a, u, v) is a direct ON basis.

    '''
    ez = np.array([0., 0., 1.], dtype = np.float64)

    if np.abs(np.dot(a, ez)) == 1.:
        u = np.dot(a, ez) * np.array([1., 0., 0.], dtype = np.float64)
        v = np.array([0., 1., 0.], dtype = np.float64)
        return u,v
    else:
        theta = np.arccos(np.dot(a, ez))
        try:
            u = ez/np.sin(theta) - a/np.tan(theta)
        except FloatingPointError:  #tan(pi/2) = inf
            u = ez
        v = np.cross(a, u)
        u = u/np.linalg.norm(u)
        v = v/np.linalg.norm(v)
        return u, v
