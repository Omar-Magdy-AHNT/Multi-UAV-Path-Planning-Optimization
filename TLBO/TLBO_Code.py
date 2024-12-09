import sys
import os

# Add the root directory of your project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import necessary modules
from TLBO.TLBO_Const1 import *  # Import constants related to the simulation
from TLBO.TLBO_Const2 import *  # Import additional constants
from TLBO.TLBO_Const3 import *  # Import more constants
from TLBO.TLBO_Const4 import Trackpointlinevalid  # Import function to validate track point lines
from TLBO.TLBO_Const5 import *  # Import function to check distance constraint
from TLBO.TLBO_Param import *  # Import data structures and variables
from TLBO.TLBO_ObjFunc1 import *  # Import first objective function
from TLBO.TLBO_ObjFunc2 import *  # Import second objective function
from TLBO.TLBO_ObjFunc3 import *  # Import second objective function
from TLBO.TLBO_CreateMap import *  # Import function to create the map
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting toolkit
import numpy as np  # Import numpy for numerical operations
import itertools  # Import itertools for generating combinations

def fitness():
    global Ranking, TopStudent, TopScore
    Ranking = []
    for i in range(numstudents):
        x = func1(i, Students)  # This function returns distance values for the i-th child
        y = func2(i, Students)
        z = func3(i, Students)
        total_dist = sum(x)
        total_danger = sum(y)
        total_penalty = sum(z)
        fit = total_dist + total_danger + total_penalty
        Ranking.append(fit)
    if TopScore == 0:
        TopStudent = Students[Ranking.index(min(Ranking))].copy()
        TopScore = min(Ranking)
    elif TopScore > min(Ranking):
        TopStudent = Students[Ranking.index(min(Ranking))].copy()
        TopScore = min(Ranking)

def teacher_phase():
    for i in range(numstudents):
        for k in range(numdrones):
            start_idx = (k) * (numtrackp + 2) + 1
            end_idx = (k + 1) * (numtrackp + 2)
            for j in range(start_idx, end_idx - 1):
                r = random.random()
                px = Students[i][j][0] + r*(TopStudent[j][0] - TeachFactor*meanpoints[j][0])
                py = Students[i][j][1] + r*(TopStudent[j][1] - TeachFactor*meanpoints[j][1])
                pz = Students[i][j][2] + r*(TopStudent[j][2] - TeachFactor*meanpoints[j][2])
                p = (math.ceil(px), math.ceil(py), math.ceil(pz))
                if not check(p,i,j): 
                    Students[i][j] = p  # Update the student's position

def learner_phase():
    for i in range(numstudents):
        for k in range(numdrones):
            start_idx = (k) * (numtrackp + 2) + 1
            end_idx = (k + 1) * (numtrackp + 2)
            for j in range(start_idx, end_idx - 1):
                r = random.random()
                while True:
                    b = random.randint(0, numstudents - 1)
                    if b != i:
                        break
                if Ranking[i] > Ranking[b]:
                    px = Students[i][j][0] + r*(Students[i][j][0] - Students[b][j][0])
                    py = Students[i][j][1] + r*(Students[i][j][1] - Students[b][j][1])
                    pz = Students[i][j][2] + r*(Students[i][j][2] - Students[b][j][2])
                    p = (math.ceil(px), math.ceil(py), math.ceil(pz))
                else:
                    px = Students[i][j][0] - r*(Students[b][j][0] - Students[i][j][0])
                    py = Students[i][j][1] - r*(Students[b][j][1] - Students[i][j][1])
                    pz = Students[i][j][2] - r*(Students[b][j][2] - Students[i][j][2])
                    p = (math.ceil(px), math.ceil(py), math.ceil(pz))
                if not check(p,i,j): 
                    Students[i][j] = p  # Update the student's position

def meanp():
    global meanpoints
    meanpoints = []
    for k in range(numdrones):
        meanpoints.append((0, 0, 0))
        start_idx = (k) * (numtrackp + 2)+1 
        end_idx = (k + 1) * (numtrackp + 2)
        for j in range(start_idx, end_idx-1):
            sumx = 0
            sumy = 0
            sumz = 0
            for i in range(numstudents):
                sumx += Students[i][j][0]
                sumy += Students[i][j][1]
                sumz += Students[i][j][2]
            meanpoints.append((sumx/numstudents, sumy/numstudents, sumz/numstudents))
        meanpoints.append((0, 0, 0))


def check(point,ai,i):
    x = point[0]
    y = point[1]
    z = point[2]
    A = Students[ai]
    # Check if the point is within the valid grid size
    if x < 0 or x > gridsize or y < 0 or y > gridsize or z < 0 or z > gridsize:
        #print("Point is out of bounds PSO, skipping.")  # Debugging statement for out of bounds 
        return True  # Return True to indicate this point is invalid (out of bounds)
    
    if not PointValid(point, A):
        #print("Point is already exists PSO, skipping.")  # Debugging statement for duplicates
        return True  # Return True to indicate this point is invalid (duplicate)
    
    # if not dist(A[i - 1], point):
    #     #print("Distance check failed PSO, skipping.")  # Debugging statement for distance check failure
    #     return True  # Return True if distance check fails

    if not Horz_check(A[i - 1], point):
        #print("Horizontal check failed PSO, skipping.")  # Debugging statement for horizontal check failure
        return True  # Return True if horizontal check fails

    # Check if the point lies on a valid line from the previous points
    if not Trackpointlinevalid(A[i - 1], point, A, i): 
        #print("Line check failed PSO, skipping.")  # Debugging statement for line check failure
        return True  # Return True if line check fails
    
    if i > 1:
        if not vertical_check(A[i - 2], A[i - 1], point):
            #print("Vertical check failed PSO, skipping.")
            return True  # Return True if vertical check fails
    
    if i == numtrackp or i == (len(A) - 2):
        # Check if the vertical relationship between the last point and the next one is valid
        if not vertical_check(A[i - 1], point, A[-1]):
            #print("Vertical check failed PSO, skipping.")
            return True  # Return True if vertical check fails
        
        # Check if the line between the current point and the last point is valid
        if not Trackpointlinevalid(point, A[-1], A, i):
            #print("Line check failed PSO, skipping.")  # Debugging statement for line check failure
            return True  # Return True if line check fails
        
        # Check if the horizontal relationship between the current point and the last point is valid
        if not Horz_check(point, A[-1]):
            #print("Horizontal check failed PSO, skipping.")  # Debugging statement for horizontal check failure
            return True  # Return True if horizontal check fails
    
    # If all checks pass, return False indicating the point is valid
    return False



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
    
def run():
    createobs(gridsize)  # Create obstacles in the simulation grid
    createmap()  # Create the map for drones, including start and end points
    fitness()
    cost.append(TopScore)
    print("Best Rank: ", TopScore) # Print the best fitness value of the current generation
    print("Top Student: ", TopStudent)  # Print the best individual of the current generation
    for i in range(schooldays):
        print("Iteration: ", i)
        meanp()
        teacher_phase()
        fitness()
        learner_phase()
        fitness()
        cost.append(TopScore)
        print("Best Rank: ", TopScore) # Print the best fitness value of the current generation
        print("Top Student: ", TopStudent)  # Print the best individual of the current generation
    bestobjective = cost[-1]
    Output = TopStudent
    return Output, bestobjective

# Only run the following code when this file is executed directly
if __name__ == "__main__":
    Output, bestobjective = run()  # Run the ant colony algorithm
    plt.plot(cost)  # Plot the cost history over iterations
    plot_map(Output, obstlist, numdrones, numtrackp, gridsize)  # Plot the final drone paths and obstacles