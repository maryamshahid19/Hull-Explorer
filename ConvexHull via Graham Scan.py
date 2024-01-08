import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk, simpledialog
import cmath               #Used for polar angle calculation

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

# generate random points
def Points(n, width=900, height=600, seed=42):
    random.seed(seed * n)       
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

def graham_scan(points):
    n = len(points)
    if n < 3:
        raise ValueError("Convex Hull requires minimum 3 points")

    # To Find the point with the minimum y-coordinate (or leftmost if 2 are same)
    start_point = min(points, key=lambda p: (Y(p), X(p)))

    # To Sort the points based on polar angle wrt the start_point
    sorted_points = sorted(points, key=lambda p: (cmath.phase(p - start_point), -abs(p - start_point)))

    # To push p0, p1, p2 in stack
    convex_hull_stack = [start_point, sorted_points[0], sorted_points[1]]

    # Iterate through the remaining sorted points and update the convex hull
    for i in range(2, n):
        while len(convex_hull_stack) > 1 and ccw(convex_hull_stack[-2], convex_hull_stack[-1], sorted_points[i]) != -1:
            convex_hull_stack.pop()
        convex_hull_stack.append(sorted_points[i])

        if(i==n-1):
            convex_hull_stack.append(sorted_points[0])

    return convex_hull_stack

# Animation function for displaying graph
def update(frame):
    ax.clear()

    # To plot all points in graph
    ax.scatter(*zip(*[(X(p), Y(p)) for p in points]), color='black', label='All Points')

    # To plot the convex hull points in graph
    hull_points = convex_hull_stack[:frame + 1]
    ax.scatter(*zip(*[(X(p), Y(p)) for p in hull_points]), color='red', s=100)
    ax.plot(*zip(*[(X(p), Y(p)) for p in hull_points]), color='red', linestyle='--', label='Convex Hull')

    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Graham Scan Convex Hull - Iteration {frame+1}\n Time Complexity - O(nlogn)')
    plt.pause(0.5)

# Example to run program:
root = tk.Tk()
root.withdraw()  # To Hide the main window

num_points = simpledialog.askinteger("Input", "Enter the number of points:")
points = Points(num_points)
points_list = convert_points_into_list(points)

# To find the convex hull
fig, ax = plt.subplots()
convex_hull_stack = graham_scan(points_list)
convex_hull_stack.append(convex_hull_stack[0])  # Close the convex hull

# To run the animation
ani = animation.FuncAnimation(fig, update, frames=len(convex_hull_stack) - 1, repeat=True)
plt.show()
