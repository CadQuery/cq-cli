import cadquery as cq

# This test file contains a method for creating a shape, but does not contain
# any top-level `show_object()` calls.


def cube():
    return cq.Workplane().box(1, 1, 1)
