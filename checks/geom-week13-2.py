import math
from build123d import *
from ocp_vscode import *

with BuildSketch() as sector:
    with BuildLine():
        o = (0, 0)
        a = CenterArc(o, 12, 0, 150)
        Line(a @ 0, o)
        Line(o, a @ 1)
    make_face()

show(sector, grid=True, position=[0, 0, 1], quaternion=[0, 0, 0, 1])
print(f'Circle sector has an area of 60pi: {math.isclose(sector.sketch.area, 60*math.pi)}')
