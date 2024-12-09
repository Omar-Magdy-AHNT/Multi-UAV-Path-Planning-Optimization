from PSO.PSO_Param import *  # noqa: F403

def PointValid(p1, a1): 
    if p1 in obstlist:  # noqa: F405
        return False  
    count = a1.count(p1)
    if count > 0:
        return False
    return True
