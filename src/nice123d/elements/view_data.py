"""
ViewData

file:           nice123d/elements/view_data.py
file-id:        14b7cc70-52af-4828-8e13-9ac9655d7e88
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class stores the data for all views.
"""
# [Imports]
from nicegui import ui
from typing import Callable, Optional, Tuple

# [Variables]

# [Main Class]
class ViewData:
    """
    A class for managing the view data.
    """
    def __init__(self, title: str, icon: str, position: Tuple[bool, bool], short_cut: str = ""):

        # - Type checks:
        if title == "":
            raise ValueError("The title must not be empty.")
        elif type(title) is not str:
            raise TypeError("The title must be a string.")
        if icon == "":
            raise ValueError("The icon must not be empty.")
        elif type(icon) is not str:
            raise TypeError("The icon must be a string (name of material icon).")
        elif icon.find(" ") != -1:
            print("Warning: The icon name contains spaces. Replacing spaces with underscores.")
            icon = icon.replace(" ", "_")

        # - Assigning values:
        self.title: str = title
        self.icon: str = icon
        self.is_left: bool = position[0]
        self.is_right: bool = position[1]
        self.short_cut: str = short_cut
        self.view: Optional[str] = None
        self.button_left: Optional[ui.button]  = None
        self.button_right: Optional[ui.button] = None

    def __str__(self):
        return f'''- title: {self.title}'''

