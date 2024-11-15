from SA.SA_Param import *

def func2():
    for i in range(numdrones):
        totaldanger = 0
        # Start and end index for the current drone's track points
        start_idx = i * (numtrackp + 2)  # Start index for current drone
        end_idx = start_idx + numtrackp  # End index for current drone (last track point)

        # Iterate through the track points of the current drone
        for j in range(start_idx, end_idx):  
            x = Droneinfo[j][0]
            y = Droneinfo[j][1]
            z = Droneinfo[j][2]
            b = 0
            for k in range(len(obstlist)):
                x1 = obstlist[k][0]
                y1 = obstlist[k][1]
                z1 = obstlist[k][2]
                dist = (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
                b = b + (dsafe/dist)**2  
            totaldanger = totaldanger + b          
        danger.append(totaldanger)