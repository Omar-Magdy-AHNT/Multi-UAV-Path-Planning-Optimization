import numpy as np
from TLBO.TLBO_Param import *

def dist(p1, p2):

    distance = np.linalg.norm(np.array(p1) - np.array(p2))
    
    # Check if the distance exceeds half of the grid size
    if distance >= (gridsize // 2) :
        return False  # Reject the move
    
    return True  # Accept the move