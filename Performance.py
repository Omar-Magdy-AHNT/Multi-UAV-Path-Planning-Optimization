from GA import Const1 
from GA import Const2
from GA import Const3
from GA import Const4
from GA import Data
from GA import OF1
from GA import OF2
from GA import milestone4 as GA
from SA import *
from SA import milestone3 as SA

import numpy as np


it = 10 #Number of runs to get performance statistics

def comparison():
    # GA
    GAfit = []
    for i in range(it):
        out,ct = GA.run()
        GAfit.append(ct)
        if i == 0:
            GA_best = out
            GA_ct = ct
        elif out < GA_best:
            GA_best = out
            GA_ct = ct
    # SA
    SAfit = []
    for i in range(it):
        out,ct = SA.run()
        SAfit.append(ct)
        if i == 0:
            SA_best = out
            SA_ct = ct
        elif out < SA_best:
            SA_best = out
            SA_ct = ct

    # Performance statistics
    GAavg = sum(GAfit)/it
    GAstd = np.std(GAfit)
    SAavg = sum(SAfit)/it
    SAstd = np.std(SAfit)
    return GA_best, GA_ct, GAavg, GAstd, SA_best, SA_ct, SAavg, SAstd

Optimal_Solution_GA, Optimal_Fitness_Value_GA,\
Mean_Fitness_GA, Standard_Deviation_GA, Optimal_Solution_SA,\
Optimal_Fitness_Value_SA, Mean_Fitness_SA, Standard_Deviation_SA = comparison()

if Optimal_Fitness_Value_GA < Optimal_Fitness_Value_SA:
    print("GA Has The Best Optimal Value" , Optimal_Fitness_Value_GA)
    print("Optimal Solution: ", Optimal_Solution_GA)
else:
    print("SA Has The Best Optimal Value" , Optimal_Fitness_Value_SA)
    print("Optimal Solution: ", Optimal_Solution_SA)
    
if Mean_Fitness_GA < Mean_Fitness_SA:
    print("GA Has The Best Mean Value" , Mean_Fitness_GA)
else:
    print("SA Has The Best Mean Value" , Mean_Fitness_SA)

if Standard_Deviation_GA < Standard_Deviation_SA:
    print("GA Has The Best Standard Deviation Value" , Standard_Deviation_GA)
else:
    print("SA Has The Best Standard Deviation Value" , Standard_Deviation_SA)
