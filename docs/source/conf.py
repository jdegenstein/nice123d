# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os 
import sys
sys.path.insert(0, os.path.abspath('../../nice123d'))
sys.path.insert(0, os.path.abspath('../../nice123d/backend'))
sys.path.insert(0, os.path.abspath('../../nice123d/elements'))
sys.path.insert(0, os.path.abspath('../../.venv/Lib/site-packages/'))
project = 'nice123d'
copyright = '2025, jdegenstein, felix@42sol.eu'
author = 'jdegenstein, felix@42sol.eu'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.mermaid',
    # FIXME: 'sphinxcontrib.ditaa', # is not working
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
