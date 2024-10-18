from Const1 import *
from Const2 import *
from Const3 import *
from Const4 import Trackpointlinevalid
from Const5 import *
from Data import *
from OF1 import *
from OF2 import *
import math
import numpy

T0 =100
Tf = 1
imax = 3
alpha = 0.95
createarray()

def objective(Droneinfo):
    distDrone.clear()
    danger.clear()
    func1()
    func2()
    total_distance = sum(distDrone)
    total_danger = sum(danger)
    obj = total_distance + 10*total_danger
    return obj

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

    print('Best solution:', best_solution)


