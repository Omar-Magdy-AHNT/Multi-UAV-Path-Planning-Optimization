import numpy as np  # Import numpy module for numerical operations
import math  # Import math module for mathematical functions

# Number of drones in the simulation (can be adjusted based on your system)
numdrones = 4   

# Maximum permissible distance between drones (depends on controller accuracy)
maxpdist = 4 

# Size of the grid (depends on the environment setup)
gridsize = 10 

# Number of track points to be calculated based on grid size and max point distance
# The formula calculates the number of track points based on grid size and max distance
numtrackp = math.ceil((((((gridsize-0)**2)+((gridsize-0)**2)+((gridsize-0)**2))**0.5)/maxpdist) + 1)

# Safe distance between drones or obstacles
dsafe = 2

# Maximum Horizontal angle (in radians)
amax = 75 *np.pi/180  # Convert to radians

# Maximum Vertical angle (in radians) 
bmax = 60 *np.pi/180  # Convert to radians

# Number of generations in the simulation or optimization process
numofgen = 10

# Population Size
numpopu= 10 

pe= 0.2

pm= 0.4

pc= 0.4

penalty_factor=10

def set_GA_params(n_drones, max_dist, safe_dist, gen, populationsize, children, mutants, elite):
    global numdrones, maxpdist, gridsize, dsafe, amax, bmax, numofgen, numpopu, pc, pm, pe
    numdrones = n_drones
    maxpdist = max_dist
    dsafe = safe_dist
    numofgen = gen
    numpopu = populationsize
    pc = children
    pm = mutants
    pe = elite

# Number of children generated in each generation
numchildren = round(numpopu*pc)

# Number of mutants (random variations) generated in each generation
nummutants = round(numpopu*pm)

# Number of elite individuals selected for the next generation (best-performing)
numelite = round(numpopu*pe)

# Number of parents selected for each generation (used in evolutionary algorithms)
numparents = round(numchildren/2)+1

# Output list to store the results of the simulation
Output = []

# List to store obstacle data, if applicable
obstlist = []

# Starting point for the drones (coordinates or other relevant data)
startpoint = []

# Ending point for the drones (coordinates or other relevant data)
endpoint = []

# List to store parent drones (or solutions in optimization)
parents = [[] for _ in range(numparents)]  

# List of children drones (or solutions) created from the parents
children = [[] for _ in range(numchildren)]  # Initialize list of children for each parent

# Fitness list to store the performance score of each individual drone/solution
fitness = []  

# List to store the elite individuals (best-performing drones/solutions)
elites = [[] for _ in range(numelite)]  

# List to store mutants (randomly generated drones/solutions)
mutants = [[] for _ in range(nummutants)]  

# List to store population
population = [[] for _ in range(numpopu)]