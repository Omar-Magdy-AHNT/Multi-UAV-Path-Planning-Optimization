import numpy as np
from PSO.PSO_Param import *
def func3(waypoints, goal):
    p = []
    for i in range(numdrones):  
        penalty = 0
        # Start and end index for the current drone's track points
        start_idx = i * (numtrackp + 2)  # Start index for current drone  
        end_idx = (i + 1) * (numtrackp + 1)  # End index for current drone (inclusive of the last point)  
        for j in range(start_idx, end_idx):  
            current_dist = np.linalg.norm(np.array(waypoints[j]) - np.array(goal))
            next_dist = np.linalg.norm(np.array(waypoints[j+ 1]) - np.array(goal))

            if next_dist > current_dist:

                penalty += (next_dist - current_dist)

        p.append(penalty)
    return p