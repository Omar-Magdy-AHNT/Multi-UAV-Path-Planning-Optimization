import random
import numpy
import math
import numpy as np

numdrones = 2   #depends on the number of drones
maxpdist = 3 #depends on the controller accuracy 
gridsize = 10 #depends on the size of the grid
numtrackp = math.ceil((((((gridsize-0)**2)+((gridsize-0)**2)+((gridsize-0)**2))**0.5)/maxpdist) + 1)
dsafe = 2
amax = 75 *numpy.pi/180
bmax = 60 *numpy.pi/180
Output = []
obstlist= []
startpoint = []
endpoint = []
#pe = 0.16 
#pm = 0.33
#pc = 0.5 
#total number of chromosomes = 6
numparents = 3
numchildren = 3
nummutants = 2
numelite = 1
parents = []  # Initialize parents list
children = []  # Initialize children list
fitness = []  # Initialize fitness list
elites = []  # Initialize elite list
mutants = []  # Initialize mutants list
