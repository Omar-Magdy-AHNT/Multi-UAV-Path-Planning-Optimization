import numpy as np  # Import numpy module for numerical operations
import math  # Import math module for mathematical functions

# Number of drones to be used in the system
numdrones = 2   # depends on the number of drones

# Maximum point distance, which might represent the accuracy of the controller
maxpdist = 3  # depends on the controller accuracy 

# Grid size for the simulation or optimization task
gridsize = 10  # depends on the size of the grid

# Calculate the number of track points based on grid size and max distance between points
numtrackp = math.ceil((((((gridsize - 0) ** 2) + ((gridsize - 0) ** 2) + ((gridsize - 0) ** 2)) ** 0.5) / maxpdist) + 1)

# List to store the distances between drones
distDrone = []

# Safety distance between drones, used to avoid collisions
dsafe = 2

# Maximum Hotizontal angle (in radians)
amax = 75 *np.pi/180  # Convert to radians

# Maximum Vertical angle (in radians) 
bmax = 60 *np.pi/180  # Convert to radians


# List to store the output track points (without start and end points)
Output = []

# List to track potential dangers (like obstacles or unsafe conditions)
danger = []

# List to store the obstacles detected in the environment
obstlist = []

# List to store the data about each drone, including all track points (from start to end)
# The data is stored in 1D arrays, each representing the full path of a drone from start to endpoint
Droneinfo = []

# Lists to store start and endpoint for each drone
startpoint = []
endpoint = []

# Simulated annealing parameters

# Final temperature, used to control the termination of the annealing process
tf = 1  # Final temperature

# Maximum iterations for the simulated annealing process
imax = 100  # Maximum iterations

# Cooling rate for the simulated annealing algorithm
alpha = 0.89  # Cooling rate, controls how fast the temperature decreases

# Initial temperature for the annealing process, higher value allows exploration of solutions
tn = 700  # Higher initial temperature

# Number of new solutions to generate per iteration
nt = 2  # Increase number of new solutions to generate per iteration
