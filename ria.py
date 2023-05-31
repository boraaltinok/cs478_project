# Simple delaunay triangle generator
# Implementation of incremental Bowyer-Watson Algorithm
# This has a time complexity of O(n^2)
# Refer to the Wikipedia page of Bowyer watson algorithm as I have implemented directly from the Pseudo-code

# Author: Vignesh Rajendiran

# This is written with ease of understanding in mind. If you want elaborate code. Then visit https://github.com/ayron
# I referred to Ayrons code for inspiration. I am planning to rewrite this code as my own in the future.

# sometimes there will be a cross division error if the n>100 because of random points used and WIDTH, HEIGHT values

import math
import random
import numpy

import matplotlib.pyplot as plt
import matplotlib.tri as tri

import numpy as np


def is_legal(line1, line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def circumcircle(self, T):

        a_x = T.v[0].x
        a_y = T.v[0].y

        b_x = T.v[1].x
        b_y = T.v[1].y

        c_x = T.v[2].x
        c_y = T.v[2].y

        # The point coordinates

        d_x = self.x
        d_y = self.y

        # If the following determinant is greater than zero then point lies inside circumcircle
        incircle = np.array([[a_x - d_x, a_y - d_y, (a_x - d_x) ** 2 + (a_y - d_y) ** 2],
                             [b_x - d_x, b_y - d_y, (b_x - d_x) ** 2 + (b_y - d_y) ** 2],
                             [c_x - d_x, c_y - d_y, (c_x - d_x) ** 2 + (c_y - d_y) ** 2]])

        if np.linalg.det(incircle) > 0:
            return True
        else:
            return False


class Triangle:
    def __init__(self, a, b, c):
        self.v = [None] * 3
        self.v[0] = a
        self.v[1] = b
        self.v[2] = c

        self.edges = [[self.v[0], self.v[1]],
                      [self.v[1], self.v[2]],
                      [self.v[2], self.v[0]]]

        self.neighbour = [None] * 3



class DelaunayTriangulation:
    def __init__(self, WIDTH, HEIGHT):
        self.triangulation = []

        # Declaring the super triangle coordinate information
        self.SuperPointA = Point(-100, -100)
        self.SuperPointB = Point(2 * WIDTH + 100, -100)
        self.SuperPointC = Point(-100, 2 * HEIGHT + 100)

        superTriangle = Triangle(self.SuperPointA, self.SuperPointB, self.SuperPointC)

        self.triangulation.append(superTriangle)

    def increment(self, p):

        bad_triangles = []

        for triangle in self.triangulation:
            # Check if the given point is inside the circumcircle of triangle
            if p.circumcircle(triangle):
                # If it is then add the triangle to bad triangles
                bad_triangles.append(triangle)

        polygon = []

        # Routine is to find the convex hull of bad triangles
        # This involves a naive search method, which increases the time complexity
        for current_triangle in bad_triangles:
            for this_edge in current_triangle.edges:
                isNeighbour = False
                for other_triangle in bad_triangles:
                    if current_triangle == other_triangle:
                        continue
                    for that_edge in other_triangle.edges:
                        if is_legal(this_edge, that_edge):
                            isNeighbour = True
                if not isNeighbour:
                    polygon.append(this_edge)

        # Delete the bad triangles
        for each_triangle in bad_triangles:
            self.triangulation.remove(each_triangle)

        # Re-triangle the convex hull using the given point
        for each_edge in polygon:
            newTriangle = Triangle(each_edge[0], each_edge[1], p)
            self.triangulation.append(newTriangle)
    
X_BOUND = 1000
Y_BOUND = 1000
n = 20  # n should be greater than 2

xs = [random.randint(1, X_BOUND - 1) for x in range(n)]
ys = [random.randint(1, Y_BOUND - 1) for y in range(n)]
zs = [0 for z in range(n)]

DT = DelaunayTriangulation(X_BOUND, Y_BOUND)
for x, y in zip(xs, ys):
    DT.increment(Point(x, y))

# Remove the super triangle on the outside

# Helps in determining the neighbours of triangles. I felt it might help in the future


# Creating a Triangulation without specifying the triangles results in the
# Delaunay triangulation of the points.

# Create the Triangulation; no triangles so Delaunay triangulation created.
triang = tri.Triangulation(xs, ys)

# Plot the triangulation.
fig, ax = plt.subplots()
ax.margins(0.1)
ax.set_aspect('equal')
ax.triplot(triang, 'bo-')

# print(XS)
# print(YS)
# print(TS)

ax.set_title('Plot of Delaunay triangulation')

plt.show()