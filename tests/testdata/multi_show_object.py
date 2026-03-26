import cadquery as cq

# This file calls show_object() multiple times (multiple results).
cube = cq.Workplane().box(1, 1, 1)
sphere = cq.Workplane().sphere(0.5)

show_object(cube)
show_object(sphere)
