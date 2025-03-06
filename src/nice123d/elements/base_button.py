"""
BaseButton -> ui.button

file:           nice123d/elements/base_button.py
file-id:        f87748e4-0de3-4a5e-a28c-f31abc2cf48b
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class is used for a button controlling the visibility or zoom of a connected view of the application.
    It is able to move the view from one side to the other.
"""

# [Imports]                                      #| description or links 
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from typing import Optional                      #| [docs](https://docs.python.org/3/library/typing.html)
from .constants import *

# [Main Class]
class BaseButton(ui.button):
    _sibling_button: Optional['Button'] = None
    _view: Optional['View'] = None
    
    def __init__(self, text, icon, on_click, sibling_button = None, view = None, **kwargs):
        self._sibling_button = sibling_button
        self._view = view
        # encapsulate the on_click function
        self._parent = None
        self._on_click = on_click
        self._active = False
        super().__init__(text, on_click=self.toggle_on_click, **kwargs)
        super().set_icon(icon)

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):        
        self._parent = value

    @property
    def sibling_button(self):
        return self._sibling_button
    
    @sibling_button.setter
    def sibling_button(self, value):        
        self._sibling_button = value

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, value):
        self._view = value

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value
        if value:
            self.props('fab color=active')
        else:
            self.props('fab color=default')

    def toggle_on_click(self, event=None):
        print(f'toggle_on_click {self.parent}')
        if hasattr( self._parent, 'last_button'):
            object = self._parent.last_button
            if object is not None:
                object.active = False
            self._parent.last_button = self

        if self._sibling_button is not None:
            self._sibling_button.active = False

        self.active = True
        self._on_click(event)
    
