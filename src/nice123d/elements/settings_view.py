"""
SettingsView -> BaseView -> ui.element

file:           nice123d/elements/settings_view.py
file-id:        0561e45d-2fc2-41ed-b5b2-b07db7977885
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the application settings editor.
    It is a place to view all the application settings in the applications `_settings` directory.
    It user interface is a tabbed view to visually group the settings in:
    - Application
    - Gallery
    - Customizer
    - Code Editor
    - Model Viewer
    - Logger
    - Notes
    - Help
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from .base_view import BaseView         #| Base class for all views
from .constants import *                         #| The application constants
from ..backend.path_manager import PathManager   #| Managing file and directory handling for the application
import yaml                                      #| [docs](https://pyyaml.org/wiki/PyYAMLDocumentation)
from pathlib import Path
from collections import namedtuple

# [Types]
SettingsItem = namedtuple('SettingsItem', ['title', 'icon', 'file'])

# [Variables]


# [Main Class]
class SettingsView(BaseView):

    # [Variables]
    settings_config = {
        'application': SettingsItem('Application',  'settings',   'nice123d.yaml'),
        'viewer':      SettingsItem('Model Viewer', 'view_in_ar', 'viewer.yaml'),
    }  
    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        super().__init__(path_manager, **kwargs)
        self.logger = path_manager.logger
        
        self.settings_path = self.paths.settings_path

        self.settings = {}
        self.build_ui()
        

    # [API]
    def build_ui(self):

        with self:
            with ui.card():

                with ui.splitter(value=10).classes('w-full h-full') as splitter:
                    with splitter.before:
                        with ui.tabs().props('vertical').classes('w-full') as tabs:
                            self.tabs = tabs

                            for key, value in self.settings_config.items():
                                setattr(self, key, ui.tab(value.title, icon=value.icon))
                            
                    with splitter.after:
                        with ui.tab_panels(self.tabs, value='Application').props('vertical').classes('w-full'):
                            
                            with ui.tab_panel(self.application) as tab:
                                self.load_settings_to_ui('application')
                            with ui.tab_panel(self.viewer) as tab:
                                self.load_settings_to_ui('viewer')

    def filter_settings(self, dictionary):
        """
        remove all keys starting with '_' from a dictionary
        """
        return {k: v for k, v in dictionary.items() if not k.startswith('_')}


    def add_typed_element(self, key, value, element=None, data=None, help=''):
        """
        add an element to the user interface.
        
        # TODO: checkout knob, slider and range and color input               
        
        """
        
        if type(value) == dict:
            entry   = value.get('value', None)
            element = value.get('element', None)
            help    = value.get('help', f'> last value: {value}')
            data    = value        
            self.add_typed_element(key, entry, element, data, help)

        else:
            if element: # direct named type of ui element
                
                    match element:
                        case 'switch':
                            with ui.grid(columns='40px 1fr 1fr 2fr').classes('w-full'):
                                ui.space().classes('w-10')
                                ui.label(key).classes('w-30')
                                ui.switch(value).classes('w-30')
                                ui.markdown(help).classes('w-full')
                        case 'knob':
                            with ui.grid(columns='40px 1fr 1fr 2fr').classes('w-full'):
                                    

                                ui.space().classes('w-10')
                                ui.label(key).classes('w-30')
                                if data.get('icon',None):
                                    with ui.knob(value, min=data.get('min', 10), max=data.get('max', 40)) \
                                    .classes('w-30'):
                                        ui.icon(data['icon'])
                                else:
                                    ui.knob(value, min=data.get('min', 10), max=data.get('max', 40), show_value=True) \
                                    .classes('w-30')
                                ui.markdown(help).classes('w-full')
                        case 'text':
                            with ui.grid(columns='40px 1fr 1fr 2fr').classes('w-full'):
                                ui.space().classes('w-10')
                                ui.label(key).classes('w-30')
                                ui.input(value, placeholder=value).classes('w-30') \
                                    .props('dense input-style="color: blue" input-class="font-mono"')
                                ui.markdown(help).classes('w-full')

            else: # use value for ui detection
                with ui.grid(columns='40px 1fr 1fr 2fr').classes('w-full'):
                    ui.space().classes('w-10')
                    if isinstance(value, bool):
                        ui.label(key).classes('w-20')
                        ui.switch(value).classes('w-30')
                    elif isinstance(value, int):
                        ui.label(key).classes('w-30')
                        ui.number(value, value=value, format='%i').classes('w-30') \
                            .props('input-style="color: blue" input-class="font-mono"')
                    elif isinstance(value, float):
                        ui.label(key).classes('w-30')
                        ui.number(value, value=value, format='%.2f').classes('w-30') \
                            .props('input-style="color: blue" input-class="font-mono"')
                    else:
                        ui.label(key).classes('w-30')
                        ui.input(value, placeholder=value).classes('w-30') \
                            .props('dense input-style="color: blue" input-class="font-mono"') 
                        # https://nicegui.io/documentation/input

                    ui.markdown(help).classes('w-full')

    # TODO: make this a generic function only passing 'title'
    def load_settings_to_ui(self, key='application'):
        """
        generate the UI for the given  settings page
        """
        if key not in self.settings_config:
            raise ValueError(f'Unknown settings key: {key}')

        item = self.settings_config[key]

        if not (self.settings_path / item.file).exists():
            raise FileNotFoundError(f'File not found: {item.file}')

        with open(self.settings_path / item.file, 'r') as file:
            self.settings[key] = yaml.safe_load(file)	
        
        with ui.row():
            ui.icon(item.icon).classes('text-xl')
            ui.label(item.title).classes('text-xl')
        with ui.card().classes('w-full h-full'):
            for key, value in self.filter_settings(self.settings[key]).items():
                if type(value) == dict:
                    with ui.expansion(key).classes('w-full h-full').props('style="background-color: #f0f0f0;"'):
                        
                        for key, value in self.filter_settings(value).items():
                            if type(value) == dict:
                                self.add_typed_element(key, value)
                            else:
                                self.add_typed_element(key, value, help=f'last value: {value}')
                else:
                    self.add_typed_element(key, value, help=f'last value: {value}')
    # [Event Handlers]

