import numpy as np

# Load the terrain map from the .npy file
file_path = 'terrain_map.npy'  # Path to your saved .npy file
terrain_map = np.load(file_path)

# Print the shape of the terrain map
print(f"Shape of the terrain map: {terrain_map.shape}")

# Optionally, print a subset of the terrain map
# For example, print the first 10 rows and 10 columns of the first layer
print(terrain_map)  # Adjust slicing as needed

# If you want to print the entire terrain map (not recommended for large arrays):
# print(terrain_map)
