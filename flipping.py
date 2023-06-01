import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json
import time

def voronoi(points):
    # Perform Delaunay triangulation
    tri = Delaunay(points)

    # Get the edges and triangles of the Delaunay triangulation
    edges = set()
    triangles = set()

    for simplex in tri.simplices:
        triangles.add(tuple(sorted(simplex)))

        for i in range(3):
            edge = tuple(sorted((simplex[i], simplex[(i + 1) % 3])))
            edges.add(edge)

    # Flip edges until we obtain the Voronoi Diagram
    while edges:
        edge = edges.pop()
        if edge not in edges:
            continue

        i, j = edge
        triangles_with_edge = []

        for triangle in triangles:
            if i in triangle and j in triangle:
                triangles_with_edge.append(triangle)

        if len(triangles_with_edge) != 2:
            continue

        # Get the vertices of the two triangles sharing the edge
        triangle1, triangle2 = triangles_with_edge
        k = [vertex for vertex in triangle1 + triangle2 if vertex != i and vertex != j]

        if len(k) != 2:
            continue

        # Check if the circumcircle of the triangles is empty
        a, b, c = points[i], points[j], points[k[0]]
        d = np.dot(np.linalg.inv(np.vstack((a - b, b - c))), np.array([np.dot(a, a) - np.dot(b, b), np.dot(b, b) - np.dot(c, c)])) / 2.0

        if np.any(np.isnan(d)):
            continue

        circumcenter = np.dot(np.vstack((a, b, c)), d)
        radius = np.linalg.norm(a - circumcenter)

        if radius > np.linalg.norm(points[k[1]] - circumcenter):
            continue

        # Flip the edge and update the triangulation
        triangles.remove(triangle1)
        triangles.remove(triangle2)
        edges.remove(edge)

        new_triangles = [(i, j, k[0]), (i, j, k[1])]
        new_edges = [(i, k[0]), (i, k[1]), (j, k[0]), (j, k[1])]

        for new_triangle in new_triangles:
            triangles.add(tuple(sorted(new_triangle)))

            for i in range(3):
                new_edge = tuple(sorted((new_triangle[i], new_triangle[(i + 1) % 3])))
                edges.add(new_edge)

        for new_edge in new_edges:
            edges.discard(new_edge)

    return triangles

def plot_voronoi(points, triangles):
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the input points
    ax.plot(points[:, 0], points[:, 1], 'ko')

    # Plot the Voronoi edges as polygons
    for triangle in triangles:
        vertices = points[list(triangle)]
        polygon = Polygon(vertices, fill=False)
        ax.add_patch(polygon)

    # Set plot limits and labels
    ax.set_xlim([np.min(points[:, 0])-1, np.max(points[:, 0])+1])
    ax.set_ylim([np.min(points[:, 1])-1, np.max(points[:, 1])+1])
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Show the plot
    plt.show()

# Example usage:
def read_points_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        points = json.loads(content)
        return points
file_path = 'thousand_points.txt'
point_list = np.array(read_points_from_file(file_path))
start = time.time()

print("hello"),
vd = voronoi(point_list)
end = time.time()
print(end - start)
plot_voronoi(point_list, list(vd))