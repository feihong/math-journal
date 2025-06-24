import math
from build123d import *
from ocp_vscode import *

o = (0, 0)
a = CenterArc(o, 12, 0, 150) # semicircle
l1 = Line(a @ 0, o)
l2 = Line(o, a @ 1)

lines = Curve() + [a, l1, l2]
sector = make_face(lines)
show(sector, grid=True, reset_camera=Camera.CENTER)

print(f'Circle sector has area = 60pi: {math.isclose(sector.area, 60*math.pi)}')
