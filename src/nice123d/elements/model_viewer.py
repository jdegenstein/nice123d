"""
ModelViewer -> BaseView -> ui.element

file:           nice123d/elements/model_viewer.py
file-id:        2fd0a90c-d9db-497c-bffc-d2a249572601
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         jdegenstein, felix@42sol.eu

description: |
    This class implements the model viewer - using OCP_vscode for viewing the models.
"""

# [Imports]                                       #| description or links
from nicegui import ui                            #| [docs](https://nicegui.readthedocs.io/en/latest/)   
from .base_view import BaseView           #| Base class for all views
from .constants import *                          #| The application constants
from ..backend.path_manager import PathManager      #| Managing file and directory handling for the application
import subprocess                                 #| [docs](https://docs.python.org/3/library/subprocess.html)
from ocp_vscode import *                          #| [docs](https://ocp_vscode.readthedocs.io/en/latest/)
import time                                       #| [docs](https://docs.python.org/3/library/time.html)

# [Variables]
running = False

# [Main Class]
class ModelViewer(BaseView):
    """"
    Model viewer element keeps track of the model files.
    Using:
    - OCP_vscode for viewing the models.
    - pywebview for the GUI.
    """
    # [Variables]
    # [Constructor]
    def __init__(self, path_manager : PathManager, ip_address= '127.0.0.1', port=3939, **kwargs):
        super().__init__(path_manager, **kwargs)
        if path_manager:
            self.logger = path_manager.logger
        self.port = port
        self.time_start('model_viewer')
        with self:
            self.ocpcv = (
                            ui.element("iframe")
                            .props(f'src="http://{ip_address}:{port}/viewer"')
                            #.classes("w-full h-[100vh-5rem]") # h-[calc(100vh-5rem)]
                            .style('width: 100%; height: 100%;')
                            
                        )
            self.info('ModelViewer', f'init src="http://{ip_address}:{port}/viewer"', call_id='model_viewer')
        self.main = self.ocpcv

    # [API]
    def startup(self):
        """
        run ocp_vscode in a subprocess
        """
        global running

        if running:
            self.shutdown()
            time.sleep(5)
        
        running = True
        self.time_start('model_viewer')
        # spawn separate viewer process
        self.ocpcv_proc = subprocess.Popen(["python", "-m", "ocp_vscode", "--port", str(self.port)])
        # pre-import build123d and ocp_vscode in main thread
        exec("from build123d import *\nfrom ocp_vscode import *")
        self.info('ModelViewer', f'started {self.ocpcv_proc}', call_id='model_viewer')

    def shutdown(self):
        """"
        kill the ocp_vscode process
        """
        global running
        self.info(f'Model Viewer', f'shutdown {self.ocpcv_proc}', call_id='model_viewer')

        if running:
            running = False
            self.ocpcv_proc.kill()
        # ocpcv_proc.terminate() # TODO: investigate best cross-platform solution

    # [Event Handlers]
