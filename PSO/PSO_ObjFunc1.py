from PSO.PSO_Param import *

def func1( A):
    dist = []
    for i in range(numdrones):
        tdist = 0
        # Calculate the start and end index for the current drone's path
        start_idx = i * (numtrackp + 2)  # Start index for current drone
        end_idx = (i + 1) * (numtrackp + 2)  # End index for current drone (inclusive of the last point)
        
        # Now, calculate the distance over the entire path for this drone
        for j in range(start_idx, end_idx - 1):  # Avoid out-of-bounds by stopping before the last point
            # Current point
            x = A[j][0]
            y = A[j][1]
            z = A[j][2]
            # Next point
            x1 = A[j + 1][0]
            y1 = A[j + 1][1]
            z1 = A[j + 1][2]
            # Calculate distance and accumulate
            tdist += (((x - x1)**2) + ((y - y1)**2) + ((z - z1)**2))**0.5
        
        dist.append(tdist)
    
    return dist

