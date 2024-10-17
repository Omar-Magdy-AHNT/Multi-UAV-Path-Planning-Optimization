import laspy
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the .laz file using laspy
def load_laz_file(file_path):
    las = laspy.read(file_path)
    x, y, z = las.x, las.y, las.z  # Extract X, Y, Z coordinates
    return np.vstack((x, y, z)).T  # Stack them into a point array

# Step 2: Create a 3D terrain grid with integer points
def create_terrain_map(point_cloud, grid_size, elevation_threshold):
    # Get min and max bounds of the points to create the array size
    min_x, min_y, min_z = np.floor(point_cloud.min(axis=0))
    max_x, max_y, max_z = np.ceil(point_cloud.max(axis=0))

    # Calculate the size of the 3D grid based on the grid_size
    x_size = int((max_x - min_x) // grid_size) + 1
    y_size = int((max_y - min_y) // grid_size) + 1
    z_size = int((max_z - min_z) // grid_size) + 1

    print(f"Min bounds: {min_x}, {min_y}, {min_z}")
    print(f"Max bounds: {max_x}, {max_y}, {max_z}")
    print(f"Grid sizes: {x_size}, {y_size}, {z_size}")

    # Step 3: Create a dense 3D array to store terrain data
    terrain_map = np.zeros((x_size, y_size, z_size), dtype=np.int8)

    # Step 4: Mark the points and all points below as terrain
    for point in point_cloud:
        x, y, z = point

        # Use integer floor values for grid positions
        grid_x = int((x - min_x) // grid_size)
        grid_y = int((y - min_y) // grid_size)
        grid_z = int((z - min_z) // grid_size)

        # Mark all points below the current point as '1'
        terrain_map[grid_x, grid_y, :grid_z+1] = 1

    return terrain_map

# Step 5: Visualize the terrain map (in 3D)
def visualize_terrain(terrain_map, grid_size):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Get coordinates of the marked terrain points
    x, y, z = np.nonzero(terrain_map)
    
    # Scale back the coordinates based on grid size
    x = x * grid_size
    y = y * grid_size
    z = z * grid_size

    ax.scatter(x, y, z, c=z, cmap='terrain', marker='o', s=1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Terrain Visualization')
    plt.show()

# Example usage
file_path = 'points.laz'
grid_size = 10  # Adjust the grid size to balance resolution and performance
elevation_threshold = 0  # Adjust if you need to ignore points below a certain height

# Load the point cloud from the .laz file
point_cloud = load_laz_file(file_path)

# Create the terrain map
terrain_map = create_terrain_map(point_cloud, grid_size, elevation_threshold)

# Visualize the terrain map
visualize_terrain(terrain_map, grid_size)
