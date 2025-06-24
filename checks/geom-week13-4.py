import math
from build123d import *
from ocp_vscode import *

with BuildSketch() as blue:
    with BuildLine():
        a = CenterArc((3, 0), 3, 0, 180)
        b = CenterArc((11, 0), 5, 0, 180)
        c = CenterArc((8, 0), 8, 0, 180)
    make_face()

show(blue, colors=['blue'], grid=True, position=[0, 0, 1], quaternion=[0, 0, 0, 1])
print(f'Blue region has an area of 15pi: {math.isclose(blue.sketch.area, 15*math.pi)}')
