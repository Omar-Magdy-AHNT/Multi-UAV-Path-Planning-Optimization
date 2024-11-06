from Data import *

def PointValid(p1,i): ##make sure no 2 track points are the same and no 2 drones are in the same position or no track point is in the same position as an obstacle
    if p1 in obstlist:
        return False
    count = Droneinfo[i].count(p1)
    if count > 1:
        return False
    return True