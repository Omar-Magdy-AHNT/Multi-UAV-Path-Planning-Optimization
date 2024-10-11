import laspy

# Open and read the .laz file
file_path = 'points.laz'
with laspy.open(file_path) as f:
    las_file = f.read()  # Read all points from the file

# Extract point coordinates (x, y, z)
x = las_file.x
y = las_file.y
z = las_file.z

# You now have the coordinates of the points in your terrain
print(f'Number of points: {len(x)}')
        