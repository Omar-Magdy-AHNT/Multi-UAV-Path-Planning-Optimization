import matplotlib.pyplot as plt
import numpy as np

def load_terrain_map(filename):
    terrain_map = np.load(filename)
    print(f"Terrain map loaded from {filename}")
    return terrain_map

# Step 7: Visualize the 3D terrain map
def visualize_terrain_map(terrain_map, grid_size):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Get coordinates of all points where terrain_map == 1
    x, y, z = np.nonzero(terrain_map)

    # Scale the points by grid size (to get the original dimensions)
    x = x * grid_size
    y = y * grid_size
    z = z * grid_size

    # Apply color map based on Z-values
    norm = plt.Normalize(vmin=z.min(), vmax=z.max())  # Normalize the Z-values for the colormap
    colors = plt.cm.viridis(norm(z))  # Use the 'viridis' colormap

    # Plot the terrain points with colors based on elevation (Z-values)
    ax.scatter(x, y, z, c=colors, marker='o', s=1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Terrain Map Visualization with Elevation Colors')

    plt.show()

# Example usage:
grid_size = 10  # Adjust the grid size to balance resolution and performance
terrain_map = load_terrain_map('terrain_map.npy')
#visualize_terrain_map(terrain_map, grid_size)
###############GETTING START POINTS################
""" if terrain_map[0][0][0] == 1:
    print("Obstacle detected")  
else:
    print("No obstacle detected")

print(len(terrain_map))

lowest_empty_point = None

# Iterate over the X and Y dimensions
for x in range(terrain_map.shape[0]):
    for y in range(terrain_map.shape[1]):
        # Check for the lowest Z index where the value is 0
        for z in range(terrain_map.shape[2]):
            if terrain_map[x, y, z] == 0:
                lowest_empty_point = (x, y, z)
                break  # Breaks out of the innermost loop
        if lowest_empty_point is not None:
            break  # Breaks out of the second loop
    if lowest_empty_point is not None:
        break  # Breaks out of the outermost loop

if lowest_empty_point:
    print("Lowest empty point (X, Y, Z):", lowest_empty_point)
else:
    print("No empty points found in the terrain.") """

############GETTING END POINTS################
# Get the shape of the terrain map get 
x_size, y_size, z_size = terrain_map.shape

# 1. Calculate mid-elevation for Z
min_z = 0  # Assuming elevation starts from 0
max_z = z_size - 1
mid_elevation = (min_z + max_z) / 2
print(f"Mid-elevation (Z): {mid_elevation}")

# Convert mid_elevation to integer
mid_elevation = int(mid_elevation)

# 2. Find the maximum points in X and Y
max_x_index = x_size - 1
max_y_index = y_size - 1

# 3. Search for the point at mid-elevation and farthest in X and Y
suitable_points = []

# Iterate over the maximum extent in X and Y to find a point above the mid-elevation
for x in range(max_x_index + 1):
    for y in range(max_y_index + 1):
        # Check if there are any points at the mid-elevation or higher
        for z in range(mid_elevation, z_size):
            if terrain_map[x, y, z] > 0:  # Check if this is a valid terrain point
                suitable_points.append((x, y, z))

# Select the furthest point(s) that meet the criteria
if suitable_points:
    # Sort points by distance from the origin (0,0)
    suitable_points.sort(key=lambda point: (point[0], point[1]), reverse=True)
    selected_point = suitable_points[0]  # furthest point
    print(f"Selected point (X, Y, Z): {selected_point}")
else:
    print("No suitable point found.")

