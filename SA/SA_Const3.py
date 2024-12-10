from SA.SA_Param import *

def PointValid(p1): 
    
    if p1 in obstlist:
        return False
    
    count = Droneinfo.count(p1)
    if count > 0:
        return False
    
    return True