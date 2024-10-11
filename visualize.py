import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Map

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter( Map.x , Map.y, Map.z, c= Map.z, cmap='terrain')
plt.show()
