import math
import random
import numpy
import time

import matplotlib.pyplot as plt
import matplotlib.tri as tri

import numpy as np

import json


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
        
    def get_values(self):
        return self.x, self.y

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

    def include(self, point):
        if (self.v[0] == point) or (self.v[1] == point) or (self.v[2] == point):
            return True
        return False

    def get_points(self):
        return self.v[0], self.v[1], self.v[2]



class DelaunayTriangulation:
    def __init__(self, WIDTH, HEIGHT, SuperPointA=None, SuperPointB=None, SuperPointC=None):
        self.triangulation = []

        # Declaring the super triangle coordinate information
        self.framep1 = Point(-100, -100)
        self.framep2 = Point(2 * WIDTH + 100, -100)
        self.framep3 = Point(-100, 2 * HEIGHT + 100)

        frame = Triangle(self.framep1, self.framep2, self.framep3)

        self.triangulation.append(frame)

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
            

    def get_values(self):

        ps = [p for t in self.triangulation for p in t.v]

        xs = [p.x for p in ps]
        ys = [p.y for p in ps]


        ts = [(ps.index(t.v[0]), ps.index(t.v[1]), ps.index(t.v[2])) for t in self.triangulation]

        return xs, ys, ts
    
    def remove_frame(self):
        onSuper = lambda triangle: triangle.include(self.framep1) or triangle.include(self.framep2) or triangle.include(self.framep3)

        for triangle_new in self.triangulation[:]:
            if onSuper(triangle_new):
                self.triangulation.remove(triangle_new)

def read_points_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        points = json.loads(content)
        return points

 
X_BOUND = 10000
Y_BOUND = 10000
n = 10  # n should be greater than 2

xs0 = [random.randint(1, X_BOUND - 1) for x in range(n)]
ys0 = [random.randint(1, Y_BOUND - 1) for y in range(n)]
point_list = list(zip(xs0, ys0))



# Example usage
#file_path = 'ten_thousand_points.txt'
#point_list = read_points_from_file(file_path)
start = time.time()
#print("hello")

DT = DelaunayTriangulation(X_BOUND, Y_BOUND)
i = 0
for x, y in point_list:
    DT.increment(Point(x, y))
    i += 1
    if i % 1000 == 0:
        checkpoint = time.time()
        print(i)
        print(checkpoint - start)

DT.remove_frame()
xs, ys, ts = DT.get_values()
end = time.time()
print(end - start)
fig, ax = plt.subplots()
ax.margins(0.1)
ax.set_aspect('equal')

ax.triplot(tri.Triangulation(xs, ys, ts), 'k-o')
ax.set_title('Plot of Delaunay triangulation')

plt.show()
