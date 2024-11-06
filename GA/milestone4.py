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



def elite():
    for i in range(numparents):
        fit = []
        f =func1(i,Droneinfo) + func2(i,Droneinfo)
        fit.append(f)
    for i in range(len(fit)):
        if fit[i] == min(fit):
            elite.append(Droneinfo[i])

def crossover():
    for i in range(len(children)+len(mutants)+len(elite)):
        f = func1(i,Droneinfo) + func2(i,Droneinfo)