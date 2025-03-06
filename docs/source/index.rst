.. nice123d documentation master file, created by
   sphinx-quickstart on Thu Feb 20 20:18:01 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nice123d documentation
======================

.. nice123d documentation master file, created by
   sphinx-quickstart on Thu Feb 20 20:18:01 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

   Add your content using ``reStructuredText`` syntax. See the
   `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
   documentation for details.
   
   . https://mermaid.js.org/syntax/classDiagram.html


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   gui_structure.rst
   modules.rst
   classes.rst

.. mermaid:: 

   gantt
   dateFormat  YYYY-MM-DD
   title nice123d Project Plan 
   excludes weekdays 2025-01-24

   section The Idea
   First working code                  :done,    t1a, 2025-01-24, 1d
   Setup the Github repository         :done,    t1b, 2025-01-25, 1d
   Defining the name `nice123d`        :done     t1c, 2025-01-27, 1d
   
   section The GUI-Structure
   Concepts                            :done     t2a, after t1b, 20d
   Building and distribution           :done     t2b, 2025-02-15, 5d
   Documentation                       :active   t2c, after t2b, 5d

   section Testing and Improvements 
   Functional Testing                  :         t3a, after t2c, 5d
   Functional Improvements             :         t3b, after t3a, 5d

