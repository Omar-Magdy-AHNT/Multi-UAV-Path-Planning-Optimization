import numpy
from GA.GA_Param import *

def vertical_check(p1,p2,p3):
    print(p1,p2,p3)
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
    
    if L1+L2<L3 or L1+L3<L2 or L2+L3<L1:
        return False
    
    a = numpy.arccos((L1**2 + L2**2 - L3**2)/(2*L1*L2))

    if a>amax:
        return False
    return True