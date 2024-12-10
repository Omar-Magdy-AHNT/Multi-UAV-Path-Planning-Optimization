from PSO.PSO_Const1 import *  # Import constants related to the simulation  # noqa: F403
from PSO.PSO_Const2 import *  # Import additional constants  # noqa: F403
from PSO.PSO_Const3 import *  # Import more constants  # noqa: F403
from PSO.PSO_Const4 import Trackpointlinevalid  # Import function to validate track points  # Import remaining constants  # noqa: F403
from PSO.PSO_Param import *  # Import data structures and variables  # noqa: F403
import random  # Import random module

def generate_integer_points(grid_size):
    points = []
    for x in range(grid_size + 1):
        for y in range(grid_size + 1):
            for z in range(grid_size + 1):
                points.append((x, y, z))
    return points

# Example usage
grid_size = 10
all_points = generate_integer_points(grid_size)

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
    for k in range(numparticles):  # Iterate over each child  # noqa: F405
        for i in range(numdrones):  # Iterate over each drone  # noqa: F405
            startpt = (0, i, 1)  # Define the start point for the drone
            endpt = (gridsize-2, gridsize - i, 2)  # Define the endpoint for the drone  # noqa: F405
            Birds[k].append(startpt)  # Add the start point to Droneinfo  # noqa: F405
            startpoint.append(startpt)  # Add the start point to the startpoint list  # noqa: F405
            endpoint.append(endpt)  # Add the end point to the endpoint list  # noqa: F405
            added_points = 0  # Initialize count of successfully added track points
            possible_points = generate_integer_points(gridsize)  # noqa: F405
            # Keep trying until we add the required number of track points
            while added_points < numtrackp:  # noqa: F405
                x, y, z = random.choice(possible_points)  # Randomly select a new point from possible points

                # Check if the generated point is in the obstacle list
                if not PointValid((x, y, z), Birds[k]):  # noqa: F405
                    print("Point is already invalid, skipping.")  # Debugging statement for duplicates
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration

                # Check for horizontal constraints if applicable
                if not Horz_check(Birds[k][-1], (x, y, z)):  # noqa: F405
                    print("Horizontal check failed, skipping.")  # Debugging statement for horizontal check
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration

                # Check for vertical constraints if applicable
                if len(Birds[k]) > (1 + ((numtrackp + 2) * i)) and not vertical_check(Birds[k][-2],Birds[k][-1], (x, y, z)):  # noqa: F405
                    print("Vertical check failed, skipping.")  # Debugging statement for vertical check
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration
            
                # Validate the line between the last point and the new point
                if  not Trackpointlinevalid(Birds[k][-1], (x, y, z),Birds[k],(len(Birds[k])-1)):  # noqa: F405
                    print("Line check failed, skipping.")  # Debugging statement for line check
                    possible_points.remove((x, y, z))  # Remove the point from possible points
                    continue  # Skip to the next iteration
            
                # If all checks pass, add the point to the drone's information
                Birds[k].append((x, y, z))  # Add the new track point to Droneinfo  # noqa: F405
                possible_points.remove((x, y, z))  # Remove the point from possible points
                added_points += 1  # Increment the count of successfully added track points
        
            Birds[k].append(endpt)  # Append the endpoint after adding all track points  # noqa: F405