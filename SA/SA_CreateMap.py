from SA.SA_Const1 import *  # Import constants related to the simulation
from SA.SA_Const2 import *  # Import additional constants
from SA.SA_Const3 import *  # Import more constants
from SA.SA_Const4 import Trackpointlinevalid  # Import function to validate track points
from SA.SA_Const5 import *  # Import remaining constants
from SA.SA_Param import *  # Import data structures and variables
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
    base_points = [(9, 9), (5, 5), (3, 3)]  # Define base points for obstacle creation
    added_points = set()  # Set to keep track of added points

    # Create obstacles based on base points
    for base_x, base_y in base_points:  # Iterate over each base point
        for x_offset in range(1):  # No offset in x direction
            for y_offset in range(1):  # No offset in y direction
                for z in range(gridsize):  # Iterate through each height level
                    x = base_x + x_offset  # Calculate x coordinate
                    y = base_y + y_offset  # Calculate y coordinate
                    point = (x, y, z)  # Create the point
                    if point not in added_points:  # Check if the point is already added
                        obstlist.append(point)  # Add the point to the obstacle list
                        added_points.add(point)  # Mark this point as added

    # Add the floor (all points in the xy-plane at z = 0)
    for x in range(gridsize):  # Iterate over all x coordinates
        for y in range(gridsize):  # Iterate over all y coordinates
            point = (x, y, 0)  # Create point at z = 0
            if point not in added_points:  # Check if the point is already added
                obstlist.append(point)  # Add the point to the obstacle list
                added_points.add(point)  # Mark this point as added

# Function to create the map for drones, including start and end points
def createmap():
    for i in range(numdrones):  # Iterate over each drone
        startpt = (0, i, 1)  # Define the start point for the drone
        endpt = (gridsize-2, gridsize - i, 2)  # Define the endpoint for the drone
        Droneinfo.append(startpt)  # Add the start point to Droneinfo
        startpoint.append(startpt)  # Add the start point to the startpoint list
        endpoint.append(endpt)  # Add the end point to the endpoint list
        added_points = 0  # Initialize count of successfully added track points
        possible_points = generate_integer_points(gridsize)
        # Keep trying until we add the required number of track points
        while added_points < numtrackp:  
            x, y, z = random.choice(possible_points)  # Randomly select a new point from possible points

            # Check if the generated point is in the obstacle list
            if (x, y, z) in obstlist:
                print("Point is an obstacle, skipping.")  # Debugging statement for obstacles
                possible_points.remove((x, y, z))  # Remove the point from possible points
                continue  # Skip to the next iteration
            
            # Check if the generated point is already in Droneinfo
            if (x, y, z) in Droneinfo:
                print("Point is already in Droneinfo, skipping.")  # Debugging statement for duplicates
                possible_points.remove((x, y, z))  # Remove the point from possible points
                continue  # Skip to the next iteration

            # Check for horizontal constraints if applicable
            if not Horz_check(Droneinfo[-1], (x, y, z)):
                print("Horizontal check failed, skipping.")  # Debugging statement for horizontal check
                possible_points.remove((x, y, z))  # Remove the point from possible points
                continue  # Skip to the next iteration

            # Check for vertical constraints if applicable
            if len(Droneinfo) > (1 + (numtrackp + 2) * i) and not vertical_check(Droneinfo[-2], Droneinfo[-1], (x, y, z)):
                print("Vertical check failed, skipping.")  # Debugging statement for vertical check
                possible_points.remove((x, y, z))  # Remove the point from possible points
                continue  # Skip to the next iteration
            
            # Validate the line between the last point and the new point
            if  not Trackpointlinevalid(Droneinfo[-1], (x, y, z)):
                print("Line check failed, skipping.")  # Debugging statement for line check
                possible_points.remove((x, y, z))  # Remove the point from possible points
                continue  # Skip to the next iteration
            


            # If all checks pass, add the point to the drone's information
            Droneinfo.append((x, y, z))  # Add the new track point to Droneinfo
            Output.append((x, y, z))  # Also add the point to Output
            added_points += 1  # Increment the count of successfully added track points
        
        Droneinfo.append(endpt)  # Append the endpoint after adding all track points

"""             # Check distance constraints between the last point and the new point
            if  not Dist(Droneinfo[-1], (x, y, z)):
                print("Distance check failed, skipping.")  # Debugging statement for distance check
                possible_points.remove((x, y, z))  # Remove the point from possible points
                continue  # Skip to the next iteration """