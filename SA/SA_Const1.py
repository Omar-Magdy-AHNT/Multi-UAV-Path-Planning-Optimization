import numpy
from SA.SA_Param import *
def vertical_check(p1, p2, p3):
    # Extract coordinates
    xm, ym, zm = p1
    x, y, z = p2
    x1, y1, z1 = p3

    # Calculate distances
    L1 = ((xm - x)**2 + (ym - y)**2 + (zm - z)**2)**0.5
    L2 = ((x - x1)**2 + (y - y1)**2 + (z - z1)**2)**0.5
    L3 = ((xm - x1)**2 + (ym - y1)**2 + (zm - z1)**2)**0.5

    # Check triangle inequality
    if L1 + L2 <= L3 or L1 + L3 <= L2 or L2 + L3 <= L1:
        return False

    # Calculate the angle using the cosine rule
    cos_a = (L1**2 + L2**2 - L3**2) / (2 * L1 * L2)
    cos_a = numpy.clip(cos_a, -1, 1)  # Clamp to avoid numerical issues
    a = numpy.arccos(cos_a)

    # Check angle constraint
    if a > amax:
        return False

    return True
