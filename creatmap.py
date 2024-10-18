from Const1 import *
from Const2 import *
from Const3 import *
from Const4 import Trackpointlinevalid
from Const5 import *
from Data import *

def createobs(gridsize):
    base_points = [(5, 5), (15, 15), (25, 25)] 
    added_points = set()  # Set to keep track of added points

    # Create obstacles based on base points
    for base_x, base_y in base_points:
        for x_offset in range(5): 
            for y_offset in range(5):
                for z in range(gridsize): 
                    x = base_x + x_offset
                    y = base_y + y_offset
                    point = (x, y, z)
                    if point not in added_points:  # Check if the point is already added
                        obstlist.append(point)
                        added_points.add(point)

    # Add the floor (all xy-plane at z = 0)
    for x in range(gridsize):
        for y in range(gridsize):
            point = (x, y, 0)  # Point at z = 0
            if point not in added_points:  # Check if the point is already added
                obstlist.append(point)
                added_points.add(point) 

def createmap():
    for i in range(numdrones):
        startpt = (0, i, 0)
        endpt = (gridsize, gridsize- i, gridsize)
        Droneinfo.append(startpt)
        
        added_points = 0  # Count of successfully added track points

        while added_points < numtrackp:  # Keep trying until we add the required number of points
            x = random.randint(0, gridsize)
            y = random.randint(0, gridsize)
            z = random.randint(0, gridsize)
            print(f"Generated point: ({x}, {y}, {z})")  # Debugging line

            # Check if the generated point is in the obstacle list
            if (x, y, z) in obstlist:
                print("Point is an obstacle, skipping.")
                continue
            
            # Check if the generated point is already in Droneinfo
            if (x, y, z) in Droneinfo:
                print("Point is already in Droneinfo, skipping.")
                continue

            # Check for horizontal constraints if applicable
            if len(Droneinfo) > 0 and not Horz_check(Droneinfo[-1], (x, y, z)):
                print("Horizontal check failed, skipping.")
                continue

            # Check for vertical constraints if applicable
            if len(Droneinfo) > 1 and not vertical_check(Droneinfo[-2], Droneinfo[-1], (x, y, z)):
                print("Vertical check failed, skipping.")
                continue

            # If all checks pass, add the point
            Droneinfo.append((x, y, z))
            Output.append((x, y, z))
            added_points += 1  # Increment the count of successfully added track points
        
        Droneinfo.append(endpt)  # Append the endpoint after adding all track points



