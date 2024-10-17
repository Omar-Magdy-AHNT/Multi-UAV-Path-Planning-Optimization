import random
import numpy

numdrones = 2   #depends on the number of drones
distbttrackp = 2 #depends on the controller accuracy 
gridsize = 10
numtrackp = (((((10-0)**2)+((10-0)**2)+((10-0)**2))**0.5)/distbttrackp) + 1
obstnum = random.randint(0, 8)
obstlist = []
distDrone = []
dsafe = 1
amax = 75 *numpy.pi/180
bmax = 60 *numpy.pi/180
Output = []
danger = []

def createobs():
    for i in range(obstnum): 
        x = random.randint(0, gridsize)
        y = random.randint(0, gridsize) 
        z = random.randint(0, gridsize)
        obstlist.append((x,y,z))

def createarray():
    matrix = []
    for i in range(numdrones):
        startpt=(0,i,0)
        endpt=(10,10-i,10)
        matrix.append(startpt)
        for j in range(numtrackp):
            x = random.randint(0, gridsize)
            y = random.randint(0, gridsize)
            z = random.randint(0, gridsize)
            matrix.append((x,y,z))
            Output.append((x,y,z))
        matrix.append(endpt)
    return matrix

Droneinfo = createarray()
createobs()
