from GA.GA_Param import *

def PointValid(p1, a1, i): 
    if p1 in obstlist:
        print(f"Point {p1} is in the obstacle list.")
        return False  
    count = a1[0:i].count(p1)
    if count > 0:
        print(f"Point {p1} is already in the list.")
        return False
    if p1 in startpoint:
        print(f"Point {p1} is already a start point.")
        return False
    if p1 in endpoint:
        print(f"Point {p1} is already an end point.")
        return False
    return True
