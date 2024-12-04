import numpy
from PSO.PSO_Param import *  # noqa: F403

def vertical_check(p1, p2, p3):
    xm = p1[0]
    ym = p1[1]
    zm = p1[2]

    x = p2[0]
    y = p2[1]
    z = p2[2]

    x1 = p3[0]
    y1 = p3[1]
    z1 = p3[2]

    L1 = ((xm-x)**2 + (ym-y)**2 + (zm-z)**2)**0.5
    L2 = ((x-x1)**2 + (y-y1)**2 + (z-z1)**2)**0.5
    L3 = ((xm-x1)**2 + (ym-y1)**2 + (zm-z1)**2)**0.5
    
    if L1 + L2 < L3 or L1 + L3 < L2 or L2 + L3 < L1:
        return False
    
    # Calculate the cosine of the angle using the law of cosines
    cos_value = (L1**2 + L2**2 - L3**2) / (2 * L1 * L2)
    
    # Clip the value to ensure it's within the domain of arccos [-1, 1]
    cos_value = numpy.clip(cos_value, -1, 1)

    # Calculate the angle a (in radians)
    a = numpy.arccos(cos_value)

    if a > amax:  # noqa: F405
        return False
    
    return True
