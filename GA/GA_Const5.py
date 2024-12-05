from GA.GA_Param import *  # Importing only maxpdist to avoid circular dependency

def Dist(p1, p2):

    x, y, _ = p1
    x1, y1, _ = p2
    
    if x < x1 or y < y1 :
        return False
    
    return True
