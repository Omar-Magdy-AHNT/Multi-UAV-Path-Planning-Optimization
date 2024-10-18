import laspy
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Step 1: Load the .laz file using laspy
def load_laz_file(file_path):
    las = laspy.read(file_path)
    x, y, z = las.x, las.y, las.z  # Extract X, Y, Z coordinates
    return np.vstack((x, y, z)).T  # Stack them into a point array

# Step 2: Create a 3D terrain grid with interpolation to fill gaps
def create_interpolated_terrain_map(point_cloud, grid_size):
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

    # Step 3: Generate a grid for interpolation
    grid_x, grid_y = np.meshgrid(np.arange(min_x, max_x, grid_size),
                                 np.arange(min_y, max_y, grid_size))

    # Step 4: Perform interpolation for the z-values
    points_2d = point_cloud[:, :2]  # Take X and Y coordinates
    z_values = point_cloud[:, 2]  # Take Z coordinates
    terrain_map_2d = griddata(points_2d, z_values, (grid_x, grid_y), method='linear')

    # Replace NaNs with zeros to avoid gaps in the terrain map
    terrain_map_2d = np.nan_to_num(terrain_map_2d, nan=min_z)

    # Expand the terrain_map_2d into 3D by assuming that all points below a surface point are solid terrain
    terrain_map = np.zeros((grid_x.shape[0], grid_y.shape[1], z_size), dtype=np.int8)

    # Step 5: Mark all points below the surface point as '1'
    for i in range(terrain_map_2d.shape[0]):
        for j in range(terrain_map_2d.shape[1]):
            surface_z = int((terrain_map_2d[i, j] - min_z) // grid_size)
            terrain_map[i, j, :surface_z+1] = 1  # Mark all terrain points below the surface

    return terrain_map

# Step 6: Save the terrain map as a .npy file
def save_terrain_map(terrain_map, file_name):
    np.save(file_name, terrain_map)
    print(f"Terrain map saved as {file_name}.npy")

# Step 7: Visualize the terrain map (in 3D)
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

    # Save the plot as a file
    plt.savefig("terrain_plot_interpolated.png")
    print("Terrain plot saved as terrain_plot_interpolated.png")
    plt.show()

# Example usage
file_path = 'points.laz'
grid_size = 5  # Adjust the grid size to balance resolution and performance

# Load the point cloud from the .laz file
point_cloud = load_laz_file(file_path)

# Create the interpolated terrain map
terrain_map = create_interpolated_terrain_map(point_cloud, grid_size)

# Save the terrain map to a .npy file
save_terrain_map(terrain_map, 'interpolated_terrain_map')

# Visualize the interpolated terrain map
visualize_terrain(terrain_map, grid_size)
