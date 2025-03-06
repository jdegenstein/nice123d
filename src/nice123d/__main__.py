"""
nice123d - a ocp_standalone viewer with nicegui.io

file:           nice123d/__main__.py
file-id:        56f65297-932d-40d3-9c21-4c4b54a5f8e8
project:        nice123d
project-id:     e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a
author:         jdegenstein, felix@42sol.eu


created: 2025-01-24

desc: |
    This module creates a graphical window with a text editor and CAD viewer (based on ocp_vscode). 
    The graphical user interface is based on nicegui and spawns the necessary subprocess and allows
    for re-running the user-supplied script and displaying the results.

Key Features:
  - Has a run button for executing user code
  - Has a keyboard shortcut of CTRL-Enter to run the user code

license:

    Copyright 2025 jdegenstein / felix@42sol

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

# [Imports]
from nicegui import app, ui
from pathlib import Path
from .elements.constants import *
from .main_window import MainWindow

# [Constants]

# [Variables]

# [Functions]
def main():

    # Startup
    win = MainWindow(app)

    # - register handlers
    app.native.window_args["resizable"] = Yes
    app.native.start_args["debug"] = Yes
    # app.native.settings["MATPLOTLIB"] = No #TODO: check why this generates an error on felix Win11 machine?
    # app.native.settings['ALLOW_DOWNLOADS'] = Yes # export "downloads" ?

    app.on_startup(win.startup)
    app.on_shutdown(win.on_close_window)  # TODO: maybe this is not needed ...

    # Execution
    win.run()

# [Main]
if __name__ in {"__main__", "__mp_main__"}:

    ui.add_css('''
    .nicegui-content {
        padding: 0;
        height: 800px;
        overflow-y: hidden;
    }
    .nicegui-scroll-area {
        height: 100%;
    }
    .nicegui-codemirror {
        height: 100%;
    }
    .iframe {
        width: 100%;
        height: 100%;
    }
    ''')
    
    # Add CSS to disable scrolling
    ui.add_head_html('''
    <style>
    body {
        overflow: hidden;
    }
    </style>
    ''')
    
    def on_resize(width: int, height: int):
        ui.notify(f"Window resized: {width}x{height}")

    ui.on("resize", lambda e: on_resize(e.args["width"], e.args["height"]))
    
    
    main()
    # Run the NiceGUI app
    ui.run(
        native      = True,
        window_size = (1280, 800),
        title       = "nice123d",
        fullscreen  = False,
        reload      = False
        # https://nicegui.io/documentation#package_for_installation
    )