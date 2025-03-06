"""
MainView

file:           nice123d/main_view.py
file-id:        200fe85c-b034-4465-8d72-166d94281441
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the main view of the application.
"""

# [Imports]                                                #| description or links
from nicegui import ui                                     #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nicegui import events  
from .elements.base_button_bar import BaseButtonBar        #| [docs](https://nicegui.readthedocs.io/en/latest/elements.html#buttonbar)
from .elements.code_editor     import CodeEditor           #| 
from .elements.model_viewer    import ModelViewer          #| 
from .elements.console_view    import ConsoleView          #| 
from .elements.settings_view   import SettingsView         #| 
from .backend.path_manager     import PathManager          #| Managing file and directory handling for the application
from .elements.view_manager    import ViewManager          #|
from .elements.view_data       import ViewData             #|

# TODO: pass resize of splitter to elements.
from .elements.constants import *


# [Variable]


# [Main Class]
class MainViews():
    # [Variables]
    # - Views
    editor     = None
    viewer     = None
    console    = None
    settings   = None

    # - Management
    views_left  = None # TODO Move to view manager
    views_right = None # TODO Move to view manager
    
    left_views      = [] # TODO Move to view manager
    right_views     = [] # TODO Move to view manager

    # [Constructor]
    def __init__(self, path_manager):

        if type(path_manager) is not PathManager:
            raise TypeError("The path_manager must be an instance of PathManager.")
        self.path_manager = path_manager

        self.manager = ViewManager(g__views, P__experimental)
        
        # first console view to have the logger available
        self.console    = ConsoleView(path_manager)
        self.logger = path_manager.logger
        
        self.editor     = CodeEditor(path_manager)
        self.settings   = SettingsView(path_manager)
        self.viewer     = ModelViewer(path_manager)

        if P__experimental:
            self.manager.add_new_view(self.editor,       Side.BOTH,   'Code Editor',      'code')
            self.manager.add_new_view(self.viewer,       Side.BOTH,   'Model Viewer',     'view_in_ar')
            self.manager.add_new_view(self.console,      Side.BOTH,   'Console',          'article')
            self.manager.add_new_view(self.settings,     Side.LEFT,   'Settings',         'settings')
        else: 
            self.manager.add_new_view(self.editor,       Side.LEFT,   'Code Editor',      'code')
            self.manager.add_new_view(self.viewer,       Side.RIGHT,  'Model Viewer',     'view_in_ar')
            self.manager.add_new_view(self.console,      Side.BOTH,   'Console',          'article')
            

        # TODO: move the following lines to manager
        self.list_views  = [self.editor, self.viewer, self.console, self.settings]
        self.show_left   = None
        self.show_right  = None

    
    def setup(self):
        path_manager = self.path_manager

        with ui.splitter().classes('w-full h-full items-stretch') as main_splitter:
        
            with main_splitter.before:
                with ui.column().classes('w-full h-full items-stretch') as container:
                    self.left_container = container
                    self.editor.move(container)
                    self.settings.move(container)

                    #  TODO: move this to view_manager ...
                    self.left_views = [self.editor, self.settings]


            with main_splitter.after:
                with ui.column().classes('w-full h-full items-stretch') as container:
                    self.right_container = container

                    self.viewer.move(container)
                    self.console.move(container)

                    #  TODO: move this to view_manager ...
                    self.right_views = [self.viewer, self.console]


            with main_splitter.separator:
                if P__use_splitter_buttons:
                    splitter_buttons = []
                    with ui.column().classes('w-full h-full items-stretch'):
                        a = ui.button(icon='multiple_stop')
                        splitter_buttons.append(a)
                        ui.space()
                        b = ui.button(icon='send', on_click=self.editor.on_run)
                        splitter_buttons.append(b)
                        ui.space()
                    for button in splitter_buttons:
                        button.classes('text-white')
                        button.props('color=accent')

        self.setup_views()

        with ui.left_drawer(top_corner=True, bottom_corner=True).classes('p-3').style('background-color: #d7e3f4').props('mini dense') as left_drawer:
            self.left_drawer = left_drawer

            if platform.system() == 'Mac':
                meta = "Cmd"
            else:
                meta = "Ctrl"

            # https://fonts.google.com/icons
            ui.icon('code').classes('text-4xl')
            ui.button(icon="send",     on_click=self.editor.on_run
                    ).tooltip(f'Run Code `{meta}+Enter`').classes('text-small').props('color=accent dense')           
            ui.button(icon="star",     on_click=self.editor.on_new 
                    ).tooltip(f'New `{meta}+N`').props('dense')
            ui.button(icon="upload",   on_click=self.editor.on_load
                    ).tooltip(f'Load `{meta}+O`').props('dense')
            ui.button("",    icon="download", on_click=self.editor.on_save
                    ).tooltip(f'Save `{meta}+S`').props('dense')
            if 0:
                ui.button("",         icon="undo",     on_click=self.editor.on_undo).props('color="grey"')
                ui.button("",         icon="redo",     on_click=self.editor.on_redo).props('color="grey"')
            #TODO: add extend buttons function
            #TODO: add light / dark theme from test/examples
            ui.button(icon="cancel",   on_click=self.toggle_drawer
                    ).tooltip(f'close drawer').classes('text-small') \
                    .props('background-color: #d7e3f4') \
                    .props('dense')
            
        with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between') as header:
            with ui.row() as row:
                self.menu_button = ui.button(on_click=self.toggle_drawer, icon='close').props('flat color=white')
                
                self.manager.ctrl_bar.move(row)
                ui.space()
                # TODO: use path_manager
                file_path = ui.label('model / path / file name').classes('text-xl')
                
                self.path_manager.set_code_file_label(file_path)
                self.path_manager.code_file = (self.path_manager.models_path / "basic.py" ).resolve()
                ui.space()
                self.splitter_value(main_splitter)
            
                self.manager.alt_bar.move(row)
            row.update()
            self.manager.ctrl_bar.create()
            self.manager.alt_bar.create()


    def init_views(self):
        #TODO: this needs to be defined in the Settings (nice123d.yaml)
        self.viewer.startup()
        self.manager.setup(self)
        ui.keyboard(on_key=self.handle_key)

        # TODO: improve this we need to have a way to activate the buttons         
        self.show_editor(Side.LEFT)
        self.show_viewer(Side.RIGHT)
        self.manager.ctrl_bar.set_active_button(self.editor.title)
        self.manager.alt_bar.set_active_button(self.viewer.title)

    def splitter_value(self, main_splitter):
        size_splitter = ui.number('Value', format='%.0f', value=50, min=0, max=100, step=10)
        size_splitter.bind_value(main_splitter)  
        if P__experimental_splitter:
            size_splitter.set_visibility(Yes)
        else:
            size_splitter.set_visibility(No)
        
        self.manager.size_splitter = size_splitter

                
    def setup_views(self):

        self.list_views = [self.editor, self.viewer, self.console, self.settings]
        self.show_left = self.editor
        self.show_right = self.viewer
    
        self.list_views_left  = [ self.editor, self.settings]
        self.list_views_right = [self.viewer,  self.console]


    def show_all(self):
        
        count = 0
        for view in self.list_views:
            if view:
                count += 1
                view.set_visibility(True)


    def update_views(self):
        self.show_left.set_visibility(True)
        self.show_right.set_visibility(True)

        count = 0
        for view in self.list_views:
            if view != self.show_left and view != self.show_right:
                if view:
                    count += 1
                    view.set_visibility(False)
        
        ui.update()

    def already_shown_on_side(self, page, side):
        if side == Side.LEFT:
            return self.show_left == page
        elif side == Side.RIGHT:
            return self.show_right == page
        else:
            return False

    def is_on_other(self, page, side):
        if side == Side.LEFT:
            return page in self.list_views_right
        elif side == Side.RIGHT:
            return page in self.list_views_left
        else:
            return False

    def modify_size(self, side):
        """If a already shown views button is clicked again, the size of the view is modified.
            50% <-> 100% (for left views), 50% <-> 0% (for right views)
        """
        if type(side) is not Side:
            raise TypeError("The side must be an instance of Side.")
        elif side not in [Side.LEFT, Side.RIGHT]:
            raise ValueError("The side must be either Side.LEFT or Side.RIGHT.")

        if side == Side.LEFT:
            self.manager.left()                
        else:
            self.manager.right()

    def make_visible(self, side):
        if type(side) is not Side:
            raise TypeError("The side must be an instance of Side.")
        elif side not in [Side.LEFT, Side.RIGHT]:
            raise ValueError("The side must be either Side.LEFT or Side.RIGHT.")

        if side == Side.LEFT:
            self.manager.ensure_left_visible()
        else: # side == Side.RIGHT:
            self.manager.ensure_right_visible()

    def show_settings(self):
        """Show the settings page - it is restricted to the left side."""

        page = self.settings
        side = Side.LEFT
        if self.already_shown_on_side(page, side):
            self.modify_size(side)
        else:
            self.manager.set_zoom(100)
            page.set_visibility(True)
            self.show_left = page

        self.update_views()

    def other(self, side):
        if side == Side.LEFT:
            return Side.RIGHT
        else:
            return Side.LEFT

    def move_to_side(self, page, side):
        code = ''
        if page == self.editor:
            self.editor.prepare_move()
        
        page.set_visibility(False)

        if side == Side.LEFT and page in self.list_views_right:
            self.list_views_right.remove(page)
            self.list_views_left.append(page)
            self.manager.prepare_move(page, side)  
            page.move(self.left_container)          

        elif side == Side.RIGHT and page in self.list_views_left:
            self.list_views_left.remove(page)
            self.list_views_right.append(page)
            self.manager.prepare_move(page, side)   
            page.move(self.right_container)         
        else:
            pass # impossible
        
        page.set_visibility(True)

        if page == self.editor:
            self.editor.finish_move()

    def show_left_or_right(self, page, side, page_sibling_left=None, page_sibling_right=None):
        if side == Side.LEFT:
            page_sibling = page_sibling_right
        
        elif side == Side.RIGHT:
            page_sibling = page_sibling_left
        else:
            pass # impossible

        if self.already_shown_on_side(page, side):
            self.modify_size(side)

        elif self.is_on_other(page, side):
            if side == Side.LEFT:                 
                self.show_left  = page
                if self.show_right == page:
                    if page_sibling:
                        self.manager.alt_bar.set_active_button(page_sibling.title)
                        self.move_to_side(page_sibling, Side.RIGHT)
                        self.show_right = page_sibling
            elif side == Side.RIGHT:
                self.show_right = page
                if self.show_left == page:
                    if page_sibling:
                        self.manager.ctrl_bar.set_active_button(page_sibling.title)
                        self.move_to_side(page_sibling, Side.LEFT)
                        self.show_left = page_sibling

            self.move_to_side(page, side)

            self.make_visible(side)

        else:
            page.set_visibility(True)
            if side == Side.LEFT:
                self.show_left = page
                if not self.show_right:
                    self.show_right = page_sibling

            elif side == Side.RIGHT:
                self.show_right = page
                
                if not self.show_left:
                    self.show_left = page_sibling
                    
            else:
                pass # impossible
                
        self.update_views()

        
    def show_editor(self, side):
        if P__experimental:
            self.show_left_or_right(self.editor, side, self.console, self.viewer)
        else:
            self.show_left_or_right(self.editor, Side.LEFT, self.viewer, self.viewer)
        
    def show_viewer(self, side):

        if P__experimental:
            self.show_left_or_right(self.viewer, side, self.editor, self.console)
        else:
            self.show_left_or_right(self.viewer, Side.RIGHT, self.editor, self.console)

    def show_console(self, side):

        self.show_left_or_right(self.console, side, self.editor, self.viewer)

    def toggle_drawer(self, event):
        self.left_drawer.toggle()
        if self.menu_button.icon == 'menu':
            self.menu_button.icon = 'close'
        else:
            self.menu_button.icon = 'menu'
        ui.update()  # Ensure UI updates


    def handle_key(self, e: events.KeyEventArguments):
        manager = self.manager

        if active_os == "Windows":
            main_modifier = e.modifiers.ctrl
        elif active_os == "Mac":
            main_modifier = e.modifiers.cmd
        else:
            main_modifier = e.modifiers.meta

        if main_modifier and e.action.keydown:
            if e.key.enter:
                print(f'>>>>>>>>>>>>>> on run')
                self.editor.on_run()             # TODO: fix editor
            elif e.key.name == "s":
                self.editor.on_save()
            elif e.key.name == "o":
                self.editor.on_load()
            elif e.key.name == "t":
                self.editor.on_new()
            elif e.key.name == "1":
                self.manager.show_editor_left(e)
            elif e.key.name == "2":
                if P__experimental:
                    self.manager.show_viewer_left(e)
                else:
                    self.manager.show_console_left(e)
            elif e.key.name == "3":
                if P__experimental:
                    self.manager.show_console_left(e)

            elif e.key.name == "4":
                if P__experimental:
                    self.manager.show_settings_left(e)

        elif e.modifiers.alt and e.action.keydown:
            if e.key.name == "1":
                if P__experimental:
                    self.manager.show_editor_right(e)
                else:
                    self.manager.show_viewer_right(e)
            elif e.key.name == "2":
                if P__experimental:
                    self.manager.show_viewer_right(e)
                else:
                    self.manager.show_console_right(e)

            elif e.key.name == "3":
                if P__experimental:
                    self.manager.show_console_right(e)



if P__experimental:
    g__views = {    # https://fonts.google.com/icons?icon.query=stop
                    # use `Meta` for views that are used on both sides
                    # use `Ctrl` for views that are used on the left side
                    # use `Alt` for views that are used on the right side
        'Meta+1':    ViewData('Editor',     'code',       both,  "Meta+1"),
        'Meta+2':    ViewData('Viewer',     'view_in_ar', both,  "Meta+2"),
        'Meta+3':    ViewData('Console',    'article',    both,  "Meta+3"),
        'Ctrl+4':    ViewData('Settings',   'settings',   left,  "Ctrl+4"),
    }
    left_buttons  = ['Meta+1', 'Meta+2', 'Meta+3', 'Ctrl+4']
    right_buttons = ['Meta+1', 'Meta+2', 'Meta+3']

else:
    g__views = {    # https://fonts.google.com/icons?icon.query=stop
                    # use `Meta` for views that are used on both sides
                    # use `Ctrl` for views that are used on the left side
                    # use `Alt` for views that are used on the right side
        'Ctrl+1':    ViewData('Editor',     'code',       left,  "Ctrl+1"),
        'Alt+1' :    ViewData('Notes',      'info',       right, "Alt+1"),
        'Meta+2':    ViewData('Console',    'article',    both,  "Alt+2"),
    } 
    left_buttons  = ['Ctrl+1', 'Meta+2']
    right_buttons = ['Alt+1',  'Meta+2']
