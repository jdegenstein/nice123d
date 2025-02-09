"""
CodeEditor -> BaseView -> ui.element

file:           nice123d/elements/note_viewer.py
file-id:        354d94a2-d095-4a98-8a81-bbf4af27d20a
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the code editor using CodeMirror.
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from nicegui import events
from elements.base_view import BaseView          #| Base class for all views
from .constants import *                         #| The application constants
from backend.parameters import *                 #| The application parameters
from backend.parameter_group import *            #| The application parameter groups

# [Variables]
# TODO: consider separate editor execution thread from nicegui thread
# TODO: the scroll bar is not working ! we need to fix it.


# [Main Class]
class CodeEditor(BaseView):
    """
    A Python code editor component.
    """

    # [Variables]
    font_size = 18   # todo: use font size for the editor

    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        """Initialize the Python editor component."""
        super().__init__(path_manager, **kwargs)
        
        # TODO: use paths directly and not split it to extra members
        self.model_path      = self.paths.models_path
        self.code_file       = self.paths.code_file
        self.new_file        = self.paths.new_file
        
        with self:
            with ui.scroll_area().classes('w-full h-full'):
                # Setup editor
                self.editor = ui.codemirror(language='python', theme='dracula')
                self.editor.classes('w-full h-full')

        # TODO: check if this is the right place for this
        if self.code_file.exists():
            with self.code_file.open() as f:
                self.editor.value = f.read()
        else:
            with self.new_file.open() as f:
                self.editor.value = f.read()

    # [API]
    def set_code_file(self, event):
        # TODO: save this in path_manager if exists
        self.code_file = event.value

    def prepare_move(self):
        """Prepare to move the editor to a new location."""
        self.code = self.editor.value

    def finish_move(self):
        """Finish moving the editor to a new location."""
        self.editor.value = self.code
        self.editor.update()

    def execute_code(self, code: str):
        """Execute the Python code in the editor."""
        # TODO: look into `RestrictedPython` or  `Jupyter` for security 
        try:
            exec(code)
            return "Code executed successfully"
        except Exception as e:
            return f"Error: {str(e)}"

    # [Event Handlers]
    def on_save(self):
        """Save the current code to a file."""
        self.time_start('on_save')
        content = self.editor.value
        file_path = self.paths.code_file
        with file_path.open('w') as f:
            f.write(content)
        self.info('file', 'saved successfully', call_id='on_save')

    def on_load(self):
        """Load code from a file into the editor."""
        # TODO: add test/load file
        self.time_start('on_load')

        def handle_upload(e: events.UploadEventArguments):
            text = e.content.read().decode('utf-8')
            self.editor.value = text
            self.file.value = e.name 
            
            upload_bar.delete()
            
        upload_bar = ui.upload(auto_upload=True, on_upload=handle_upload).props('accept=.py').classes('max-w-full')        
        # TODO: ^ for now we need a second click to upload the file
        
        self.info('file', 'loaded successfully', call_id='on_load')
        
    def on_new(self):
        """Clear the editor."""
        self.time_start('on_new')
        if self.new_file:
            with self.new_file.open('r') as f:
                self.editor.value = f.read()
            self.info('file', f'loaded template {self.new_file}', call_id='on_new')
        else:
            self.info('file', 'No template file specified (`new.py` in `models`). Using minimal default code', call_id='on_new')
            self.editor.set_value('from build123d import *\nfrom ocp_vscode import *\n\n\nshow_all()')

    def on_run(self):
        """Execute the code from the editor."""
        self.time_start('on_run')
        result = self.execute_code(self.editor.value)
        self.info('on_run', result, call_id='on_run')
        
        
