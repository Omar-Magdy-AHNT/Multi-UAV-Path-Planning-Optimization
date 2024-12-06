from PSO.PSO_Param import *  # noqa: F403

def PointValid(p1, a1, i): 
    if p1 in obstlist:  # noqa: F405
        return False  
    count = a1[0:i].count(p1)
    if count > 0:
        return False
    if p1 in endpoint:  # noqa: F405
        return False
    return True
