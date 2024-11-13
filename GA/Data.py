import random
import numpy
import math
import numpy as np

numdrones = 2   #depends on the number of drones
maxpdist = 5 #depends on the controller accuracy 
gridsize = 10 #depends on the size of the grid
numtrackp = math.ceil((((((gridsize-0)**2)+((gridsize-0)**2)+((gridsize-0)**2))**0.5)/maxpdist) + 1)
dsafe = 2
amax = 75 *numpy.pi/180
bmax = 60 *numpy.pi/180
Output = []
obstlist= []
startpoint = []
endpoint = []
numofgen = 200
numparents = 4
numchildren = 2
nummutants = 4
numelite = 2
parents = []  # Initialize parents list
children = [[] for _ in range(numparents)]  # Initialize children list
fitness = []  # Initialize fitness list
elites = []  # Initialize elite list
mutants = []  # Initialize mutants list
