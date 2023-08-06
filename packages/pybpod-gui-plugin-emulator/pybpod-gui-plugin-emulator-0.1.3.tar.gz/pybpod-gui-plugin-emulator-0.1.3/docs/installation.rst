.. _installation:

============
Installation
============

At the command line, in your environment::

    pip install pybpod-gui-plugin-emulator

Afterwards, configure PyBpod to load the plugin:

1. On PyBpod's top menu, go to Options > Edit user settings.
2. Add 'pybpod_gui_plugin_emulator' to the end of the **﻿GENERIC_EDITOR_PLUGINS_LIST** field::

        GENERIC_EDITOR_PLUGINS_LIST = [ 'pybpodgui_plugin',
                            'pybpodgui_plugin_timeline',
                            ...
                            'pybpod_gui_plugin_emulator']

3. Restart PyBpod to load the new plugin.
