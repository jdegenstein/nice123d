"""
PathManager -> BaseView -> ui.element
 +-> [n] Path

file:           nice123d/elements/note_viewer.py
file-id:        af8c5a12-e5df-46f5-9edd-2c88449ae6d7
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the path and file objects for the application.

"""
# [Imports]                                      #| description or links 
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)
from pathlib import Path                         #| [docs](https://docs.python.org/3/library/pathlib.html)
import os                                        #| [docs](https://docs.python.org/3/library/os.html)

# [Variables]

# [Main Class]
class PathManager():
    """
    Path manager keeps track of the paths for the models and the help files.
    """

    # [Variables]
    settings_path = Path(__file__).parent / '../data/_settings'
    models_path = Path(__file__).parent / '../data/_models'
    _code_file = models_path / "basic.py"
    new_file = models_path / "new.py"
    
    # [Constructor]
    def __init__(self, settings_path=None, models_path=None):
        """ Construcutor
        """
        self.ui_code_file = None 
        if settings_path and Path(settings_path).exists():
            self.settings_path = settings_path
        else:
            print(f'[ERROR] User defined settings {settings_path} path does not exist using {self.settings_path}')
        
        if models_path and Path(models_path).exists():
            self.models_path = models_path
        else:
            print(f'[ERROR] User defined models path {models_path} does not exist using {self.models_path}')

    def set_code_file_label(self, file_path):
        self.ui_code_file = file_path

    def set_logger(self, logger):
        self.logger = logger
        

    # [API]
    def push(self, msg):
        if self.logger:        
            self.logger.push(msg)

    @property
    def settings(self):
        return self.settings_path
    
    @property
    def models(self):
        return self.models_path
    
    @property
    def code_file(self):
        return self._code_file
    
    @code_file.setter
    def code_file(self, file_path):
        self._code_file = file_path
        if self.ui_code_file:
            self.ui_code_file.text = str( file_path ).replace( '\\', '/' ).replace('/', ' / ')
            print(f'[INFO] Code file set to {self._code_file}')
            self.ui_code_file.update()


    # TODO: add logger to the path manager

    # [Event Handlers]
    def on_load_data(self):
        self.info("Data loaded")
    
    def on_save_data(self):
        self.info("Data saved")
    
    def on_validate_data(self):
        self.info("Data validated")


# [Main]
if __name__ in {'__main__', '__mp_main__'}:
    print(f'running {__file__}')
    path = PathManager()