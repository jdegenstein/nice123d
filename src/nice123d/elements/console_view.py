"""
ConsoleView -> BaseView -> ui.element

file:           nice123d/elements/consol_view.py
file-id:        6a848c30-083d-4343-a323-3325552dff86
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         felix@42sol.eu

description: |
    This class implements the project console view.
    It collects all the log messages from the different views.
"""

# [Imports]                                      #| description or links
from nicegui import ui                           #| [docs](https://nicegui.readthedocs.io/en/latest/)   
import logging
from rich.logging import RichHandler  # https://rich.readthedocs.io/en/stable/logging.html
from datetime import datetime
import pyperclip
from .constants import *                         #| The application constants
from .base_view import BaseView         #| Base class for all views
from ..backend.path_manager import PathManager    #| Managing file and directory handling for the application

# [Variables]
logger = logging.getLogger()

# [Classes]
# Configure logging with RichHandler
class NiceGUILogHandler(logging.Handler):
    """Custom log handler to send logs to a NiceGUI log UI element."""
    def __init__(self, log_element: ui.log) -> None:
        super().__init__()
        self.log_element = log_element

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to the NiceGUI log element."""
        try:
            msg = self.format(record)
            self.log_element.push(msg)
        except Exception:
            self.handleError(record)



# [Main Class]
class ConsoleView(BaseView):
    """
    Keeping a common ui element for logging messages from the different views.
    """

    def __init__(self, path_manager : PathManager=None, **kwargs):
        super().__init__(**kwargs)
        self.time_start('init_console_view')
        # TODO:           self.logger = NiceGUILogHandler(self.logger_ui)
        with self:
            with ui.row().classes('w-full h-full') as main:
                ui.button('Log time', on_click=lambda: logger.warning(datetime.now().strftime('%X.%f')[:-5]))
                ui.button('Clear log', on_click=lambda: self.logger.clear())
                ui.button('Copy log', on_click=lambda:pyperclip.copy(self.logger._text))
                self.logger = ui.log(max_lines=40).classes('w-full h-full')
                
        self._handler = NiceGUILogHandler(self.logger)
        logger.addHandler(self._handler)
        ui.context.client.on_disconnect(lambda: self.logger.removeHandler(self._handler))
        
        self.main = main
        self.path_manager = path_manager
        if self.path_manager:
            self.path_manager.set_logger(self.logger)
            self._logger = path_manager.logger
        
        super().define_logger(self.logger)

        self.push(self.info('init', 'Code editor initialized', call_id='init_console_view'))

    def push(self, message):
        self.logger.push(message)

