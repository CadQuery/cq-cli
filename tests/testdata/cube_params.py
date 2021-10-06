import cadquery as cq

width = 1

cube = cq.Workplane().box(width, width, width)

show_object(cube)