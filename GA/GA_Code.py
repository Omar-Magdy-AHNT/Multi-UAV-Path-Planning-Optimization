import sys
import os

# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary modules
from GA.GA_Const1 import *  # Import constants related to the simulation
from GA.GA_Const2 import *  # Import additional constants
from GA.GA_Const3 import *  # Import more constants
from GA.GA_Const4 import Trackpointlinevalid  # Import function to validate track point lines
from GA.GA_Const5 import *  # Import remaining constants
from GA.GA_Param import *  # Import data structures and variables
from GA.GA_ObjFunc1 import *  # Import first objective function
from GA.GA_ObjFunc2 import *  # Import second objective function
from GA.GA_CreateMap import *  # Import function to create the map
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting toolkit
import numpy as np  # Import numpy for numerical operations
import itertools  # Import itertools for generating combinations
import copy  # Import the copy module



# Main function to generate a new generation in the genetic algorithm
def newgen():
    elite()  # Select elite individuals
    mutation()  # Apply mutation to the population
    crossover()  # Apply crossover to the population


# Select the elite individuals from the current population
def elite():
    global elites
    elites.clear()  # Clear the elites list
    fittest()  # Find the fittest individuals
    for i in range(numelite):
        z = fitness.index(min(fitness))  # Get the index of the fittest individual
        elites.append(copy.deepcopy(children[z]))  # Add the fittest individual to elites
        del children[z]  # Remove it from the children list
        del fitness[z]  # Remove its fitness value


# Function to generate alpha combinations for crossover
def generate_alpha_combinations(parents, i, k, alpha_values, intg):
    combinations = []  # Initialize an empty list to store the generated combinations

    if intg == 1:  # First case for generating alpha combinations (based on parents[0] and parents[i+1])
        for alpha in alpha_values:  # Iterate through each alpha value in the provided range
            # Compute the new coordinates using alpha and the corresponding values from parents
            x1 = (alpha * parents[0][k][0]) - (1 - alpha) * parents[i + 1][k][0]
            y1 = (alpha * parents[0][k][1]) - (1 - alpha) * parents[i + 1][k][1]
            z1 = (alpha * parents[0][k][2]) - (1 - alpha) * parents[i + 1][k][2]
            
            # Round the resulting coordinates to integers and append to combinations list
            x, y, z = int(round(x1)), int(round(y1)), int(round(z1))
            c1 = (x, y, z)  # Create a tuple with the rounded values
            combinations.append(c1)  # Append the combination to the list
            
            # Repeat the same but without rounding to integers, directly adding to the list
            x, y, z = int(x1), int(y1), int(z1)
            c1 = (x, y, z)
            combinations.append(c1)  # Append the second version of the combination

    else:  # Second case for generating alpha combinations (based on parents[i+1] and parents[0])
        for alpha in alpha_values:  # Iterate through each alpha value in the provided range
            # Compute the new coordinates using alpha and the corresponding values from parents
            x2 = (alpha * parents[i + 1][k][0]) - (1 - alpha) * parents[0][k][0]
            y2 = (alpha * parents[i + 1][k][1]) - (1 - alpha) * parents[0][k][1]
            z2 = (alpha * parents[i + 1][k][2]) - (1 - alpha) * parents[0][k][2]
            
            # Round the resulting coordinates to integers and append to combinations list
            x, y, z = int(round(x2)), int(round(y2)), int(round(z2))
            c2 = (x, y, z)  # Create a tuple with the rounded values
            combinations.append(c2)  # Append the combination to the list
            
            # Repeat the same but without rounding to integers, directly adding to the list
            x, y, z = int(x2), int(y2), int(z2)
            c1 = (x, y, z)
            combinations.append(c1)  # Append the second version of the combination

    return combinations  # Return the list of generated combinations




# Function to perform crossover between elite and non-elite individuals to generate new children
def crossover():
    # Append elite individuals to parents list
    for i in range(numelite):
        parents.append(copy.deepcopy(elites[i]))  # Copy each elite individual to parents

    # Append non-elite individuals (based on fitness) to parents list
    for il in range(numparents - numelite):
        h = fitness.index(min(fitness))  # Find the index of the individual with the minimum fitness
        parents.append(children[h])  # Append the corresponding child to parents list

    # Clear previous fitness and children lists for the next generation
    fitness.clear()
    children.clear()

    # Generate new children by performing crossover on parents
    for i in range(round(numchildren/2)):  # Iterate for half the number of children
        child1 = []  # Initialize first child
        child2 = []  # Initialize second child

        for j in range(numdrones):  # Iterate over the number of drones
            for k in range(numtrackp + 2):  # Iterate over the track points plus start/end points
                f1 = True  # Flag for checking the first child
                f2 = True  # Flag for checking the second child

                # Start point handling
                if k == 0:
                    child1.append(startpoint[j])
                    child2.append(startpoint[j])
                    continue  # Skip the start point since it's always the same

                # End point handling
                if k == numtrackp + 1:
                    child1.append(endpoint[j])
                    child2.append(endpoint[j])  
                    continue  # Skip the end point since it's always the same

                # Generate an array of alpha values for interpolation
                alpha_values = np.linspace(0.1, 0.7, num=20)  # Adjust the number of alpha values as needed
                
                # Generate alpha combinations for the first child
                combine = generate_alpha_combinations(parents, i, k, alpha_values, 1)
                for c in range(len(combine)):
                    zz = sorted(combine, reverse=True)  # Sort combinations in descending order
                    c1 = zz[c]  # Select the c-th combination
                    f1 = check(c1, child1, (len(child1) - 1))  # Check if the combination is valid for the first child
                    if not f1:  # If not valid, add it to child1 and break
                        child1.append(c1)
                        break
                    if f1 and c == len(combine) - 1:  # If no valid combination found, fallback to the parent value
                        child1.append(parents[0][k + (numtrackp + 2) * j])

                # Generate alpha combinations for the second child
                combine = generate_alpha_combinations(parents, i, k, alpha_values, 2)
                for v in range(len(combine)):
                    zy = sorted(combine, reverse=True)  # Sort combinations in descending order
                    c2 = zy[v]  # Select the v-th combination
                    f2 = check(c2, child2, (len(child2) - 1))  # Check if the combination is valid for the second child
                    if not f2:  # If not valid, add it to child2 and break
                        child2.append(c2)
                        break
                    if f2 and v == len(combine) - 1:  # If no valid combination found, fallback to the parent value
                        child2.append(parents[i][k + (numtrackp + 2) * j])

        # Append the generated children to the children list
        children.append(child1)
        children.append(child2)

    # If the number of children is odd, discard the worst child based on fitness
    if numchildren % 2 == 1:
        fittest()  # Update fitness values
        if fitness[-1] > fitness[-2]:  # Compare the last two fitness values
            del children[-1]  # Discard the last child if it has worse fitness
        else: 
            del children[-2]  # Otherwise, discard the second last child

    # Add mutants and elite individuals to the children list
    for p in range(nummutants):
        children.append(copy.deepcopy(mutants[p]))  # Append each mutant to the children list

    for l in range(numelite):
        children.append(copy.deepcopy(elites[l]))  # Append each elite individual to the children list



# Function to calculate and update the fitness of all children
def fittest():
    # Clear previous fitness values
    fitness.clear()

    # Iterate over each child in the children list
    for i in range(len(children)):
        # Calculate x and y values for the i-th child using func1 and func2
        x = func1(i, children)  # This function returns distance values for the i-th child
        y = func2(i, children)  # This function returns danger values for the i-th child

        # Calculate the total distance by summing the x values
        total_dist = sum(x)

        # Calculate the total danger by summing the y values
        total_danger = sum(y)

        # Append the sum of total distance and total danger to the fitness list
        fitness.append(total_dist + total_danger)

import itertools

# Function to generate all combinations of (x, y, z) by applying offsets
def generate_combinations(original_xyz, offsets):
    # Unpack the original x, y, z coordinates from the input tuple
    original_x, original_y, original_z = original_xyz

    # Generate all combinations of x, y, and z by adding each offset to the original values
    combinations = [
        (original_x + dx, original_y + dy, original_z + dz)  # Apply offsets to original coordinates
        for dx, dy, dz in itertools.product(offsets, repeat=3)  # itertools.product generates all combinations of offsets
    ]

    # Return the list of generated combinations
    return combinations


def mutation():
    # Accessing the global mutants list to store mutated solutions
    global mutants

    # Clear any previous mutant solutions from the list
    mutants.clear()

    # Ensure the number of mutants is at least `nummutants`, if not, append elites to fill the gap
    if len(children) < nummutants:
        k = abs(len(children) - nummutants)
        for u in range(k):
            children.append(copy.deepcopy(elites[u]))  # Add elite solutions to the children list

    # Find the fittest solutions by evaluating the fitness of children
    fittest()

    # Sort the fitness list in descending order
    vix = sorted(fitness, reverse=True)

    # Select the top `nummutants` children based on their fitness
    for f in range(nummutants):     
        # Find the index of the fittest solution
        i = fitness.index(vix[f])

        # Append the fittest solutions to the mutants list
        mutants.append(copy.deepcopy(children[i]))

        # Mutate each drone's path
        for j in range(numdrones):
            # Define the index range for the current drone's path
            start_idx = (j * (numtrackp + 2)) + 1  # Start index for the drone
            end_idx = (j + 1) * (numtrackp + 2) - 1  # End index for the drone

            # Iterate through each point in the drone's path
            for k in range(start_idx, end_idx):
                # Get the current coordinates (x1, y1, z1) for the point
                x1, y1, z1 = mutants[f][k]

                # Define possible offsets to mutate the position
                offset = [-7, -6, -5, -4, -3, 3, 4, 5, 6, 7]

                # Generate all possible combinations of mutated coordinates based on offsets
                combinations = generate_combinations((x1, y1, z1), offset)                

                # Sort the combinations to prioritize certain changes
                for n in range(len(combinations)):
                    zx = sorted(combinations, reverse=True)  # Sorting in reverse order for preference
                    c = zx[n]  # Get the current combination

                    # Check if the mutated coordinate is valid and does not violate any constraints
                    if check(c, mutants[f], k) == False:
                        # Apply the mutation if valid
                        mutants[f][k] = c
                        break  # Exit the loop after applying the mutation


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

def check(p1, a1, k):
    # Extracting the coordinates of the point to check (x, y, z) and the index (d)
    x = p1[0]
    y = p1[1]
    z = p1[2]
    d = k

    # Check if the point is within the valid grid size
    if x < 0 or x > gridsize or y < 0 or y > gridsize or z < 0 or z > gridsize:
        #print("Point is out of bounds GA, skipping.")  # Debugging statement for out of bounds 
        return True  # Return True to indicate this point is invalid (out of bounds)
    
    # Check if the point already exists in the list (duplicates)
    if not PointValid(p1, a1, d):
        #print("Point is already exists GA, skipping.")  # Debugging statement for duplicates
        return True  # Return True to indicate this point is invalid (duplicate)

    # If the point is not the first point, check if the previous points are valid vertically
    if d > 1:
        if not vertical_check(a1[d - 2], a1[d - 1], p1):
            #print("Vertical check failed GA, skipping.")
            return True  # Return True if vertical check fails
    
    # Check if the point lies on a valid line from the previous points
    if not Trackpointlinevalid(a1[d - 1], p1, a1, d): 
        #print("Line check failed GA, skipping.")  # Debugging statement for line check failure
        return True  # Return True if line check fails
    
    # Check if the point passes the horizontal validity check
    if not Horz_check(a1[d - 1], p1):
        #print("Horizontal check failed GA, skipping.")  # Debugging statement for horizontal check failure
        return True  # Return True if horizontal check fails

    # Special case for the last track point, needs additional checks with the point after it
    if d == numtrackp or d == (len(a1) - 2):
        # Check if the vertical relationship between the last point and the next one is valid
        if not vertical_check(a1[d - 1], p1, a1[-1]):
            #print("Vertical check failed GA, skipping.")
            return True  # Return True if vertical check fails
        
        # Check if the line between the current point and the last point is valid
        if not Trackpointlinevalid(p1, a1[-1], a1, d):
            #print("Line check failed GA, skipping.")  # Debugging statement for line check failure
            return True  # Return True if line check fails
        
        # Check if the horizontal relationship between the current point and the last point is valid
        if not Horz_check(p1, a1[-1]):
           #print("Horizontal check failed GA, skipping.")  # Debugging statement for horizontal check failure
            return True  # Return True if horizontal check fails
    
    # If all checks pass, return False indicating the point is valid
    return False


cost=[] #cost list to store the best fitness value of each generation

def run():
    # Initialize an empty list to store output
    Output = []

    # Generate obstacles and create the map for the simulation
    createobs(gridsize)
    createmap()

    # Main loop for each generation in the genetic algorithm
    for i in range(numofgen):
        # Generate a new generation based on the current population
        newgen()
        
        # Print the current generation number
        print("Generation: ", i)
        
        # Evaluate the fitness of the current generation
        fittest()
        print("Best fitness value: ", min(fitness))  # Print the best fitness value of the current generation
        print("Best individual: ", children[fitness.index(min(fitness))])  # Print the best individual of the current generation
        # Append the best fitness value of the current generation to the cost list
        cost.append(min(fitness))

    # After all generations, select the elites (best individuals)
    elite()

    # Copy the best individual from the elites to the output list
    Output = copy.deepcopy(elites[0])

    # Return the best individual and the best fitness value from the last generation
    return Output, cost[-1]

# Only run the following code when this file is executed directly
if __name__ == "__main__":
    Output, bestobjective = run()  # Run the genetic algorithm
    plt.plot(cost)  # Plot the cost history over iterations
    plot_map(Output, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles