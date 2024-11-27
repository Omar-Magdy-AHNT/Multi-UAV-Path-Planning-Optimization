import numpy as np  # Import numpy module for numerical operations
import math  # Import math module for mathematical functions

# Number of drones in the simulation (can be adjusted based on your system)
numdrones = 2   

# Maximum permissible distance between drones (depends on controller accuracy)
maxpdist = 5 

# Size of the grid (depends on the environment setup)
gridsize = 10 

# Number of track points to be calculated based on grid size and max point distance
# The formula calculates the number of track points based on grid size and max distance
numtrackp = math.ceil((((((gridsize-0)**2)+((gridsize-0)**2)+((gridsize-0)**2))**0.5)/maxpdist) + 1)

# Safe distance between drones or obstacles
dsafe = 2

# Maximum Hotizontal angle (in radians)
amax = 75 *np.pi/180  # Convert to radians

# Maximum Vertical angle (in radians) 
bmax = 60 *np.pi/180  # Convert to radians


def set_PSO_params(n_drones, max_dist, safe_dist, ):
    global numdrones, maxpdist, gridsize, dsafe, amax, bmax, 
    numdrones = n_drones
    maxpdist = max_dist
    dsafe = safe_dist


# Output list to store the results of the simulation
Output = []

# List to store obstacle data, if applicable
obstlist = []

# Starting point for the drones (coordinates or other relevant data)
startpoint = []

# Ending point for the drones (coordinates or other relevant data)
endpoint = []
