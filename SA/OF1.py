from Data import *

def func1():
    for i in range(numdrones):
        tdist = 0
        for j in range(numtrackp+2):
            x = Droneinfo[(i*4)+j][0]
            y = Droneinfo[(i*4)+j][1]
            z = Droneinfo[(i*4)+j][2]
            x1 = Droneinfo[(i*4)+j+1][0]
            y1 = Droneinfo[(i*4)+j+1][1]
            z1 = Droneinfo[(i*4)+j+1][2]
            tdist = tdist + (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
        distDrone.append(tdist)
