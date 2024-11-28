import numpy as np

def func3(waypoints, goal):
    penalty = 0
    for i in range(len(waypoints) - 1):
        current_dist = np.linalg.norm(np.array(waypoints[i]) - np.array(goal))
        next_dist = np.linalg.norm(np.array(waypoints[i + 1]) - np.array(goal))
        if next_dist > current_dist:
            penalty += (next_dist - current_dist)
    return penalty