import laspy
import numpy as np
import pandas as pd
from scipy.sparse import dok_matrix

# Step 1: Load the .laz file using laspy
def load_laz_file(file_path):
    las = laspy.read(file_path)
    x, y, z = las.x, las.y, las.z  # Extract X, Y, Z coordinates
    return np.vstack((x, y, z)).T  # Stack them into a point array

# Step 2: Create a sparse matrix map with integer points
def create_integer_terrain_map(point_cloud, grid_size, elevation_threshold):
    # Get min and max bounds of the points to create the array size
    min_x, min_y, min_z = np.floor(point_cloud.min(axis=0))
    max_x, max_y, max_z = np.ceil(point_cloud.max(axis=0))
    
    # Calculate the size of the grid based on the grid_size
    x_size = int((max_x - min_x) // grid_size) + 1
    y_size = int((max_y - min_y) // grid_size) + 1
    
    # Create a sparse 2D matrix initialized with zeros
    terrain_map = dok_matrix((x_size, y_size), dtype=np.int8)

    # Step 3: Fill the sparse array with '1' where there's terrain data
    for point in point_cloud:
        x, y, z = point
        
        # Use integer floor values for grid positions
        grid_x = int((x - min_x) // grid_size)
        grid_y = int((y - min_y) // grid_size)
        
        # Apply a threshold to mark points considered as terrain
        if z >= elevation_threshold:
            terrain_map[grid_x, grid_y] = 1  # Mark terrain point as '1'
    
    return terrain_map

# Step 4: Save the sparse matrix to a CSV file
def save_terrain_map(terrain_map, file_name):
    # Convert DOK matrix to CSR before saving
    csr_map = terrain_map.tocsr()  # Convert to CSR format
    
    # Convert sparse matrix to a dense format for saving
    dense_map = csr_map.toarray()
    
    # Save to CSV
    np.savetxt(file_name, dense_map, delimiter=',', fmt='%d')

# Step 5: Load the sparse matrix from a CSV file
def load_terrain_map(file_name):
    dense_map = np.loadtxt(file_name, delimiter=',')
    return dense_map

# Example usage
file_path = 'points.laz'
grid_size = 1  # Integer grid size
elevation_threshold = 0  # Adjust the threshold if needed

# Load the point cloud from the .laz file
point_cloud = load_laz_file(file_path)

# Create a sparse matrix map with integer points
terrain_map = create_integer_terrain_map(point_cloud, grid_size, elevation_threshold)

# Save the terrain map to a CSV file
save_terrain_map(terrain_map, 'terrain_map.csv')

# Load the terrain map back from the CSV file (if needed)
loaded_terrain_map = load_terrain_map('terrain_map.csv')
print(loaded_terrain_map)
