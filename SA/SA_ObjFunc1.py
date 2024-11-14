from SA.SA_Param import *

def func1():
    for i in range(numdrones):
        tdist = 0
        start_idx = i * (numtrackp + 2)  # Start index for current drone
        end_idx = (i + 1) * (numtrackp +2)-1  # End index for current drone
        for j in range(start_idx, end_idx):
            x = Droneinfo[j][0]
            y = Droneinfo[j][1]
            z = Droneinfo[j][2]
            x1 = Droneinfo[j+1][0]
            y1 = Droneinfo[j+1][1]
            z1 = Droneinfo[j+1][2]
            tdist = tdist + (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
        distDrone.append(tdist)
