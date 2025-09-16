"""
nicegui cadviewer

name: cadviewer.py
by:   jdegenstein
date: January 24, 2025

desc:

This module creates a graphical window with a text editor and CAD viewer (based on ocp_vscode). 
The graphical user interface is based on nicegui and spawns the necessary subprocess and allows
for re-running the user-supplied script and displaying the results.

Key Features:
  - Has a run button for executing user code
  - Has a keyboard shortcut of CTRL-Enter to run the user code

license:

    Copyright 2025 jdegenstein

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

from nicegui import app, ui
from nicegui.events import KeyEventArguments
import subprocess
app.native.window_args["resizable"] = True
app.native.start_args["debug"] = True
# app.native.settings['ALLOW_DOWNLOADS'] = True # export "downloads" ?

editor_fontsize = 18
# TODO: consider separate editor execution thread from nicegui thread
import platform

# run ocp_vscode in a subprocess
def startup_all():
    global ocpcv_proc
    
    if platform.system == "Windows":
        ocpcv_proc = subprocess.Popen([r"uv\uv.exe", "run", "python", "-m", "ocp_vscode"])
    else:
        ocpcv_proc = subprocess.Popen([r"uv/uv", "run", "python", "-m", "ocp_vscode"])
    # spawn separate viewer process
    # pre-import build123d and ocp_vscode in main thread
    exec("from build123d import *\nfrom ocp_vscode import *")


def button_run_callback():
    exec(code.value)


def shutdown_all():
    ocpcv_proc.kill()
    # ocpcv_proc.terminate() # TODO: investigate best cross-platform solution
    app.shutdown()


app.on_startup(startup_all)

button_frac = 0.05


with ui.splitter().classes(
    "w-full h-[calc(100vh-2rem)] no-wrap items-stretch border"
) as splitter:
    with splitter.before:
        with ui.column().classes("w-full items-stretch border"):
            with ui.row():
                with ui.column().classes("w-1/3"):
                    ui.button(
                        "Run Code", icon="send", on_click=lambda: button_run_callback()
                    ).classes(f"h-[calc(100vh*{button_frac}-3rem)]")
            # ui.button('shutdown', on_click=lambda: shutdown_all()) # just close the window
            code = (
                ui.codemirror(
                    'from build123d import *\nfrom ocp_vscode import *\nset_port(3939)\na_box = Box(1,2,3)\nshow(a_box)',
                    language="Python",
                    theme="vscodeLight",
                )
                .classes(f"h-[calc(100vh*{1-button_frac}-3rem)]")
                .style(f"font-size: {editor_fontsize}px")
            )
    with splitter.after:
        with ui.column().classes("w-full items-stretch border"):
            ocpcv = (
                ui.element("iframe")
                .props('src="http://127.0.0.1:3939/viewer"')
                .classes("h-[calc(100vh-3rem)]")
            )


# handle the CTRL + Enter run shortcut:
def handle_key(e: KeyEventArguments):
    if e.modifiers.ctrl and e.action.keydown:
        if e.key.enter:
            button_run_callback()


keyboard = ui.keyboard(on_key=handle_key)
# TODO: consider separating this module and how best to organize it (if name == main, etc.)
app.on_shutdown(shutdown_all)  # register shutdown handler
ui.run(
    native=True,
    window_size=(1700, 900),
    title="nice123d",
    fullscreen=False,
    reload=False,
)
# ui.run(native=True, window_size=(1800, 900), fullscreen=False, reload=True) #use reload=True when developing rapidly, False helps exit behavior

# layout info https://github.com/zauberzeug/nicegui/discussions/1937
