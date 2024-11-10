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
import itertools


def newgen():
    elite()
    mutation()
    crossover()


def elite():
    global elites
    elites.clear()
    fittest()
    for i in range(numelite):
        i = fitness.index(min(fitness))
        elites = children[i]
        del children[i]
        del fitness[i]

def generate_alpha_combinations(parents, i, k, alpha_values,intg):
    combinations = []
    if intg == 1:
        for alpha in alpha_values:
            x1 = (alpha * parents[0][k][0]) - (1 - alpha) * parents[i + 1][k][0]
            y1 = (alpha * parents[0][k][1]) - (1 - alpha) * parents[i + 1][k][1]
            z1 = (alpha * parents[0][k][2]) - (1 - alpha) * parents[i + 1][k][2]
            x1, y1, z1 = int(round(x1)), int(round(y1)), int(round(z1))
            c1 = (x1, y1, z1)
            combinations.append(c1)
    else:
        for alpha in alpha_values:
            x2 = (alpha*parents[i+1][k][0])- (1-alpha)*parents[0][k][0]
            y2 = (alpha*parents[i+1][k][1])- (1-alpha)*parents[0][k][1]
            z2 = (alpha*parents[i+1][k][2])- (1-alpha)*parents[0][k][2]
            x2, y2, z2 = int(round(x2)), int(round(y2)), int(round(z2))
            c2 = (x2, y2, z2)
            combinations.append(c2)
    return combinations



def crossover():
    parents.append(elites.copy())
    for il in range(numparents - numelite):
        h = fitness.index(min(fitness))
        parents.append(children[h])
    fitness.clear()
    children.clear()
    for i in range(round(numchildren/2)):
        child1 = []
        child2 = []
        for j in range(numdrones):
            for k in range(numtrackp+2):
                f1 = True
                f2 = True
                if k == 0:
                    child1.append(startpoint[j])
                    child2.append(startpoint[j])
                    continue
                if k == numtrackp+1:
                    child1.append(endpoint[j])
                    child2.append(endpoint[j])  
                    continue
                # Generate an array of alpha values from 0.4 to 0.9
                alpha_values = np.linspace(0.4, 0.9, num=10)  # Adjust `num` for the desired number of points
                combine = generate_alpha_combinations(parents, i, k, alpha_values,1)
                for c in range(len(combine)):
                    c1 = combine[c]
                    f1 = check(c1,child1,(len(child1)-1))
                    if f1 == False:
                        child1.append(c1)
                        break
                    if f1 == True and c == len(combine)-1:
                        child1.append(parents[0][k+(numtrackp+2)*j])

                combine = generate_alpha_combinations(parents, i, k, alpha_values,2)
                for v in range(len(combine)):
                    c2= combine[v]
                    f2 = check(c2,child2,(len(child2)-1))
                    if f2 == False:
                        child2.append(c2)
                        break
                    if f2 == True and v == len(combine)-1:
                        child2.append(parents[i][k+(numtrackp+2)*j])
        children.append(child1)
        children.append(child2)
    if numchildren % 2 == 1:
        fittest()
        if fitness[-1] > fitness[-2]:
            del children[-1]
        else: 
            del children[-2]
    for p in range(nummutants):
        children.append(mutants[p].copy())
    children.append(elites.copy())


def fittest():
    fitness.clear()
    for i in range(len(children)):
        x = func1(i,children) 
        y = func2(i,children)
        total_dist = sum(x)
        total_danger = sum(y)
        fitness.append(total_dist + total_danger)

def generate_combinations(original_xyz, offsets):
    original_x, original_y, original_z = original_xyz

    # Generate all combinations of x, y, and z with each offset
    combinations = [
        (original_x + dx, original_y + dy, original_z + dz)
        for dx, dy, dz in itertools.product(offsets, repeat=3)
    ]

    return combinations

def mutation():
    global mutants
    fittest()
    for f in range(nummutants):
        i = fitness.index(max(fitness))
        mutants.append(children[i].copy())
        for j in range(numdrones):
            for k in range(numtrackp):
                x1 ,y1 ,z1 = mutants[f][k+1+(numtrackp*j)]
                offest = [-2,-1,0,1,2]
                combinations = generate_combinations((x1, y1, z1), offest)                
                for n in range(len(combinations)):
                    if check((x1,y1,z1),mutants[f],(k+1)+(numtrackp*j)) == False:
                        mutants[f][(k+1)+(numtrackp*j)] = (x1,y1,z1)
                        break

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
    print("Best Fitness: ", fitness)
    cost.append(min(fitness))

Output = elites.copy()
plt.plot(cost)  # Plot the cost history over iterations
plot_map(Output, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles

