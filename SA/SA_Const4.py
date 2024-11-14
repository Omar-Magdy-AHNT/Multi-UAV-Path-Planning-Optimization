from SA.SA_Param import *

def Trackpointlinevalid(p1,p2): ##get points between each 2 track points to make sure no objects in between
    pl = bresenham_3d(p1,p2)
    for i in range(len(obstlist)):
        if obstlist[i] in pl:
            return False
    for i in range(len(Droneinfo)):
        if Droneinfo[i] in pl:
            return False
    return True

def bresenham_3d(p1, p2):
    # List to store the intermediate points on the line
    points = []
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    
    # Differences
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)

    # Signs of increments (direction of the line)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    sz = 1 if z2 > z1 else -1

    # Initialize the error terms
    if dx >= dy and dx >= dz:        # x is the major axis
        err_1 = 2 * dy - dx
        err_2 = 2 * dz - dx
        while x1 != x2 - sx:  # Stop before reaching x2
            x1 += sx
            if err_1 >= 0:
                y1 += sy
                err_1 -= 2 * dx
            if err_2 >= 0:
                z1 += sz
                err_2 -= 2 * dx
            err_1 += 2 * dy
            err_2 += 2 * dz
            points.append((x1, y1, z1))  # Add intermediate points only
    elif dy >= dx and dy >= dz:      # y is the major axis
        err_1 = 2 * dx - dy
        err_2 = 2 * dz - dy
        while y1 != y2 - sy:  # Stop before reaching y2
            y1 += sy
            if err_1 >= 0:
                x1 += sx
                err_1 -= 2 * dy
            if err_2 >= 0:
                z1 += sz
                err_2 -= 2 * dy
            err_1 += 2 * dx
            err_2 += 2 * dz
            points.append((x1, y1, z1))  # Add intermediate points only
    else:                            # z is the major axis
        err_1 = 2 * dx - dz
        err_2 = 2 * dy - dz
        while z1 != z2 - sz:  # Stop before reaching z2
            z1 += sz
            if err_1 >= 0:
                x1 += sx
                err_1 -= 2 * dz
            if err_2 >= 0:
                y1 += sy
                err_2 -= 2 * dz
            err_1 += 2 * dx
            err_2 += 2 * dy
            points.append((x1, y1, z1))  # Add intermediate points only

    return points
