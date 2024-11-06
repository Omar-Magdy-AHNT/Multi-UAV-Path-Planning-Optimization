from Data import *

def func2(i):
    b=0
    for i in range(numdrones):
        totaldanger = 0
        for j in range(numtrackp):
            x = Droneinfo[i][j+(i*4)][0]
            y = Droneinfo[i][j+(i*4)][1]
            z = Droneinfo[i][j+(i*4)][2]
            b = 0
            for k in range(len(obstlist)):
                x1 = obstlist[k][0]
                y1 = obstlist[k][1]
                z1 = obstlist[k][2]
                dist = (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
                b = b + (dsafe/dist)**2  
            totaldanger = totaldanger + b          
        danger.append(totaldanger)