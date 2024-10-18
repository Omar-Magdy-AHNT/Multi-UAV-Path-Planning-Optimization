from Data import maxpdist  # Importing only maxpdist to avoid circular dependency

def Dist(p1, p2):

    x, y, z = p1
    x1, y1, z1 = p2

    L = ((x - x1) ** 2 + (y - y1) ** 2 + (z1 - z) ** 2) ** 0.5

    return L <= maxpdist
