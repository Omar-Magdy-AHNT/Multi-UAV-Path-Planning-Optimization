from GA.GA_Param import *

def func2(i,d):
    b=0
    dang = []
    for i in range(numdrones):
        totaldanger = 0
        for j in range(numtrackp):
            x = d[i][j+(i*4)][0]
            y = d[i][j+(i*4)][1]
            z = d[i][j+(i*4)][2]
            b = 0
            for k in range(len(obstlist)):
                x1 = obstlist[k][0]
                y1 = obstlist[k][1]
                z1 = obstlist[k][2]
                dist = (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
                b = b + (dsafe/dist)**2  
            totaldanger = totaldanger + b          
        dang.append(totaldanger)
    return dang