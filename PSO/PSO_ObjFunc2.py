from PSO.PSO_Param import *  # noqa: F403


def func2(l,d):  # noqa: E741
    dang = []
    for i in range(numdrones):  
        totaldanger = 0
        # Start and end index for the current drone's track points
        start_idx = i * (numtrackp + 2)  # Start index for current drone  
        end_idx = start_idx + numtrackp  # End index for current drone (last track point)  

        # Iterate through the track points of the current drone
        for j in range(start_idx, end_idx):  
            x = d[l][j][0]
            y = d[l][j][1]
            z = d[l][j][2]
            b = 0
            # Check distance to each obstacle in obstlist
            for k in range(len(obstlist)):  
                x1 = obstlist[k][0]  
                y1 = obstlist[k][1]  
                z1 = obstlist[k][2]
                dist = (((x - x1)**2) + ((y - y1)**2) + ((z - z1)**2))**0.5
                b += (dsafe / dist) ** 2  # Sum of danger values based on distance to obstacles
            totaldanger += b  # Accumulate total danger for the current drone
        dang.append(totaldanger)
    return dang
