from foronoi import Voronoi, Polygon, Visualizer, VoronoiObserver

# Define some points (a.k.a sites or cell points)
points = [
    (2.5, 2.5),
    (4, 7.5),
    (7.5, 2.5),
    (6, 7.5),
    (4, 4),
]

# Define a bounding box / polygon
polygon = Polygon([
    (2.5, 10),
    (5, 10),
    (10, 5),
    (10, 2.5),
    (5, 0),
    (2.5, 0),
    (0, 2.5),
    (0, 5),
])

# Initialize the algorithm
v = Voronoi(polygon)

# Attach a Voronoi Observer that monitors and visualizes the construction of 
# the Voronoi Diagram step-by-step. See for more information 
# examples/quickstart.py or examples/observers.py.
v.attach_observer(VoronoiObserver())

# Create the diagram
v.create_diagram(points=points)

# Get properties. See more examples in examples/quickstart.py
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points

# Plotting
# Note: plot_border_to_site() indicates with dashed line to which site a border 
# belongs. The site's first edge is colored green.
Visualizer(v, canvas_offset=1)\
    .plot_sites(show_labels=True)\
    .plot_edges(show_labels=False)\
    .plot_vertices()\
    .show()