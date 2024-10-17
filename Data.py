import random
import numpy
import math

numdrones = 2   #depends on the number of drones
distbttrackp = 2 #depends on the controller accuracy 
gridsize = 100
numtrackp = math.ceil((((((10-0)**2)+((10-0)**2)+((10-0)**2))**0.5)/distbttrackp) + 1)
obstlist = []
createobs()
distDrone = []
dsafe = 1
amax = 75 *numpy.pi/180
bmax = 60 *numpy.pi/180
Output = []
danger = []


def createobs():

    base_points = [(5, 5), (15, 15), (25, 25)] 


    for base_x, base_y in base_points:
        for x_offset in range(5): 
            for y_offset in range(5):
                for z in range(gridsize): 
                    x = base_x + x_offset
                    y = base_y + y_offset
                    obstlist.append((x, y, z))


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
