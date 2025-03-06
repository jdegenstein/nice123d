"""
ViewManager

file:           nice123d/elements/view_manager.py
file-id:        9980bdb8-716d-40b8-884c-b09c71838447
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class is used for managing the views of the application.
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from .base_button import BaseButton      #| Base class for all buttons
from .base_button_bar import BaseButtonBar #| Base class for all button bars
from .base_view import BaseView          #| Base class for all views
from .constants import *                         #| The application constants
from ..backend.path_manager import PathManager     #| Managing file and directory handling for the application

# [Variables]

# [Main Class]
class ViewManager():

    # [Variables]
    last_button_left  = None # TODO: move this to the button bar
    last_button_right = None

    ctrl = "Ctrl"
    alt = "Alt"
    all_views = {}

    # [Constructor]
    def __init__(self, pages = None, add_zoom=False):
        if platform.system() == 'MacOS':
            self.ctrl = "Cmd"

        ui.colors(active='#00004f',accent='#3874a0', info='#555555')
        self.pages = pages  # TODO: this member needs to be removed ...
        self.add_zoom = add_zoom
        self.ctrl_bar = BaseButtonBar('looks_one')
        self.alt_bar = BaseButtonBar('looks_two', sibling_button_bar=self.ctrl_bar)
        self.ctrl_bar.sibling_button_bar = self.alt_bar
        
        # TODO: move default to a yaml file

        self.views = None 
        self.list_views = {Side.LEFT: [], Side.RIGHT: []} # NEW: manage the views positions (left or right) in a list

        # TOOD: 2025-02-07 integrate this in add_new_view ... use partials for left and right

        if P__experimental:
            self.map_button_to_views = {
                'Ctrl+1': self.show_editor_left,
                'Alt+1':  self.show_editor_right,
                'Ctrl+2': self.show_viewer_left,
                'Alt+2':  self.show_viewer_right,
                'Ctrl+3': self.show_console_left,
                'Alt+3':  self.show_console_right,
                'Ctrl+4': self.show_settings_left,
            }
        else:
            self.map_button_to_views = {
                'Ctrl+1': self.show_editor_left,
                'Ctrl+2': self.show_console_left,
                'Alt+1':  self.show_viewer_right,
                'Alt+2':  self.show_console_right,
            }
  
    def setup(self, views):
        self.views = views
        #self.pages[]

    def add_new_view( self, view : BaseView, side : Side, text : str, icon : str):
        button_left = None
        button_right = None
        if side in [Side.LEFT, Side.BOTH]:        
            index = len(self.ctrl_bar._buttons)+1
            short_cut_left = f'{self.ctrl}+{index}'
            tooltip_left = f'{text} `{short_cut_left}`'
            print(f'add_new_view left: {text} {short_cut_left}')
            
            # TODO: map_button_to_views needs to be replaced with a function passed to this method and a partial depending on the side

            button_left = BaseButton('', icon=icon, on_click=self.map_button_to_views[short_cut_left])
            button_left.tooltip(tooltip_left)
            button_left.view = view
            self.ctrl_bar.add(button_left, view.title)
            

        if side in [Side.RIGHT, Side.BOTH]:
            index = len(self.alt_bar._buttons)+1
            short_cut_right = f'{self.alt}+{index}'
            tooltip_right = f'{text} `{short_cut_right}`'
            print(f'add_new_view right: {text} {short_cut_right}')
            
            # TODO: map_button_to_views needs to be replaced with a function passed to this method and a partial depending on the side
            
            button_right = BaseButton('', icon=icon, on_click=self.map_button_to_views[short_cut_right])
            button_right.tooltip(tooltip_right)
            button_right.view = view
            self.alt_bar.add(button_right, view.title)

        if button_left and button_right:
            button_left.sibling_button = button_right
            button_right.sibling_button = button_left

        self.all_views[text] = view
        if side == Side.RIGHT:
            self.list_views[Side.RIGHT].append(view)
        else:
            self.list_views[Side.LEFT].append(view)

    # TODO: remove functions from here ...
    def setup_left_button_bar(self, views : list):
        views.reverse()

        with ui.button_group() as bar:	
            self.left_button_bar = bar
            for page in self.pages:
                
                if self.pages[page].is_left:
                    active = self.pages[page]
                    active.view = views.pop()
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Ctrl')
                    else: 
                        short_cut = active.short_cut
                    
                    button = BaseButton('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
                    button.tooltip(f'{active.title} `{short_cut}`')
                    
                    self.pages[page].button_left = button
                    button.props('fab color=default')
                    # INFO: `inactive` is the color from the header background color                    

            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=self.set_zoom_left).tooltip('Zoom left `Meta+0`')
                z.props('fab color=info')

        return self.left_button_bar

    # TODO: remove functions from here ...
    def setup_right_button_bar(self, views : list):
        views.reverse()
        
        with ui.button_group() as bar:	
            self.right_button_bar = bar
            for page in self.pages:
                if self.pages[page].is_right:
                    active = self.pages[page]                    
                    active.view = views.pop()
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Alt')
                    else: 
                        short_cut = active.short_cut
                    
                    button = BaseButton('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
                    button.tooltip(f'{active.title} {short_cut}')
                    
                    if self.pages[page].button_left:
                        button.sibling_button = self.pages[page].button_left
                        self.pages[page].button_left.sibling_button = button 

                    self.pages[page].button_right = button   
                    
                    button.props('fab color=default')
                    # INFO: `inactive` is the color from the header background color 
            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=self.set_zoom_right).tooltip('Zoom right `Meta+0`')
                z.props('fab color=info')

        return self.right_button_bar


    def prepare_move(self, page, side):
        page_info = None 

        # find the correct page
        for view_data in self.pages.values():
            if view_data.view == page:
                page_info = view_data
                break

    def highlight_button(self, button, side):
        if type(button) is not BaseButton:
            print(f'ERROR: highlight_button: button not of type BaseButton {button}')
            return # TODO: raise exception
        if type(side) is not Side:
            print(f'ERROR: highlight_button: side not of type Side {side}')
            return # TODO: raise exception
        if side not in (Side.LEFT, Side.RIGHT):
            print(f'ERROR: highlight_button: side not in (Side.LEFT, Side.RIGHT) {side}')
            return # TODO: raise exception


        if side == Side.LEFT:        
            if button != self.last_button_left:
                button.props('fab color=active')
                if self.last_button_left:
                    self.last_button_left.props('fab color=default')
            # else: nothing to do - keep same button active

            self.last_button_left = button

        else: # side == Side.RIGHT:        
            if button != self.last_button_right:
                button.props('fab color=active')
                if self.last_button_right:
                    self.last_button_right.props('fab color=default')
            # else: nothing to do - keep same button active
            self.last_button_right = button  

    def show_editor_left(self, event):
        print(f'show_editor_left')
        self.views.show_editor(Side.LEFT)
        self.ctrl_bar.set_active_button(self.views.editor.title)

    def show_editor_right(self, event):
        print(f'show_editor_right')
        self.views.show_editor(Side.RIGHT)
        self.alt_bar.set_active_button(self.views.editor.title)

    def show_viewer_left(self, event):
        print(f'show_viewer_left')
        self.views.show_viewer(Side.LEFT)
        self.ctrl_bar.set_active_button(self.views.viewer.title)
    
    def show_viewer_right(self, event):
        print(f'show_viewer_right')
        self.views.show_viewer(Side.RIGHT)
        self.alt_bar.set_active_button(self.views.viewer.title)

    def show_console_left(self, event):
        print(f'show_console_left')
        self.views.show_console(Side.LEFT)
        self.ctrl_bar.set_active_button(self.views.console.title)

    def show_console_right(self, event):
        print(f'show_console_right')
        self.views.show_console(Side.RIGHT)
        self.alt_bar.set_active_button(self.views.console.title)


    def show_settings_left(self, event):
        print(f'show_settings_left')
        self.views.show_settings()
        self.ctrl_bar.set_active_button(self.views.settings.title)


    def set_zoom(self, value):
        self.size_splitter.value = value        

    def set_zoom_left(self):
        if self.size_splitter.value == 100:
            self.size_splitter.value = 50
        elif self.size_splitter.value < 50:
            self.size_splitter.value = 50
        else: # self.size_splitter.value >= 50:
            self.size_splitter.value = 100

    def set_zoom_right(self):
        if self.size_splitter.value == 0:
            self.size_splitter.value = 50
        elif self.size_splitter.value > 50:
            self.size_splitter.value = 50
        else: # self.size_splitter.value <= 50:
            self.size_splitter.value = 0

    def left(self):
        if self.size_splitter.value < 50:
            self.size_splitter.value = 50
        elif self.size_splitter.value < 100:
            self.size_splitter.value = 100
        else:
            self.size_splitter.value = 50

    def right(self):
        if self.size_splitter.value > 50:
            self.size_splitter.value = 50
        elif self.size_splitter.value == 50:
            self.size_splitter.value = 0
        else:
            self.size_splitter.value = 50

    def ensure_left_visible(self):
        if self.size_splitter.value < 50:
            self.size_splitter.value = 50

    def ensure_right_visible(self):
        if self.size_splitter.value > 50:
            self.size_splitter.value = 50
