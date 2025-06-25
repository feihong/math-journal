from math import sqrt, cos, sin, pi, isclose
from build123d import *
from ocp_vscode import *

r = sqrt(9 / 2 / (1 - cos(2*pi/7)))
print(f'Radius of heptagon = {r}')

heptagon = RegularPolygon(r, 7)

circles =  [Pos(v.X, v.Y) * Circle(2) for v in heptagon.vertices()]
# Add 2.2 to radius based on experimentation
walkway = fillet(RegularPolygon(r + 2.2, 7).vertices(), 2) - heptagon

show_list = [
    heptagon,
    # Circle(r),
    walkway,
    # *circles,
]

show(*show_list, transparent=True, grid=True, reset_camera=Camera.CENTER,
     colors=['red', 'green', 'blue'])
print(f'Walkway has an area of {walkway.area}')
