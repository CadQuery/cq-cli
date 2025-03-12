import cadquery as cq

# print info about the __file__ variable to stdout so the test can check it
if '__file__' in locals():
    print(f"__file__={__file__}")
else:
    print("__FILE__ not set")

# render a simple shape so the cq-cli invocation succeeds
b = cq.Workplane("XY").rect(10, 10).extrude(10)
show_object(b)
