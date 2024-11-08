from Data import *

def func1(d,A):
    dist = []
    for i in range(numdrones):
        tdist = 0
        for j in range(numtrackp+2):
            x = A[d][j+(numtrackp+2)*i][0]
            y = A[d][j+(numtrackp+2)*i][1]
            z = A[d][j+(numtrackp+2)*i][2]
            x1 = A[d][j+(numtrackp+2)*i][0]
            y1 = A[d][j+(numtrackp+2)*i][1]
            z1 = A[d][j+(numtrackp+2)*i][2]
            tdist = tdist + (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
        dist.append(tdist)
    return dist