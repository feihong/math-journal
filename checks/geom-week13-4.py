import math
from build123d import *
from ocp_vscode import *

lines = Curve() + [
    CenterArc((3, 0), 3, 0, 180),
    CenterArc((11, 0), 5, 0, 180),
    CenterArc((8, 0), 8, 0, 180),
]
region = make_face(lines)

show(region, colors=['blue'], grid=True, reset_camera=Camera.CENTER)
print(f'Blue region has an area of 15pi: {math.isclose(region.area, 15*math.pi)}')
