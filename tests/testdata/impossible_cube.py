import cadquery as cq

box = cq.Workplane().box(10, 10, 10).edges().fillet(400.0)

show_object(box)
