from TLBO.TLBO_Param import *  # noqa: F403


def func2(d):
    dang = []
    for i in range(numdrones):
        totaldanger = 0
        # Start and end index for the current drone's track points
        start_idx = i * (numtrackp + 2)  # Start index for current drone
        end_idx = (i + 1) * (numtrackp +2)  # End index for current drone

        # Iterate through the track points of the current drone
        for j in range(start_idx, end_idx):  
            x = d[j][0]
            y = d[j][1]
            z = d[j][2]
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
