from Data import *

import numpy as np

def create_3d_map():

    map_3d = np.zeros((gridsize, gridsize, gridsize), dtype=int)
    

    for obstacle in obstlist:
        x, y, z = obstacle
        if 0 <= x < gridsize and 0 <= y < gridsize and 0 <= z < gridsize:
            map_3d[x, y, z] = 1 
    
    return map_3d

print(create_3d_map())