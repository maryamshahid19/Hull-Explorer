import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import ttk, simpledialog
import tkinter as tk

Point = complex
P = Point

def X(point):
    if isinstance(point, P):
        return point.real
    else:
        return 0

def Y(point):
    if isinstance(point, P):
        return point.imag
    else:
        return 0

def distance(A, B):
    return abs(A - B)

# To generate random points
def Points(n, width=900, height=600, seed=42):
    random.seed(seed * n)       
    return frozenset(P(random.randrange(width), random.randrange(height))
                     for c in range(n))

def convert_points_into_list(points):
    return list(points)

def ccw(p, q, r):
    val = (Y(q) - Y(p)) * (X(r) - X(q)) - (X(q) - X(p)) * (Y(r) - Y(q))
    if val == 0:
        return 0  # Collinear
    elif val > 0:
        return 1  # Clockwise
    else:
        return -1  # Counter Clock Wise

def jarvis_march(points):
    n = len(points)
    if n < 3:
        raise ValueError("Convex hull requires minimum 3 points")

    hull = []

    # To find the point with the smallest y-coordinate or leftmost if two points have same y coordinate
    start_point = min(points, key=lambda p: (Y(p), X(p)))
    current_point = start_point

    while True:
        hull.append(current_point)
        next_point = points[0]

        for pi in points[1:]:
        
            result = ccw(current_point, next_point, pi)

            # Incase if the current_point, next_point, pi are collinear and pi is closer to current point than take pi as the next point that will be part of convex hull
            if result == -1 or (result == 0 and distance(current_point, next_point) < distance(current_point, pi)):
                next_point = pi

        if next_point == start_point:
            break  # Convex hull is complete
        else:
            current_point = next_point

    return hull

def update(frame):
    ax.clear()

    # Plot all points
    ax.scatter(*zip(*[(X(p), Y(p)) for p in points]), color='black', label='All Points')

    # Plot the convex hull points
    hull_points = convex_hull[:frame + 1]
    ax.scatter(*zip(*[(X(p), Y(p)) for p in hull_points]), color='red', s=100, label='Convex Hull Points')
    ax.plot(*zip(*[(X(p), Y(p)) for p in hull_points]), color='red', linestyle='--')

    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Jarvis March Convex Hull - Iteration {frame+1}\nTime Complexity - O(nh)')
    plt.pause(0.5)

# Example to run program
root = tk.Tk()
root.withdraw()  # To Hide the main window

num_points = simpledialog.askinteger("Input", "Enter the number of points:")
points = Points(num_points)
points_list = convert_points_into_list(points)

# To find the convex hull
fig, ax = plt.subplots()
convex_hull= jarvis_march(points_list)
convex_hull.append(convex_hull[0])  # Close the convex hull

# To run the animation
ani = animation.FuncAnimation(fig, update, frames=len(convex_hull), repeat=True)
plt.show()
