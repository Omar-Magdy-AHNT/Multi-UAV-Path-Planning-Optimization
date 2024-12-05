import numpy as np
from GA.GA_Param import *

def func3(i,Droneinfo):
    penalty = []
    for i in range(numdrones):
        total_penalty = 0
        # Start and end index for the current drone's track points
        start_idx = i * (numtrackp + 2)  # Start index for current drone
        end_idx = (i + 1) * (numtrackp +2)  # End index for current drone

        # Iterate through the track points of the current drone
        for j in range(start_idx, end_idx-1):  
            # Get the current and previous point
            current_point = Droneinfo[i][j]
            next_point = Droneinfo[i][j+1]
            
            # Extract x, y (ignore z for this check)
            x, y, _ = current_point
            next_x, next_y, _ = next_point
            
            # Penalty for going backward in x or y direction
            if x < next_x:
                total_penalty += penalty_factor*(next_x - x)
            
            if y < next_y:
                total_penalty += penalty_factor*(next_y - y)
            
            # Calculate distance between current and previous point
            distance = np.linalg.norm(np.array(current_point) - np.array(next_point))
            
            # Penalty for exceeding maximum distance
            if distance > maxpdist:
                total_penalty += penalty_factor*(distance - maxpdist)

        penalty.append(total_penalty)
    return penalty
