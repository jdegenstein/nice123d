"""
BaseView

file:           nice123d/elements/base_view.py
file-id:        7385bbca-9dc9-424b-af9d-43bffd84154b
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class is used for a base view of the application on a specific panel.
"""
# [Imports]                                      #| description or links 
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from typing import Optional                      #| [docs](https://docs.python.org/3/library/typing.html)
from datetime import datetime                    #| [docs](https://docs.python.org/3/library/datetime.html)
import time                                      #| [docs](https://docs.python.org/3/library/time.html)
from .constants import *
from ..backend.path_manager import PathManager    #| Managing file and directory handling for the application


# [Main Class]
class BaseView(ui.element):
    view_id = 0
    # [Variables]
    logger_available = False    # Whether the logger is available
    main = None                 # The main ui element
    
    # [Constructor]
    def __init__(self, path_manager=None, **kwargs):
        super().__init__(**kwargs)
        BaseView.view_id += 1
        self.title = f'view_{BaseView.view_id}'
        
        # Type check the path_manager
        if path_manager is not None and type(path_manager) is not PathManager:
            raise TypeError('The path_manager must be of type PathManager')

        if path_manager is not None:
            self._paths = path_manager
            self.logger = path_manager.logger
        

        self.start_time = {}

    # [API]

    @property
    def paths(self):
        return self._paths

    def define_logger(self, logger):
        """Set the logger to use for logging."""

        if type(logger) is not ui.log   :
            raise TypeError('The logger must be of type logging.Logger')
        
        self.logger = logger
        self.logger_available = True
        self.time_start(call_id='default')

    def time_start(self, call_id):
        """Start the timer for the logger."""
        self.start_time[call_id] = time.time()

    def info(self, function, message, call_id = 'default', do_time=True):
        """Log an info message with the current time."""
        timestamp = datetime.now().strftime('%X.%f')[:-5]
        used_time = ''
        if do_time:
            used_time = f'in {time.time() - self.start_time[call_id]:0.2}s'
        self.logger.push(f'{timestamp}: [{function}] {message} {used_time}')

    # [Event Handlers]
    def set_visibility(self, visible):
        if self.main:
            self.main.set_visibility(visible)

        return super().set_visibility(visible)
    
    def move(self,
            target_container: Optional[ui.element] = None ) -> None:

        if self.main:
            self.main.move(target_container)

        return super().move(target_container)