import random
import numpy
import math
import numpy as np

numdrones = 2   #depends on the number of drones
maxpdist = 2 #depends on the controller accuracy 
gridsize = 10
numtrackp = math.ceil((((((gridsize-0)**2)+((gridsize-0)**2)+((gridsize-0)**2))**0.5)/maxpdist) + 1)*2
distDrone = []
dsafe = 1
amax = 75 *numpy.pi/180
bmax = 60 *numpy.pi/180
Output = []
danger = []
obstlist= []
Droneinfo = []