"""
BaseButtonBar -> ui.element 
 +-> ui.button_group

file:           nice123d/base_button_bar.py
file-id:        77550f13-5b5d-4f7a-a9e7-3fb960f658e2
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class is used for a button bar controlling the view of the application on a specific panel.
"""

# [Imports]                                      #| description or links 
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from typing import Optional                      #| [docs](https://docs.python.org/3/library/typing.html)
from .constants import *
from .base_button import BaseButton
# [Main Class]
class BaseButtonBar(ui.element):
    _sibling_button: Optional['Button'] = None
    _view: Optional['View'] = None
    _last_button: Optional['BaseButton'] = None
    _created = False
    
    def __init__(self, icon, sibling_button_bar = None, view = None, on_click = None, **kwargs):
        self._button_bar = None
        self._sibling_button_bar = None
        self._icon = icon
        self._view = view
        self._buttons = [] # Stores the order
        self._map_to_view = {} # Maps the views title to the button
        # encapsulate the on_click function
        
        self._on_click = on_click
        self._buttons = []
        super().__init__(**kwargs)
    
    def add(self, button: BaseButton, title : str):
        if button not in self._buttons:
            self._buttons.append(button)
            self._map_to_view[title] = button
            button.parent = self

    def create(self):
        if self._created:
            print(f'Button bar {self._icon} already created!')
            return
        self._created = True

        with self:
            with ui.row():
                if self._icon:
                    ui.icon(self._icon)
                self._button_group = ui.button_group()
                for button in self._buttons:
                    button.move(self._button_group)

    def set_active_button(self, title: str):
        if not title in self._map_to_view.keys():
            print(f'Button {title} not found in {self._icon} button bar!')
            return
        
        if self._last_button:
            self._last_button.active = False
        button = self._map_to_view[title]
        button.active = True
        self._last_button = button

    @property
    def last_button(self):
        return self._last_button

    @last_button.setter
    def last_button(self, button):
        self._last_button = button

    @property
    def sibling_button_bar(self):
        return self._sibling_button_bar
    
    @sibling_button_bar.setter
    def sibling_button_bar(self, value):        
        self._sibling_button_bar = value

    @property
    def view(self):
        return self._view
    
    @view.setter
    def set_view(self, value):
        self._view = value

