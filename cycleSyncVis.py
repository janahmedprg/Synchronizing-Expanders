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

# Number of nodes in a cycle
n=4

# Setting initial phase of nodes
theta = np.zeros(n)
for i in range(n):
    # theta[i] = random.uniform(0,2*np.pi)
    theta[i] = i*2*np.pi/n #+ 1.3/(i+1)

# Positioning the nodes in a circle
x = np.zeros(n)
y = np.zeros(n)
for i in range(n):
    x[i] = 3*np.cos(2*i*np.pi/n)
    y[i] = 3*np.sin(2*i*np.pi/n)

# Setting up edges
edges = np.zeros((n,2),dtype=np.int8)
for i in range(n):
    edges[i][0] = int(i)
    edges[i][1] = int((i+1)%n)

# Solving system of ODEs
def sysOde(t,thet):
    ret = []
    for i in range(n):
        ret.append(2-(np.sin(thet[i]-thet[(i+1)%n])+np.sin(thet[i]-thet[i-1])))
        # print(f"2-(np.sin(thet[{i}]-thet[{(i+1)%n}])+np.sin(thet[{i}]-thet[{i-1}]))",i)
    return ret

ts = np.linspace(0,50,300)
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
ani = FuncAnimation(plt.gcf(), animate, interval = 150)
# plt.plot(sol.t,sol.y.T)
plt.show()