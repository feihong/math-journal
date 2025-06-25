import math
from build123d import *
from ocp_vscode import *

pi = math.pi

c1 = Circle(1)
c2 = Circle(2) - Circle(1)
c3 = Circle(3) - Circle(2)
c4 = Circle(4) - Circle(3)
show(c1, c2, c3, c4, grid=True, position=[0, 0, 1],
     colors=['red', 'yellow', 'green', 'blue'])

print(f'Areas: {c1.area / pi}, {c2.area / pi}, {c3.area / pi}, {c4.area / pi}')
print(f'r4/r1 = {4/1}')
