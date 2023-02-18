import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib as mpl
from scipy.integrate import solve_ivp
import random

# Plot settings
ax = plt.axes()
colormap = plt.get_cmap('hsv')
norm = mpl.colors.Normalize(0.0, 2*np.pi)

f = open("lpsP3Q13.txt", "r")

# Number of nodes in a cycle
n= int(f.readline().split()[1])

# Setting initial phase of nodes
theta = np.zeros(n)
for i in range(n):
    theta[i] = random.uniform(0,2*np.pi)
    # theta[i] = i*2*np.pi/n #+ 1.3/(i+1)

# Positioning the nodes in a circle
x = np.zeros(n)
y = np.zeros(n)
for i in range(n):
    x[i] = 1000*np.cos(2*i*np.pi/n)
    y[i] = 1000*np.sin(2*i*np.pi/n)

# Adjacency matrix
A = np.empty(n, dtype=object)
for i in range(n):
    A[i] = []
a = f.readline().split()
edges = []
while int(a[1]) != -1:
    A[int(a[1])-1].append(int(a[2]) - 1)
    A[int(a[2])-1].append(int(a[1]) - 1)
    a = f.readline().split()
    edges.append([int(a[1])-1,int(a[2])-1]) 
edges = np.array(edges)

# Solving system of ODEs
def sysOde(t,thet):
    ret = []
    for i in range(n):
        tmp = 0
        for j in range(len(A[i])):
            tmp -= np.sin(thet[i]-thet[A[i][j]])
            # print(f"np.sin(thet[{i}]-thet[{A[i][j]}])",end=" ")
        # print("")
        ret.append(tmp)
    return ret

ts = np.linspace(0,50,500)
sol = solve_ivp(sysOde,(0,50),theta,t_eval=ts)

# Animation settings
def animate(t):
    tmp = np.zeros(n)
    for i in range(n):
        tmp[i] = sol.y[i][t]%(2*np.pi)
    plt.cla()
    ax.scatter(x,y,s=200,c=tmp,cmap=colormap,norm=norm,zorder=10)
    ax.plot(x[edges.T], y[edges.T], linestyle='-', color='black',linewidth =1) 

# Plotting    
# ani = FuncAnimation(plt.gcf(), animate, interval = 150)
plt.plot(sol.t,np.mod(sol.y.T,2*np.pi))
plt.title("Phases of each node")
plt.xlabel("Time")
plt.ylabel("Phase in radians")
plt.show()