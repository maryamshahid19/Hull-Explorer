import random                               #Used in code to generate random numbers
import matplotlib.pyplot as plt             #Used to plot graphs
import matplotlib.animation as animation    #Used to change plotting in graphs over time
import tkinter as tk                        #Used in the code for GUI
from tkinter import ttk, simpledialog       #Used to pop-up input dialogue for taking input from user

Point = complex
P = Point

# returns x-coordinate of point
def X(point):
    if isinstance(point, P):
        return point.real
    else:
        return 0

# returns y-coordinate of point
def Y(point):
    if isinstance(point, P):
        return point.imag
    else:
        return 0

# To generate random points
def Points(n, width=900, height=600, seed=42):
    random.seed(seed * n)       #If we input same no.of points than same set of random points will be generated everytime
    return frozenset(P(random.randrange(width), random.randrange(height))
                     for c in range(n))

def convert_points_into_list(points):
    return list(points)

# tells if a specific point is ccw or not
def ccw(p, q, r):
    val = (Y(q) - Y(p)) * (X(r) - X(q)) - (X(q) - X(p)) * (Y(r) - Y(q))
    if val == 0:
        return 0  # Collinear
    elif val > 0:
        return 1  # Clockwise
    else:
        return -1  # Counter Clock Wise

def brute_force(points):
    n = len(points)
    if n < 3:
        raise ValueError("Convex Hull requires minimum 3 points")

    for i in range(n):
        for j in range(n):
            if j != i:
                pi, pj = points[i], points[j]
                valid = True

                for k in range(n):
                    if k != i and k != j:
                        pk = points[k]
                        if ccw(pi, pj, pk) != -1:
                            valid = False  # pk is not ccw to pi and pj
                            break

                if valid:
                    if pi not in convex_hull:
                        convex_hull.append(pi)
                    if pj not in convex_hull:
                        convex_hull.append(pj)
                    lines.append([(X(pi), Y(pi)), (X(pj), Y(pj))])      #to keep track of two valid points in each iteration that will connect eachother 
                                                                        #otherwise convex hull will connect randomly with any of the convex hull points

# Animation function for displaying graph
def update(frame):
    ax.clear()

    # Plots all points
    ax.scatter(*zip(*[(X(p), Y(p)) for p in points_list]), color='black', label='All Points')

    # Plot lines connecting valid points pi and pj acc to convex hull for each iteration
    for i in range(frame + 1):
        if i < len(lines):
            line = lines[i]
            plt.scatter([line[0][0], line[1][0]], [line[0][1], line[1][1]], color='red', s=100)
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color='red', linestyle="--")

    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Brute Force Convex Hull - Iteration {frame + 1}\nTime Complexity - O(n^3)')
    plt.pause(0.5)


root = tk.Tk()
root.withdraw()  

num_points = simpledialog.askinteger("Input", "Enter the number of points:")
points = Points(num_points)
points_list = convert_points_into_list(points)


fig, ax = plt.subplots()
convex_hull = []
lines = []
brute_force(points_list)

# To run the animation
ani = animation.FuncAnimation(fig, update, frames=len(lines), repeat=True)
plt.show()

