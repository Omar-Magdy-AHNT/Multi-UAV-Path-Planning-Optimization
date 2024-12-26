import sys
import os
from memory_profiler import profile
import gc
import math

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
from PSO.PSO_ObjFunc3 import *
import matplotlib.pyplot as plt
import numpy as np

def GFittness():
    global Global_Fitness,Personal_Fitness,global_path
    Global_Fitness = min(Personal_Fitness)
    global_path = Birds[Personal_Fitness.index(Global_Fitness)].copy()

def fits(i):
    # Calculate x and y values for the i-th child using func1 and func2
    x = func1(Birds[i])  # This function returns distance values for the i-th child
    y = func2(Birds[i])  # This function returns danger values for the i-th child
    z = func3(Birds[i])
    total_dist = sum(x)
    total_danger = sum(y)
    total_penalty = sum(z)
    # Append the sum of total distance and total danger to the fitness list
    fit = total_dist + total_danger + total_penalty
    return fit

def PFittness():
    global Personal_Fitness
    for i in range(numparticles):
        fit = fits(i)
        if Personal_Fitness[i] == 0:
            Personal_Fitness[i] = fit
            personal_path[i] = Birds[i].copy()
        elif fit < Personal_Fitness[i]:
            Personal_Fitness[i] = fit
            personal_path[i] = Birds[i].copy()

def check(point,ai,i):
    x = point[0]
    y = point[1]
    z = point[2]
    A = Birds[ai]
    # Check if the point is within the valid grid size
    if x < 0 or x > gridsize or y < 0 or y > gridsize or z < 0 or z > gridsize:
        #print("Point is out of bounds PSO, skipping.")  # Debugging statement for out of bounds 
        return True  # Return True to indicate this point is invalid (out of bounds)
    
    if not PointValid(point, A):
        #print("Point is already exists PSO, skipping.")  # Debugging statement for duplicates
        return True  # Return True to indicate this point is invalid (duplicate)

    if not Horz_check(A[i - 1], point):
        #print("Horizontal check failed PSO, skipping.")  # Debugging statement for horizontal check failure
        return True  # Return True if horizontal check fails

    # Check if the point lies on a valid line from the previous points
    if not Trackpointlinevalid(A[i - 1], point, A, i): 
        #print("Line check failed PSO, skipping.")  # Debugging statement for line check failure
        return True  # Return True if line check fails
    
    if i > 1:
        if not vertical_check(A[i - 2], A[i - 1], point):
            #print("Vertical check failed PSO, skipping.")
            return True  # Return True if vertical check fails
    
    if i == numtrackp or i == (len(A) - 2):
        # Check if the vertical relationship between the last point and the next one is valid
        if not vertical_check(A[i - 1], point, A[-1]):
            #print("Vertical check failed PSO, skipping.")
            return True  # Return True if vertical check fails
        
        # Check if the line between the current point and the last point is valid
        if not Trackpointlinevalid(point, A[-1], A, i):
            #print("Line check failed PSO, skipping.")  # Debugging statement for line check failure
            return True  # Return True if line check fails
        
        # Check if the horizontal relationship between the current point and the last point is valid
        if not Horz_check(point, A[-1]):
            #print("Horizontal check failed PSO, skipping.")  # Debugging statement for horizontal check failure
            return True  # Return True if horizontal check fails
    
    # If all checks pass, return False indicating the point is valid
    return False


def calculate_vx_vy_vz( Velocity, personal_path, Birds, global_path, num_points):
    # Create 20 equally spaced values between 0 and 1 for r1 and r2
    r1_values = np.linspace(0, 1, num_points)
    r2_values = np.linspace(0, 1, num_points)
    
    # List to store the results
    results = []
    
    # Iterate over all combinations of r1 and r2
    for r1 in r1_values:
        for r2 in r2_values:
            # Calculate vx, vy, vz for the current r1, r2 combination
            vx =(wx * Velocity[0] + cx1 * r1 * (personal_path[0] - Birds[0]) + cx2 * r2 * (global_path[0] - Birds[0]))
            vy = (wy * Velocity[1] + cy1 * r1 * (personal_path[1] - Birds[1]) + cy2 * r2 * (global_path[1] - Birds[1]))
            vz = (wz * Velocity[2] + cz1 * r1 * (personal_path[2] - Birds[2]) + cz2 * r2 * (global_path[2] - Birds[2]))
            
            # Append the result to the list
            results.append((math.ceil(vx),math.ceil(vy), math.ceil(vz)))
            results.append((int(vx),int(vy), int(vz)))
    
    return results

def newsol():
    for i in range(numparticles):
        for k in range(numdrones):
            start_idx = (k) * (numtrackp + 2) + 1
            end_idx = (k + 1) * (numtrackp + 2)
            for j in range(start_idx, end_idx - 1):
                vel = calculate_vx_vy_vz(Velocity[i], personal_path[i][j], Birds[i][j], global_path[j], 20)
                for v in vel:
                    vx, vy, vz = v
                    px = Birds[i][j][0] + vx
                    py = Birds[i][j][1] + vy
                    pz = Birds[i][j][2] + vz
                    Pu = (px, py, pz)
                    if not check(Pu, i, j):
                        Birds[i][j] = Pu
                        Velocity[i] = (vx, vy, vz)
                        break

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

    # Evaluate initial fitness
    PFittness()
    GFittness()
    cost.append(Global_Fitness)
    print("Best fitness value: ", Global_Fitness)  # Print the best fitness value of the current generation
    print("Best Bird: ", global_path)  # Print the best individual of the current generation

    # Initialize the cost plot
    plt.figure("Cost Minimization Curve")  # Name the figure for clarity
    plt.ion()  # Enable interactive mode
    cost_line, = plt.plot(cost, marker='o', label='Cost Curve', color='blue')  # Initialize the plot line
    plt.title('Minimization Curve')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.legend()

    # Main loop for each iteration
    for i in range(maxiter):
        print("Iteration: ", i)

        # Generate a new solution
        newsol()

        # Evaluate fitness
        PFittness()
        GFittness()
        print("Best fitness value: ", Global_Fitness)  # Print the best fitness value of the current generation
        print("Best Bird: ", global_path)  # Print the best individual of the current generation

        # Append the current global fitness value to the cost list
        cost.append(Global_Fitness)

        # Update the cost plot dynamically
        cost_line.set_ydata(cost)  # Update y-data
        cost_line.set_xdata(range(len(cost)))  # Update x-data
        plt.xlim(0, len(cost))  # Adjust x-axis limits dynamically
        plt.ylim(min(cost) - 1, max(cost) + 1)  # Adjust y-axis limits dynamically
        plt.pause(0.1)  # Pause for a brief moment to refresh the plot

    # Finalize the best solution
    BestBird = global_path.copy()

    # Finalize and keep the cost plot open
    plt.ioff()

    plot_map(BestBird, obstlist, numdrones, numtrackp, gridsize)  # Call plot_map with the required arguments

    # Keep both figures open
    plt.show(block=True)


if __name__ == "__main__":
    run()  # Run the PSO algorithm 