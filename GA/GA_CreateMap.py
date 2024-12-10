from GA.GA_Const1 import *  # Import constants related to the simulation
from GA.GA_Const2 import *  # Import additional constants
from GA.GA_Const3 import *  # Import more constants
from GA.GA_Const4 import Trackpointlinevalid  # Import function to validate track points
from GA.GA_Param import *  # Import data structures and variables
import random  # Import random module


def generate_integer_points(grid_size):
    points = []
    for x in range(grid_size + 1):
        for y in range(grid_size + 1):
            for z in range(grid_size + 1):
                points.append((x, y, z))
    return points


# Function to create obstacles in the simulation grid
def createobs(gridsize):
    global obstlist  # Explicitly refer to the global variable
    added_points = set()  # Set to keep track of added points

    # Add all points where z = 0 as obstacles
    for x in range(gridsize+1):
        for y in range(gridsize+1):
            point = (x, y, 0)
            if point not in added_points:
                obstlist.append(point)
                added_points.add(point)

    # Add vertical obstacles for specified base points
    base_points = [(9, 9), (5, 5), (3, 3)]
    for base_x, base_y in base_points:
        for z in range(gridsize+1):  # Add points from z = 0 to gridsize - 1
            point = (base_x, base_y, z)
            if point not in added_points:
                obstlist.append(point)
                added_points.add(point)

# Function to create the map for drones, including start and end points
def createmap():
    for k in range(numpopu):  # Iterate over each child
        for i in range(numdrones):  # Iterate over each drone
            startpt = (0, i, 1)  # Define the start point for the drone
            endpt = (gridsize-2, gridsize - i, 2)  # Define the endpoint for the drone
            population[k].append(startpt)  # Add the start point to Droneinfo
            startpoint.append(startpt)  # Add the start point to the startpoint list
            endpoint.append(endpt)  # Add the end point to the endpoint list
            added_points = 0  # Initialize count of successfully added track points
            possible_points = generate_integer_points(gridsize)
            # Keep trying until we add the required number of track points
            while added_points < numtrackp: 
                random.seed(random.random()) 
                x, y, z = random.choice(possible_points)  # Randomly select a new point from possible points

                # Check if the generated point is in the obstacle list
                if not PointValid((x, y, z), population[k]):
                    print("Point is already invalid, skipping.")  # Debugging statement for duplicates
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration

                # Check for horizontal constraints if applicable
                if not Horz_check(population[k][-1], (x, y, z)):
                    print("Horizontal check failed, skipping.")  # Debugging statement for horizontal check
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration

                # Check for vertical constraints if applicable
                if len(population[k]) > (1 + ((numtrackp + 2) * i)) and not vertical_check(population[k][-2],population[k][-1], (x, y, z)):
                    print("Vertical check failed, skipping.")  # Debugging statement for vertical check
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration
            
                # Validate the line between the last point and the new point
                if  not Trackpointlinevalid(population[k][-1], (x, y, z),population[k],(len(population[k])-1)):
                    print("Line check failed, skipping.")  # Debugging statement for line check
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration
            


                # If all checks pass, add the point to the drone's information
                population[k].append((x, y, z))  # Add the new track point to Droneinfo
                possible_points.remove((x, y, z))  # Remove the point from possible points
                added_points += 1  # Increment the count of successfully added track points
        
            population[k].append(endpt)  # Append the endpoint after adding all track points