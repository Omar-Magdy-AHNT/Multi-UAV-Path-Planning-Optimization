import numpy
from Data import *

def Horz_check(p1,p2):


    x = p1[0]
    y = p1[1]
    z = p1[2]

    x1 = p2[0]
    y1 = p2[1]
    z1 = p2[2]

    H = z1-z
    L = ((x-x1)**2 + (y-y1)**2)**0.5

    if L == 0:
        b=0
    else:
        b = numpy.arctan(H/L)
    if b>bmax:
        return False    
    return True