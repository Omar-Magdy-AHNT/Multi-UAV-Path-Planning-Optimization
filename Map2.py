from Data import *

import numpy as np

def create_3d_map():

    map_3d = np.zeros((gridsize, gridsize, gridsize), dtype=int)
    
    # Iterate through the obstacle array and mark those positions in the 3D map with '1'
    for obstacle in obstlist:
        x, y, z = obstacle
        if 0 <= x < gridsize and 0 <= y < gridsize and 0 <= z < gridsize:
            map_3d[x, y, z] = 1  # Mark the obstacle position
    
    return map_3d

