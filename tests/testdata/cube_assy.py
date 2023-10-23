import cadquery as cq

assy = cq.Assembly()
assy.add(cq.Workplane().box(10, 10, 10))
assy.add(cq.Workplane().box(10, 10, 10), loc=cq.Location((5, 5, 0)))

show_object(assy)
