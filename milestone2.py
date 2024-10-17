import random
import numpy

numdrones = 2
numtrackp = 2 
obstnum = random.randint(0, 8)
obstlist = []
distDrone = []
gridsize = 10
dsafe = 1
amax = 75 *numpy.pi/180
bmax = 60 *numpy.pi/180
Output = []
danger = []
def createobs():
    for i in range(obstnum): 
        x = random.randint(0, gridsize)
        y = random.randint(0, gridsize) 
        z = random.randint(0, gridsize)
        obstlist.append((x,y,z))

def createarray():
    matrix = []
    for i in range(numdrones):
        startpt=(0,i,0)
        endpt=(10,10-i,10)
        matrix.append(startpt)
        for j in range(numtrackp):
            x = random.randint(0, gridsize)
            y = random.randint(0, gridsize)
            z = random.randint(0, gridsize)
            matrix.append((x,y,z))
            Output.append((x,y,z))
        matrix.append(endpt)
    return matrix


def func1():
    for i in range(numdrones):
        tdist = 0
        for j in range(numtrackp+1):
            x = Droneinfo[(i*4)+j][0]
            y = Droneinfo[(i*4)+j][1]
            z = Droneinfo[(i*4)+j][2]
            x1 = Droneinfo[(i*4)+j+1][0]
            y1 = Droneinfo[(i*4)+j+1][1]
            z1 = Droneinfo[(i*4)+j+1][2]
            tdist = tdist + (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
            if(j==(len(Droneinfo))-1):
                break
        distDrone.append(tdist)


def func2():
    b=0
    for i in range(numdrones):
        totaldanger = 0
        for j in range(numtrackp):
            x = Droneinfo[j+(i*4)][0]
            y = Droneinfo[j+(i*4)][1]
            z = Droneinfo[j+(i*4)][2]
            b = 0
            for k in range(obstnum):
                x1 = obstlist[k][0]
                y1 = obstlist[k][1]
                z1 = obstlist[k][2]
                dist = (((x-x1)**2 )+ ((y-y1)**2) + ((z-z1)**2))**0.5
                b = b + (dsafe/dist)**2  
            totaldanger = totaldanger + b          
        danger.append(totaldanger)

def constraint1():
    for j in range(numdrones):
        for i in range(numtrackp):
            xm = Droneinfo[i+(j*4)][0]
            ym= Droneinfo[i+(j*4)][1]
            zm = Droneinfo[i+(j*4)][2]
            x = Droneinfo[i+1+(j*4)][0]
            y= Droneinfo[i+1+(j*4)][1]
            z = Droneinfo[i+1+(j*4)][2]
            x1 = Droneinfo[i+2+(j*4)][0]
            y1= Droneinfo[i+2+(j*4)][1]
            z1 = Droneinfo[i+2+(j*4)][2]
            L1 = ((xm-x)**2 + (ym-y)**2 + (zm-z)**2)**0.5
            L2 = ((x-x1)**2 + (y-y1)**2 + (z-z1)**2)**0.5
            L3 = ((xm-x1)**2 + (ym-y1)**2 + (zm-z1)**2)**0.5
            a = numpy.arccos((L1**2 + L2**2 - L3**2)/(2*L1*L2))
            if a>amax:
                return False
    return True

def constraint2():
    for j in range(numdrones):
        for i in range(numtrackp+1):
            x = Droneinfo[i+(j*4)][0]
            y= Droneinfo[i+(j*4)][1]
            z = Droneinfo[i+(j*4)][2]
            x1 = Droneinfo[i+1+(j*4)][0]
            y1= Droneinfo[i+1+(j*4)][1]
            z1 = Droneinfo[i+1+(j*4)][2]
            H = z1-z
            L = ((x-x1)**2 + (y-y1)**2)**0.5
            if L == 0:
                b=0
            else:
                b = numpy.arctan(H/L)
            if b>bmax:
                return False    
    return True

def constraint3():
    for i in range(len(Droneinfo)):
        p = Droneinfo[i]
        for j in range(obstnum):
            p1 =obstlist[j]
            if ((p[0] == p1[0]) & (p[1] == p1[1]) & (p[2] == p1[2])):
                return False
    for i in range(len(Droneinfo)):
        p = Droneinfo[i]
        for j in range(len(Droneinfo)):
            if i == j:
                continue
            p1 = Droneinfo[j]
            if ((p[0] == p1[0] )&(p[1] == p1[1] )& (p[2] == p1[2])):
                return False
    return True

Droneinfo = createarray()
#Droneinfo =  [(0, 0, 0), (0,1, 10), (3 ,1, 0), (10, 10, 10), (0, 1, 0), (9, 2, 9), (2, 5, 3), (10, 9, 10)]
print ("info", Droneinfo)
createobs()
func1()
print ("dist" , distDrone)
print ("constraint1", constraint1())
print ("constraint2", constraint2())
print ("constraint3", constraint3())
func2()
print ("danger", danger)
print ("Obs", obstlist)
print ("Output", Output)