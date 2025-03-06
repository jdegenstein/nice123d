<!--
file:         .vscode/SETUP.md
file-id:      7a35a93b-b908-4263-9053-4f1451dfd3b1
project:      nice123d
project-id:   e2bbd03f-0ac6-41ec-89ae-2ad52fa0652a

TODO: update content of this file.

description:  This file contains the folder documentation. |
    The folder is part of the `nice123d` project.
-->
# Setup for usage

## Setup

> [!Note]
> `python3` for Linux and MacOS.
> `python` for Windows.

```shell
python3 -m pip install -e .     # install dependencies that are defined in `pyproject tomple.
python3 -m nice123d             # run the application (default is `native      = True`)
```
### Build the documentation 

```shell 
python -m pip install sphinxcontrib-mermaid
cd docs 
sphinx-apidoc -o .\source\ ..\nice123d
make html
```

## Setting up Sphinx 

```shell
mkdir docs
cd docs
sphinx-quickstart --ext-autodoc
```

## Other Notes 
```shell
python3 -m venv .venv
source .venv/bin/activate
which python
which pip
```

Should show `...your path.../nicegui-cadviewer/.venv/bin/python`
and `...your path.../nicegui-cadviewer/.venv/bin/pip`

Now install the dependencies:
- ocp_vscode
- build123d
- nicegui
- pywebview

---
```
pip install ocp_vscode
pip install nicegui
pip install pywebview
pip list | grep ocp_vscode
pip list | grep build123d
pip list | grep nicegui
pip list | grep pywebview
```
---

Should show
---
```
ocp_vscode         2.6.1
build123d          0.9.0
nicegui            2.10.1
pywebview          5.3.2
```
---


# Setup for development 

follow the steps above but add the last build version for `build123d` with:

---
````
pip install git+https://github.com/gumyr/build123d.git
pip install pyyaml
pip install gitpython
pip install click
pip install rich




```
---



 
