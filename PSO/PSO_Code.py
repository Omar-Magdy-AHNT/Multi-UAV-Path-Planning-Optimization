import sys
import os

# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PSO.PSO_Param import *
from PSO.PSO_CreateMap import *
from PSO.PSO_Const1 import *
from PSO.PSO_Const2 import *
from PSO.PSO_Const3 import *
from PSO.PSO_Const4 import *
from PSO.PSO_ObjFunc1 import *
from PSO.PSO_ObjFunc2 import *
import matplotlib.pyplot as plt
import numpy as np

def GFittness():
    global Global_Fitness,Personal_Fitness
    Global_Fitness = min(Personal_Fitness)


def fits(i):
    # Calculate x and y values for the i-th child using func1 and func2
    x = func1(i, Birds)  # This function returns distance values for the i-th child
    y = func2(i, Birds)  # This function returns danger values for the i-th child

    # Calculate the total distance by summing the x values
    total_dist = sum(x)

    # Calculate the total danger by summing the y values
    total_danger = sum(y)

    # Append the sum of total distance and total danger to the fitness list
    fit = total_dist + total_danger
    return fit

def PFittness():
    global Personal_Fitness
    for i in range(numparticles):
        fit = fits(i)
        if Personal_Fitness[i] == 0:
            Personal_Fitness[i] = fit
        elif fit < Personal_Fitness[i]:
            Personal_Fitness[i] = fit

def check(point,ai,i):
    x = point[0]
    y = point[1]
    z = point[2]
    A = Birds[ai]
    # Check if the point is within the valid grid size
    if x < 0 or x > gridsize or y < 0 or y > gridsize or z < 0 or z > gridsize:
        #print("Point is out of bounds GA, skipping.")  # Debugging statement for out of bounds 
        return True  # Return True to indicate this point is invalid (out of bounds)
    
    if not PointValid(point, A, i):
        #print("Point is already exists GA, skipping.")  # Debugging statement for duplicates
        return True  # Return True to indicate this point is invalid (duplicate)
    
    if not Horz_check(A[i - 1], point):
        #print("Horizontal check failed GA, skipping.")  # Debugging statement for horizontal check failure
        return True  # Return True if horizontal check fails

    # Check if the point lies on a valid line from the previous points
    if not Trackpointlinevalid(A[i - 1], point, A, i): 
        #print("Line check failed GA, skipping.")  # Debugging statement for line check failure
        return True  # Return True if line check fails
    
    if i > 1:
        if not vertical_check(A[i - 2], A[i - 1], point):
            #print("Vertical check failed GA, skipping.")
            return True  # Return True if vertical check fails
    
    if i == numtrackp or i == (len(A) - 2):
        # Check if the vertical relationship between the last point and the next one is valid
        if not vertical_check(A[i - 1], point, A[-1]):
            #print("Vertical check failed GA, skipping.")
            return True  # Return True if vertical check fails
        
        # Check if the line between the current point and the last point is valid
        if not Trackpointlinevalid(point, A[-1], A, i):
            #print("Line check failed GA, skipping.")  # Debugging statement for line check failure
            return True  # Return True if line check fails
        
        # Check if the horizontal relationship between the current point and the last point is valid
        if not Horz_check(point, A[-1]):
            #print("Horizontal check failed GA, skipping.")  # Debugging statement for horizontal check failure
            return True  # Return True if horizontal check fails
    
    # If all checks pass, return False indicating the point is valid
    return False


def newsol():
    for i in range(numparticles):
        r1 = np.random.uniform(0, 1)  
        r2 = np.random.uniform(0, 1)
        B = fits(i)
        Velocity[i] = w * Velocity[i] +c1 *r1 * (Personal_Fitness[i] - B ) + c2 * r2 * (Global_Fitness - B)
        for k in range(numdrones):
            # Calculate the start and end index for the current drone's path
            start_idx = k * (numtrackp + 2)  # Start index for current drone
            end_idx = (k + 1) * (numtrackp + 2)  # End index for current drone (inclusive of the last point)
            # Now, calculate the distance over the entire path for this drone
            for j in range(start_idx, end_idx - 1):  # Avoid out-of-bounds by stopping before the last point

                px= Birds[i][j][0] + Velocity[i]
                py= Birds[i][j][1] + Velocity[i]
                pz= Birds[i][j][2] + Velocity[i]
                Pu = (round(px), round(py), round(pz))
                Pd = (int(px), int(py), int(pz))

                if not check(Pu,i,j+1):
                    Birds[i][j] = Pu
                elif not check(Pd,i,j+1):
                    Birds[i][j] = Pd



# Function to plot the drone paths and obstacles in 3D
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
    global cost
    createobs(gridsize)
    createmap()
    for i in range(maxiter):
        PFittness()
        GFittness()
        newsol()
        cost.append(Global_Fitness)
        BestBird = Birds[Personal_Fitness.index(Global_Fitness)].copy()
    return BestBird, Global_Fitness

# Only run the following code when this file is executed directly
if __name__ == "__main__":
    Output, bestobjective = run()  # Run the ant colony algorithm
    plt.plot(cost)  # Plot the cost history over iterations
    plot_map(Output, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles