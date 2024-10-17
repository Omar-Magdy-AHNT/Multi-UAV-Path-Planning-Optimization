from Data import *
def Dist(p1,p2):
    x = p1[0]
    y = p1[1]
    z = p1[2]

    x1 = p2[0]
    y1 = p2[1]
    z1 = p2[2]

    L = ((x-x1)**2 + (y-y1)**2 + (z1-z)**2)**0.5

    if L>mpd:
        return False    
    return True