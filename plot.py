import numpy as np
import matplotlib.pyplot as plt

# Function to load the saved .npy file
def load_terrain_map(file_name):
    return np.load(file_name)

# Function to plot the loaded terrain map
def visualize_loaded_terrain(terrain_map, grid_size):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Get coordinates of the marked terrain points
    x, y, z = np.nonzero(terrain_map)
    
    # Reduce the number of points to plot for better performance
    if len(x) > 100000:  # Limit to 100,000 points for plotting
        indices = np.random.choice(len(x), 100000, replace=False)
        x, y, z = x[indices], y[indices], z[indices]

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
file_name = "terrain_map.npy"  # Name of your saved .npy file
grid_size = 10  # Use the same grid size as before

# Load the terrain map
terrain_map = load_terrain_map(file_name)

# Visualize the loaded terrain map
visualize_loaded_terrain(terrain_map, grid_size)
