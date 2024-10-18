import laspy
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the .laz file using laspy and create point cloud
def load_laz_file(file_path):
    las = laspy.read(file_path)
    x, y, z = las.x, las.y, las.z  # Extract X, Y, Z coordinates
    return np.vstack((x, y, z)).T  # Stack them into a point array

# Step 2: Create a 3D terrain grid with integer points (binary obstacle map)
def create_terrain_map(point_cloud, grid_size, min_z):
    # Get min and max bounds of the points to create the array size
    min_x, min_y, min_z = np.floor(point_cloud.min(axis=0))  # Override min_z for custom floor
    max_x, max_y, max_z = np.ceil(point_cloud.max(axis=0))

    # Calculate the size of the 3D grid based on the grid_size
    x_size = int((max_x - min_x) // grid_size) + 1
    y_size = int((max_y - min_y) // grid_size) + 1
    z_size = int((max_z - min_z) // grid_size) + 1

    print(f"Min bounds: {min_x}, {min_y}, {min_z}")
    print(f"Max bounds: {max_x}, {max_y}, {max_z}")
    print(f"Grid sizes: {x_size}, {y_size}, {z_size}")

    # Step 3: Create a 3D array to store binary terrain data (1: obstacle, 0: free)
    terrain_map = np.zeros((x_size, y_size, z_size), dtype=np.int8)

    # Step 4: Mark the points and all points below as terrain
    for point in point_cloud:
        x, y, z = point

        # Use integer floor values for grid positions
        grid_x = int((x - min_x) // grid_size)
        grid_y = int((y - min_y) // grid_size)
        grid_z = int((z - min_z) // grid_size)

        # Mark all points below the current point as '1' (obstacle)
        terrain_map[grid_x, grid_y, :grid_z+1] = 1

    return terrain_map

# Step 5: Save the terrain map as a .npy file
def save_terrain_map(terrain_map, filename):
    np.save(filename, terrain_map)
    print(f"Terrain map saved to {filename}")

# Step 6: Load the terrain map from a .npy file


# Example usage:
file_path = 'points.laz'
grid_size = 10  # Adjust the grid size to balance resolution and performance
min_z = 0  # Define a custom minimum z if needed

# Load the point cloud from the .laz file
point_cloud = load_laz_file(file_path)

# Create the terrain map from the point cloud
terrain_map = create_terrain_map(point_cloud, grid_size, min_z)

# Save the terrain map to a .npy file
save_terrain_map(terrain_map, 'terrain_map.npy')



