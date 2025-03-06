"""
Constants

file:           nice123d/elements/constants.py
file-id:        0254fdeb-5b0f-4a87-8067-d19e1368cc04
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class defines the constants for the applications.
"""

# [Imports]                                      #|
from enum import Enum  # | [docs](https://docs.python.org/3/library/enum.html)
import platform  # | [docs](https://docs.python.org/3/library/platform.html)


# [Types]
class Side(Enum):
    """
    Enum for defining the side in the view.
    """

    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3


# [Constants]
Yes = True
No = False

active_os = platform.system()  # get the operating system

# TODO: check if still used
left = True, False
right = False, True
both = True, True
none = False, False

# [Parameters]
P__experimental = No # or Yes
P__experimental_splitter = No
P__use_splitter_buttons = No