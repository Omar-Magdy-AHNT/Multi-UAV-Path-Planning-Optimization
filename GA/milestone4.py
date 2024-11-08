from Const1 import *  # Import constants related to the simulation
from Const2 import *  # Import additional constants
from Const3 import *  # Import more constants
from Const4 import Trackpointlinevalid  # Import function to validate track point lines
from Const5 import *  # Import remaining constants
from Data import *  # Import data structures and variables
from OF1 import *  # Import first objective function
from OF2 import *  # Import second objective function
import math  # Import math module for mathematical functions
from creatmap import *  # Import function to create the map
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting toolkit
import numpy as np  # Import numpy for numerical operations

def newgen():
    elite()
    mutation()
    crossover()


def elite():
    elites.clear()
    for i in range(numelite):
        fittest()
        i = fitness.index(min(fitness))
        elites = children[i]
        del children[i]
        del fitness[i]

def crossover():
    parents = elites
    for i in range(numparents - numelite):
        i = fitness.index(min(fitness))
        parents.append(children[i])
    fitness.clear()
    children.clear()
    for i in range(numchildren//2):
        child1 = []
        child2 = []
        for j in range(numdrones):
            for k in range(numtrackp+2):
                f1 = True
                f2 = True
                if k == 0:
                    children[i][k] = startpoint[j]
                    continue
                if k == numtrackp+1:
                    children[i][k] = endpoint[j]
                    continue
                while f1:
                    alpha = random.uniform(0.2,0.9)
                    x1 = (alpha*parents[0][k]) - (1-alpha)*parents[i+1][k]
                    y1 = (alpha*parents[0][k]) - (1-alpha)*parents[i+1][k]
                    z1 = (alpha*parents[0][k]) - (1-alpha)*parents[i+1][k]
                    c1 = (x1,y1,z1)
                    f1 = check(c1,child1,k)
                    if f1 == False:
                        child1.append((x1,y1,z1))

                while f2:
                    x2 = (alpha*parents[i+1][k])- (1-alpha)*parents[0][k]
                    y2 = (alpha*parents[i+1][k])- (1-alpha)*parents[0][k]
                    z2 = (alpha*parents[i+1][k])- (1-alpha)*parents[0][k]
                    c2 = (x2,y2,z2)
                    f2 = check(c2,child2,k)
                    if f2 == False:
                        child2.append((x2,y2,z2))

        children.append(child1)
        children.append(child2)
    if numchildren % 2 == 1:
        fittest()
        if fitness[-1] > fitness[-2]:
            del children[-1]
        else: 
            del children[-2]
    children.extend(mutants)
    children.extend(elites)

def fittest():
    fitness.clear()
    z= []
    for i in range(numchildren):
        x = func1(i,children) 
        y = func2(i,children)
        for j in range(numdrones):
            z.append(x[j] + y[j])
        fitness.append(z)

def mutation():
    for f in range(nummutants):
        fittest()
        i = fitness.index(max(fitness))
        mutants = children[i]
        for j in range(numdrones):
            for k in range(numtrackp):
                flag = True
                while flag:
                    x1 = mutants[f][(k+1)+(numtrackp*j)][0] + random.choice(-1,0,1)
                    y1 = mutants[f][(k+1)+(numtrackp*j)][1] + random.choice(-1,0,1)
                    z1 = mutants[f][(k+1)+(numtrackp*j)][2] + random.choice(-1,0,1)
                    if check((x1,y1,z1),mutants[f],(k+1)+(numtrackp*j)) == False:
                        mutants[f][(k+1)+(numtrackp*j)] = (x1,y1,z1)
                        flag = False

# Function to plot the drone paths and obstacles in 3D
def plot_map(Droneinfo, obstlist, numdrones, numtrackp, gridsize):
    fig = plt.figure()  # Create a new figure
    ax = fig.add_subplot(111, projection='3d')  # Add a 3D subplot

    # Define a list of colors for each drone
    colors = plt.cm.jet(np.linspace(0, 1, numdrones))  # Generate a color map for drones

    # Plot each drone's path in a different color
    for i in range(numdrones):  # Iterate over each drone
        start_index = (numtrackp + 2) * i  # Calculate start index for the current drone's path
        end_index = start_index + (numtrackp + 2)  # Calculate end index for the current drone's path

        # Get the track points for this drone from Droneinfo
        drone_path = Droneinfo[start_index:end_index]  # Extract path points for the current drone
        xs, ys, zs = zip(*drone_path)  # Unpack into separate lists for x, y, z

        ax.plot(xs, ys, zs, color=colors[i], label=f'Drone {i + 1}', marker='o')  # Plot the drone path

    # Plot obstacles
    if obstlist:  # Check if there are obstacles to plot
        ox, oy, oz = zip(*obstlist)  # Unpack obstacle coordinates
        ax.scatter(ox, oy, oz, color='red', marker='x', label='Obstacles')  # Scatter plot for obstacles

    # Set axis limits based on grid size
    ax.set_xlim([0, gridsize])  # Set x-axis limits
    ax.set_ylim([0, gridsize])  # Set y-axis limits
    ax.set_zlim([0, gridsize])  # Set z-axis limits

    # Set labels and title
    ax.set_xlabel('X')  # Set x-axis label
    ax.set_ylabel('Y')  # Set y-axis label
    ax.set_zlabel('Z')  # Set z-axis label
    ax.set_title('Drone Paths with Obstacles')  # Set plot title

    plt.legend()  # Display the legend
    plt.show()  # Show the plot

def check(p1,a1,k):
    x= p1[0]
    y= p1[1]
    z= p1[2]
    d= k

    if x < 0 or x > gridsize or y < 0 or y > gridsize or z < 0 or z > gridsize:
        print("Point is out of bounds GA, skipping.")  # Debugging statement for out of bounds 
        return True
    
    if not PointValid(p1,a1,d):
        print("Point is already exists GA, skipping.")  # Debugging statement for duplicates
        return True
    
    if d > 1:
        if not vertical_check(a1[d - 2], a1[d - 1], (x, y, z)):
            print("Vertical check failed GA, skipping.")
            return True
        
    if not Trackpointlinevalid(a1[d - 1], (x, y, z),a1,d): 
        print("Line check failed GA, skipping.")  # Debugging statement for line check failure
        return True
    
    if not Horz_check(a1[d - 1], (x, y, z)) :
        print("Horizontal check failed GA, skipping.")  # Debugging statement for horizontal check failure
        return True
    
    if d == numtrackp or d == (len(a1)-2) : #last track point needs to be checked with point after 
            if not vertical_check(a1[d - 1],(x, y, z),a1[ - 1]):
                print("Vertical check failed GA, skipping.")
                return True
            if not Trackpointlinevalid((x, y, z), a1[-1],a1,d):
                print("Line check failed GA, skipping.")  # Debugging statement for line check failure
                return True
            if not Horz_check((x, y, z),a1[-1]):
                print("Horizontal check failed GA, skipping.")  # Debugging statement for horizontal check failure
                return True
    return False

cost=[]
Output=[]
createmap()
for i in range(numofgen):
    newgen()
    print("Generation: ", i)
    fittest()
    cost.append(fitness[fitness.index(min(fitness))])

Output = elites[fitness.index(min(fitness))]
plt.plot(cost)  # Plot the cost history over iterations
plot_map(Output, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles

