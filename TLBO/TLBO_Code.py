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


def plot_map(Droneinfo, obstlist, numdrones, numtrackp, gridsize):
    fig = plt.figure()  # Create a new figure
    ax = fig.add_subplot(111, projection='3d')  # Add a 3D subplot

    # Define a list of colors for each drone
    colors = plt.cm.jet(np.linspace(0, 1, numdrones))  # Generate a color map for drones

    # Plot each drone's path in a different color
    for i in range(numdrones):  # Iterate over each drone
        start_index = (numtrackp + 2) * i  # Calculate start index for the current drone's path
        end_index = start_index + (numtrackp + 2)  # Calculate end index for the current drone's path

        # Get the track points for this drone from Droneinfo
        drone_path = Droneinfo[start_index:end_index]  # Extract path points for the current drone
        xs, ys, zs = zip(*drone_path)  # Unpack into separate lists for x, y, z

        ax.plot(xs, ys, zs, color=colors[i], label=f'Drone {i + 1}', marker='o')  # Plot the drone path

    # Plot obstacles
    if obstlist:  # Check if there are obstacles to plot
        ox, oy, oz = zip(*obstlist)  # Unpack obstacle coordinates
        ax.scatter(ox, oy, oz, color='red', marker='x', label='Obstacles')  # Scatter plot for obstacles

    # Set axis limits based on grid size
    ax.set_xlim([0, gridsize])  # Set x-axis limits
    ax.set_ylim([0, gridsize])  # Set y-axis limits
    ax.set_zlim([0, gridsize])  # Set z-axis limits

    # Set labels and title
    ax.set_xlabel('X')  # Set x-axis label
    ax.set_ylabel('Y')  # Set y-axis label
    ax.set_zlabel('Z')  # Set z-axis label
    ax.set_title('Drone Paths with Obstacles')  # Set plot title

    plt.legend()  # Display the legend
    plt.show()  # Show the plot
    
def run():
    createobs(gridsize)  # Create obstacles in the simulation grid
    createmap()  # Create the map for drones, including start and end points


    return Output, bestobjective

# Only run the following code when this file is executed directly
if __name__ == "__main__":
    Output, bestobjective = run()  # Run the ant colony algorithm
    plt.plot(cost)  # Plot the cost history over iterations
    plot_map(Output, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles