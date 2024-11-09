from Data import *

def func1(d,A):
    dist = []
    for i in range(numdrones):
        tdist = 0
        start_idx = i * (numtrackp + 2)  # Start index for current drone
        end_idx = (i + 1) * (numtrackp +2)-1  # End index for current drone
        for j in range(start_idx, end_idx):
            x = A[d][j][0]
            y = A[d][j][1]
            z = A[d][j][2]
            x1 = A[d][1+j][0]
            y1 = A[d][1+j][1]
            z1 = A[d][1+j][2]
            tdist = tdist + (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
        dist.append(tdist)
    return dist