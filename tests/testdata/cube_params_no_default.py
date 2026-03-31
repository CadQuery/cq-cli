import cadquery as cq

# cq.cqgi.describe_parameter gives valid_values but no default_value,
# exercising the branch where param.default_value is falsy.
width = cq.cqgi.describe_parameter(1, "Width of the cube", valid_values=[1, 2, 3, 4, 5])

cube = cq.Workplane().box(width, width, width)

show_object(cube)
