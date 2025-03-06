nice123d
========

.. toctree::
   :maxdepth: 4

   nice123d

Core GUI
--------


.. mermaid::

   classDiagram
      note "Core GUI classes"
      
      Element <|-- Button
      Element <|-- Drawer
      Drawer <|-- BaseDrawer
      Button <|-- BaseButton

      Element <|-- BaseButton
      class BaseButton {
      +BaseButtonBar parent
      +String text
      +String shortcut
      +BaseButton sibling
      +BaseView view
      }
      Element <|-- ButtonGroup
      ButtonGroup <|-- BaseButtonBar
      class BaseButtonBar {
      +BaseButtonBar sibling
      +BaseButton children
      }
      
      class BaseDrawer {
      +BaseButtonBar tools
      +toggle_visible()
      }
      Element <|-- BaseView
      class BaseView {
      +ui.element main
      +is_visible()
      +move(ui.element target)
      }

.. mermaid::

   classDiagram
      note "View GUI classes"
      BaseView <-- CodeEditor
      BaseView <-- ModelViewer
      BaseView <-- ConsoleView
      
      BaseView <-- SettingsView