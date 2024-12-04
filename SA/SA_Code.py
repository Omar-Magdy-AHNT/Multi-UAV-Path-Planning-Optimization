import sys
import os

# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary modules
from SA.SA_Const1 import *  # Import constants related to the simulation
from SA.SA_Const2 import *  # Import additional constants
from SA.SA_Const3 import *  # Import more constants
from SA.SA_Const4 import *  # Import function to validate track point lines
from SA.SA_Param import *  # Import data structures and variables
from SA.SA_ObjFunc1 import *  # Import first objective function
from SA.SA_ObjFunc2 import *  # Import second objective function
import math  # Import math module for mathematical functions
from SA.SA_CreateMap import *  # Import function to create the map
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting toolkit
import numpy as np  # Import numpy for numerical operations
import random  # Import random module
    

def generate_possible_points(x, y, z):
    # Define perturbation ranges
    x_range = range(-5, 6)  # From -5 to 5
    y_range = range(-5, 6)  # From -5 to 5
    z_range = range(-3, 4)  # From -3 to 3

    # Create a list to store all possible (xn, yn, zn) combinations
    possible_points = []

    # Generate all combinations of perturbations
    for dx in x_range:
        for dy in y_range:
            for dz in z_range:
                xn = x + dx
                yn = y + dy
                zn = z + dz
                possible_points.append((xn, yn, zn))

    return possible_points

# Function to calculate the objective value based on distances and dangers
def objective():
    distDrone.clear()  # Clear the distance list
    danger.clear()  # Clear the danger list
    func1()  # Calculate distances (function defined elsewhere)
    func2()  # Calculate dangers (function defined elsewhere)
    total_distance = sum(distDrone)  # Sum up total distances
    total_danger = sum(danger)  # Sum up total dangers
    obj = total_distance + total_danger  # Combine distances and dangers to form objective
    return obj  # Return the objective value

# Function to generate a new solution
def newsolution():
    for i in range(numdrones):  # Iterate over each drone
        flag = False  # Initialize flag to track valid new solutions
        start_idx = (numtrackp) * i  # Calculate start index for the current drone's points
        end_idx = (numtrackp) * (i + 1) -1 # Calculate end index for the current drone's points (exclusive)
        f = random.randint(start_idx, end_idx)  # Randomly select an index for the drone's point
        g = Droneinfo.index(Output[f])  # Get the actual index in the Droneinfo list
        x, y, z = Output[f]  # Get current point's coordinates
        possible_points = generate_possible_points(x, y, z)  # Generate possible points around current point
        while not flag:  # Loop until a valid new point is found
            if not possible_points:  # If no possible points left
                print("No possible points left SA, skipping.")
                xn,yn,zn = Output[f]  # Keep the current point
                break  # Break out of the loop
            xn, yn, zn = random.choice(possible_points)  # Randomly select a new point from possible points
            
            # Check if new point is within bounds
            if xn < 0 or xn > gridsize or yn < 0 or yn > gridsize or zn < 0 or zn > gridsize:
                print("Point is out of bounds SA, skipping.")  # Debugging statement for out of bounds
                possible_points.remove((xn, yn, zn))  # Remove the invalid point
                continue  # Skip this iteration
            
            # Check if the generated point is in the obstacle list
            if (xn, yn, zn) in obstlist:
                print("Point is an obstacle SA, skipping.")  # Debugging statement for obstacle
                possible_points.remove((xn, yn, zn))  # Remove the invalid point
                continue  # Skip this iteration
            
            # Check if the generated point is already in Droneinfo
            if (xn, yn, zn) in Droneinfo:
                print("Point is already in Droneinfo SA, skipping.")  # Debugging statement for duplicates
                possible_points.remove((xn, yn, zn))  # Remove the invalid point
                continue  # Skip this iteration

            # Check for horizontal constraints if applicable
            if not Horz_check(Droneinfo[g - 1], (xn, yn, zn)) and not Horz_check((xn, yn, zn),Droneinfo[g + 1]):
                print("Horizontal check failed SA, skipping.")  # Debugging statement for horizontal check failure
                possible_points.remove((xn, yn, zn))  # Remove the invalid point
                continue  # Skip this iteration

            # Check for vertical constraints if applicable
            if g > (1 + (numtrackp + 2) * i) :
                if not vertical_check(Droneinfo[g - 2], Droneinfo[g - 1], (xn, yn, zn)) and not vertical_check(Droneinfo[g - 1], (xn, yn, zn), Droneinfo[g + 1]):
                    print("Vertical check failed SA, skipping.")  # Debugging statement for vertical check failure
                    possible_points.remove((xn, yn, zn))  # Remove the invalid point
                    continue  # Skip this iteration
                if g < (numtrackp + 2) * (i + 1) - 2:
                    if not vertical_check((xn, yn, zn), Droneinfo[g + 1], Droneinfo[g + 2]):
                        print("Vertical check failed SA, skipping.")
                        possible_points.remove((xn, yn, zn))  # Remove the invalid point
                        continue # Skip this iteration

            if not Trackpointlinevalid(Droneinfo[g - 1], (xn, yn, zn)) and not Trackpointlinevalid((xn, yn, zn), Droneinfo[g + 1]):
                print("Line check failed SA, skipping.")  # Debugging statement for line check failure
                possible_points.remove((xn, yn, zn))  # Remove the invalid point
                continue  # Skip this iteration
            
            
            flag = True  # Mark that a valid point has been found
        
        Output[f] = (xn, yn, zn)  # Update the Output with the new point
        Droneinfo[g] = (xn, yn, zn)  # Update the Droneinfo with the new point



cost = []  # Initialize a list to store cost values

# Function to perform simulated annealing
def SimulatedAnnealing():
    # Define global variables to be used in the function
    global tf
    global tn
    global imax
    global alpha
    
    current_solution = Output.copy()  # Work with a copy of the initial solution
    best_solution = current_solution.copy()  # Initialize the best solution
    current_objective = objective()  # Calculate initial objective
    best_objective = current_objective  # Initialize best objective
    i = 0  # Initialize iteration counter

    while tn > tf and i < imax:  # Loop until temperature is low enough or max iterations reached

        for j in range(nt):  # Generate new solutions
            newsolution()  # Generate a new solution
            new_objective = objective()  # Calculate the new objective
            delta = new_objective - current_objective  # Determine the change in objective

            # If the new solution is better
            if delta < 0:
                current_solution = Output.copy()  # Update current solution
                current_objective = new_objective  # Update current objective
                # Update the best solution if necessary
                if new_objective < best_objective:
                    best_solution = Output.copy()  # Update the best solution
                    best_objective = new_objective  # Update the best objective
            # If the new solution is worse, accept it with a higher probability
            elif random.random() < math.exp(-delta / tn):
                current_solution = Output.copy()  # Update current solution
                current_objective = new_objective  # Update current objective

        # Cool down the temperature
        tn = tn * alpha  # Simplified cooling schedule

        # Print current best solution and its objective
        print('Iteration:', i + 1)  # Print current iteration
        print('Temperature:', tn)  # Print current temperature

        i += 1  # Increment iteration counter
        cost.append(best_objective)  # Store the best objective for this iteration
    # Return the best solution and its objective after all iterations
    return best_solution, best_objective


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
    createobs(gridsize)  # Create obstacles in the grid
    createmap()  # Create the initial map with obstacles and drone info
    bs , bo = SimulatedAnnealing()  # Execute the simulated annealing algorithm
    Output = bs  # Update the Output with the best solution found
    Droneinfo = []  # Reset Droneinfo list
    for i in range(numdrones):  # Iterate over each drone
        startpt = startpoint[i]  # Get the start point for the current drone
        endpt = endpoint[i]  # Get the end point for the current drone
        Droneinfo.append(startpt)  # Add the start point to Droneinfo
        for j in range(numtrackp):  # Iterate over each track point
            Droneinfo.append(Output[j +(numtrackp*i)])  # Add the current track point to Droneinfo
        Droneinfo.append(endpt)  # Add the end point to Droneinfo
    return Droneinfo, bo

# Only run the following code when this file is executed directly
if __name__ == "__main__":
    Droneinfo,BestObjective = run()
    print(Droneinfo)
    plt.plot(cost)  # Plot the cost history over iterations
    plot_map(Droneinfo, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles
