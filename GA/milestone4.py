from Const1 import *  # Import constants related to the simulation
from Const2 import *  # Import additional constants
from Const3 import *  # Import more constants
from Const4 import Trackpointlinevalid  # Import function to validate track point lines
from Const5 import *  # Import remaining constants
from Data import *  # Import data structures and variables
from OF1 import *  # Import first objective function
from OF2 import *  # Import second objective function
import math  # Import math module for mathematical functions
from creatmap import *  # Import function to create the map
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting toolkit
import numpy as np  # Import numpy for numerical operations

def newgen():
    elite()
    crossover()
    mutation()

def elite():
    elites = []
    for i in range(numelite):
        fittest()
        i = fitness.index(min(fitness))
        elites = children[i]
        del children[i]
        del fitness[i]

def crossover():
    parents = elites
    for i in range(numparents - numelite):
        i = fitness.index(min(fitness))
        parents.append(children[i])
        del children[i]
        del fitness[i]
    children = []
    for i in range(numchildren//2):
        child1 = []
        child2 = []
        for j in range(numdrones):
            for k in range(numtrackp+2):
                f1 = True
                f2 = True
                if k == 0:
                    children[i][k] = startpoint[j]
                    continue
                if k == numtrackp+1:
                    children[i][k] = endpoint[j]
                    continue
                while f1:
                    alpha = random.uniform(0.2,0.9)
                    x1 = (alpha*parents[0][k]) - (1-alpha)*parents[i+1][k]
                    y1 = (alpha*parents[0][k]) - (1-alpha)*parents[i+1][k]
                    z1 = (alpha*parents[0][k]) - (1-alpha)*parents[i+1][k]
                    c1 = (x1,y1,z1)
                    f1 = check(c1,child1)
                    if f1 == False:
                        child1.append((x1,y1,z1))

                while f2:
                    x2 = (alpha*parents[i+1][k])- (1-alpha)*parents[0][k]
                    y2 = (alpha*parents[i+1][k])- (1-alpha)*parents[0][k]
                    z2 = (alpha*parents[i+1][k])- (1-alpha)*parents[0][k]
                    c2 = (x2,y2,z2)
                    f2 = check(c2,child2)
                    if f2 == False:
                        child2.append((x2,y2,z2))

        children.append(child1)
        children.append(child2)
    if numchildren % 2 == 1:
        fittest()
        if fitness[-1] > fitness[-2]:
            del children[-1]
        else: 
            del children[-2]
def fittest():
    fitness = []
    z= []
    for i in range(numchildren):
        x = func1(i,children) 
        y = func2(i,children)
        for j in range(numdrones):
            z[j] = x[j] + y[j]
        fitness.append(z)

def mutation():
    for i in range(nummutants):
        fittest()
        i = fitness.index(max(fitness))
        mutants = children[i]
        del children[i]
        del fitness[i]
        for j in range(numdrones):
            for k in range(numtrackp+2):
                if k == 0:
                    children[i][k] = startpoint[j]
                    continue
                if k == numtrackp+1:
                    children[i][k] = endpoint[j]
                    continue
                x1 = mutants[k] + random.uniform(-1,1)
                y1 = mutants[k] + random.uniform(-1,1)
                z1 = mutants[k] + random.uniform(-1,1)
                if check((x1,y1,z1),children[i]) == False:
                    children[i][k] = (x1,y1,z1)
    for i in range(nummutants):
        children.extend(mutants)

def check(p1,a1):
    #takes 2 points and checks them
createmap()