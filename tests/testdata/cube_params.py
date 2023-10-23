import cadquery as cq

width = 1
tag_name = "cube"
centered = True

cube = cq.Workplane().box(width, width, width, centered).tag(tag_name)

show_object(cube)
