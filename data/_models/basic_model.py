from build123d import *
from ocp_vscode import *

# a

with BuildPart() as main:
    Box(10, 20, 30)
    Cylinder(10, 20, mode=Mode.SUBTRACT)

main.part.color = "#FF2244EE"
main.part.name = "main"

with BuildPart() as second:
    Sphere(9)
    Cylinder(5, 10, mode=Mode.SUBTRACT)

second.part.color = "#4422FFEE"
second.part.name = "second"


show(main.part, second.part)