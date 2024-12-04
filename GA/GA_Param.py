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

# Number of generations in the simulation or optimization process
numofgen = 100

# Number of parents selected for each generation (used in evolutionary algorithms)
numparents = 4

# Number of children generated in each generation
numchildren = 2

# Number of mutants (random variations) generated in each generation
nummutants = 4

# Number of elite individuals selected for the next generation (best-performing)
numelite = 1

def set_GA_params(n_drones, max_dist, safe_dist, gen, parents, children, mutants, elite):
    global numdrones, maxpdist, gridsize, dsafe, amax, bmax, numofgen, numparents, numchildren, nummutants, numelite
    numdrones = n_drones
    maxpdist = max_dist
    dsafe = safe_dist
    numofgen = gen
    numparents = parents
    numchildren = children
    nummutants = mutants
    numelite = elite

# Output list to store the results of the simulation
Output = []

# List to store obstacle data, if applicable
obstlist = []

# Starting point for the drones (coordinates or other relevant data)
startpoint = []

# Ending point for the drones (coordinates or other relevant data)
endpoint = []

# List to store parent drones (or solutions in optimization)
parents = []  

# List of children drones (or solutions) created from the parents
children = [[] for _ in range(numchildren+nummutants)]  # Initialize list of children for each parent

# Fitness list to store the performance score of each individual drone/solution
fitness = []  

# List to store the elite individuals (best-performing drones/solutions)
elites = []  

# List to store mutants (randomly generated drones/solutions)
mutants = []  

#cost list to store the best fitness value of each generation
cost=[] 