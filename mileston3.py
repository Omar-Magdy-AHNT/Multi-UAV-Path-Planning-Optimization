from Const1 import *
from Const2 import *
from Const3 import *
from Const4 import Trackpointlinevalid
from Const5 import *
from Data import *
from OF1 import *
from OF2 import *
import math
from creatmap import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

createobs(gridsize)
""" 
def neighbor_solution():
    #print('Droneinfo:', Droneinfo)
    #print('Droneinfo:', Droneinfo)
    flag = True
    new_Droneinfo = Droneinfo.copy()
    drone_index = random.randint(0, numdrones - 1)
    point_index = random.randint(1, numtrackp - 1)
    
    x, y, z = new_Droneinfo[drone_index * (numtrackp + 2) + point_index]
    
    while flag:
        x_new = max(0, min(gridsize, x + random.choice([-1, 1])))
        y_new = max(0, min(gridsize, y + random.choice([-1, 1])))
        z_new = max(0, min(gridsize, z + random.choice([-1, 1])))

        new_Droneinfo[drone_index * (numtrackp + 2) + point_index] = (x_new, y_new, z_new)
    
        new_point = (x_new, y_new, z_new)
        new_Droneinfo[drone_index * (numtrackp + 2) + point_index] = new_point
        if not is_valid_solution(new_Droneinfo):
            flag = False
        print("ss",is_valid_solution(new_Droneinfo))

    return new_Droneinfo

def is_valid_solution(Droneinfo):
    for drone_index in range(numdrones):
        for i in range(numtrackp):
            p1 = Droneinfo[drone_index * (numtrackp + 2) + i]
            if not PointValid(p1):
                return False
            if i < numtrackp - 1:
                p2 = Droneinfo[drone_index * (numtrackp + 2) + i + 1]

                if not Trackpointlinevalid(p1, p2):
                    return False
                
                if not Dist(p1, p2):
                    return False
                
            if i < numtrackp - 2:

                p2 = Droneinfo[drone_index * (numtrackp + 2) + i + 1]
                p3 = Droneinfo[drone_index * (numtrackp + 2) + i + 2]

                if not vertical_check(p1, p2, p3):
                    return False
                
                if not Horz_check(p1, p2):
                    return False
                
    return True

current_solution = Droneinfo
#print('Current solution:', current_solution)
best_solution = current_solution
current_objective = objective(current_solution)
best_objective = current_objective

while T0 > Tf:
    i = 0
    while i < imax:
        new_solution = neighbor_solution()
        new_objective = objective(new_solution)
        delta = new_objective - current_objective
        if delta < 0:
            current_solution = new_solution
            current_objective = new_objective
            if new_objective < best_objective:
                best_solution = new_solution
                best_objective = new_objective
        else:
            p = math.exp(-delta / T0)
            if random.random() < p:
                current_solution = new_solution
                current_objective = new_objective
        i += 1
    T0 *= alpha**i

    print('Best solution:', best_solution) """


def objective():
    distDrone.clear()
    danger.clear()
    func1()
    func2()
    total_distance = sum(distDrone)
    total_danger = sum(danger)
    obj = total_distance + 10*total_danger
    return obj

def newsolution():
    for i in range (numdrones):
        flag = False
        start_idx = (numtrackp) * i
        end_idx = (numtrackp) * (i + 1) - 1
        f = random.randint(start_idx, end_idx-1)
        g = Droneinfo.index(Output[f])
        while flag == False:
            x,y,z = Output[f]
            xn = x + random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            yn = y + random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            zn = z + random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            # Check if the generated point is in the obstacle list
            if (xn, yn, zn) in obstlist:
                print("Point is an obstacle SA, skipping.")
                continue
            
            # Check if the generated point is already in Droneinfo
            if (xn, yn, zn) in Droneinfo:
                print("Point is already in Droneinfo SA, skipping.")
                continue

            # Check for horizontal constraints if applicable
            if len(Droneinfo) > (0 +(numtrackp+2)*i)  and not Horz_check(Droneinfo[-1], (x, y, z)):
                print("Horizontal check failed SA, skipping.")
                continue

            # Check for vertical constraints if applicable
            if len(Droneinfo) > (1 +(numtrackp+2)*i) and not vertical_check(Droneinfo[-2], Droneinfo[-1], (x, y, z)):
                print("Vertical check failed SA, skipping.")
                continue
            if len(Droneinfo) > (1 +(numtrackp+2)*i) and not Trackpointlinevalid(Droneinfo[-1], (x, y, z)):
                print("Line check failed SA, skipping.")
                continue
            flag = True
        Output[f] = (xn,yn,zn)
        Droneinfo[g] = (xn,yn,zn)

tf = 1
imax = 3
alpha = 0.95
cost = []

def SA():
    tn = 100
    current_solution = Output
    best_solution = current_solution
    current_objective = objective()
    best_objective = current_objective
    i = 0
    while tn > tf and i < imax:
        newsolution()
        new_objective = objective()
        delta = new_objective - current_objective
        if delta < 0:
            current_solution = Output
            current_objective = new_objective
        elif random.random(0,1) < math.exp(-delta / tn) : 
            current_solution = Output
            current_objective = new_objective
        i += 1
        tn *= alpha**i
        print('Best solution:', best_solution)
        print('Best solution:', Droneinfo)
        cost.append(best_objective)


def plot_map(Droneinfo, obstlist, numdrones, numtrackp, gridsize):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define a list of colors for each drone
    colors = plt.cm.jet(np.linspace(0, 1, numdrones))

    # Plot each drone's path in a different color
    for i in range(numdrones):
        start_index = (numtrackp + 2) * i
        end_index = start_index + (numtrackp + 2)

        # Get the track points for this drone from Droneinfo
        drone_path = Droneinfo[start_index:end_index]
        xs, ys, zs = zip(*drone_path)  # Unpack into separate lists for x, y, z

        ax.plot(xs, ys, zs, color=colors[i], label=f'Drone {i + 1}', marker='o')

    # Plot obstacles
    if obstlist:
        ox, oy, oz = zip(*obstlist)
        ax.scatter(ox, oy, oz, color='red', marker='x', label='Obstacles')

    # Set axis limits based on grid size
    ax.set_xlim([0, gridsize])
    ax.set_ylim([0, gridsize])
    ax.set_zlim([0, gridsize])

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Drone Paths with Obstacles')

    plt.legend()
    plt.show()

createmap()
#print('obstlist',obstlist)
#print('Droneinfo',Droneinfo)
#print('numdrones',numdrones)
#print('numtrackp',numtrackp)
#print('Output',Output)
SA()
plot_map(Droneinfo, obstlist, numdrones, numtrackp, gridsize)
