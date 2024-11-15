from GA.GA_Param import *

def PointValid(p1, a1, i): 
    if p1 in obstlist:
        return False  
    count = a1[0:i].count(p1)
    if count > 0:
        return False
    if p1 in startpoint:
        return False
    if p1 in endpoint:
        return False
    return True
