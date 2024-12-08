import sys
import os

# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import necessary modules
from TLBO.TLBO_Const1 import *  # Import constants related to the simulation
from TLBO.TLBO_Const2 import *  # Import additional constants
from TLBO.TLBO_Const3 import *  # Import more constants
from TLBO.TLBO_Const4 import Trackpointlinevalid  # Import function to validate track point lines
from TLBO.TLBO_Const5 import *  # Import function to check distance constraint
from TLBO.TLBO_Param import *  # Import data structures and variables
from TLBO.TLBO_ObjFunc1 import *  # Import first objective function
from TLBO.TLBO_ObjFunc2 import *  # Import second objective function
from TLBO.TLBO_ObjFunc3 import *  # Import second objective function
from TLBO.TLBO_CreateMap import *  # Import function to create the map
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting toolkit
import numpy as np  # Import numpy for numerical operations
import itertools  # Import itertools for generating combinations
import copy  # Import the copy module


# Only run the following code when this file is executed directly
if __name__ == "__main__":
    Output, bestobjective = run()  # Run the ant colony algorithm
    plt.plot(cost)  # Plot the cost history over iterations
    plot_map(Output, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles