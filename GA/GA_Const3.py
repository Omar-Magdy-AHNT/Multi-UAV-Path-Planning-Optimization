from GA.GA_Param import *

def PointValid(p1, a1): 
    if p1 in obstlist:  
        return False  
    count = a1.count(p1)
    if count > 0:
        return False
    return True
