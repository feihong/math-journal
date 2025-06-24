import math
from build123d import *
from ocp_vscode import *

c = Circle(2)
show(c, grid=True, position=[0, 0, 1])
print(f'Area is about 4pi: {math.isclose(c.area, 4 * math.pi)}')
