from build123d import *
from ocp_vscode import *

class Par:
    a = 12 
    w = 2 
    b = 24
    c = 4
    box = "A"
    color = "#440000"
# TEST
# Create a new part
inner = Box( Par.a - Par.w, Par.b- Par.w, 2*Par.c)
inner.name = 'inner'
main = Box( Par.a, Par.b, Par.c) \
      - inner
main.name = Par.box 
main.color = Par.color

show(main, inner)

