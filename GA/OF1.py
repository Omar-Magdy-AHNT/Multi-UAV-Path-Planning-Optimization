from Data import *

def func1(d,A):
    for i in range(numdrones):
        tdist = 0
        for j in range(numtrackp+2):
            x = A[d][(i*4)+j][0]
            y = A[d][(i*4)+j][1]
            z = A[d][(i*4)+j][2]
            x1 = A[d][(i*4)+j+1][0]
            y1 = A[d][(i*4)+j+1][1]
            z1 = A[d][(i*4)+j+1][2]
            tdist = tdist + (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
        distDrone.append(tdist)
