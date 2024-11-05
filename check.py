from Const5 import *  # Import remaining constants

points = [(0, 1, 1), (1, 0, 1), (2, 3, 3), (1, 2, 2), (4, 2, 2), (1, 1, 4), (0, 3, 1), (8, 9, 2)]

for i in range(len(points)-1):
    if not Dist(points[i], points[i+1]):
        print(f"Points {points[i]} and {points[i+1]} exceed the distance condition.")
