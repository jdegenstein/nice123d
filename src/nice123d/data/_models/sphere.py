from build123d import *
from ocp_vscode import *

class Par:
    a = 10 
    w = 2 
    b = 24
    c = 4
    box = "A"
    color = "#440000"
# TEST

try: 
    # Create a new part
    inner = Box( Par.a - Par.w, Par.b- Par.w, 2*Par.c)
    inner.name = 'inner'
    main = Sphere( Par.a) \
          - inner
    main.name = Par.box 
    main.color = Par.color
except e:
    print(f"{e=}")
    
show(main, inner)

