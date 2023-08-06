"""
Defines several useful plugins for use with the pymania controller.

Each plugin must define a version, name, its dependencies and a load/unload method. The dependencies
are guaranteed to be fully initialized before the plugin is loaded. This approach prevents overly
complicated plugin ranking systems that need to be maintained by hand.

Basic structure of a plugin:

.. code-block:: python

    class AwesomePlugin:
        version = '1.0.0'
        name = 'awesome'
        depends = 'remote', 'chat' # optional
        logger = logging.getLogger(__name__) # optional

        async def load(self, config, dependencies):
            allocate_some_resources()
            server = dependencies['remote']

            @server.callback('Trackmania.WhateverCallback')
            async def handle_whatever_callback(arg1, arg2):
                some_value = config['some_value']
                do_something_with(some_value, arg1, arg2)

        async def unload(self): # optional
            destroy_some_resources()

A plugin can optionally manage a main loop. If multiple plugins implement a main loop, pymania waits
for all of them to finish, except if an exception occured.

.. code-block:: python

    async def main(self):
        try:
            await some_loop()
        except ControllerInterrupt as exc:
            log_something()
            raise exc

.. Important::
   What to do if multiple plugins intercept the same callback? Instead of adding complex logic
   that somehow handles the order in which callback handlers are invoked, the plugins themselves
   should expose e.g. a list of conditions under which a specific handler is disabled. The plugins
   can then modify these in the load() method.

.. Important::
   While not required, you should add a `logger` attribute to your plugin. Pymania then appends a
   rotating file handler to your logger that appends messages to a log file. The format, output
   directory, backup count and max file size can be specified in the config script.

.. Important::
   Unloading the plugin must not fail if plugin is not currently loaded.

To use this plugin, simply add the following to the plugin dictionary of your controller config:

.. code-block:: python

    plugins = {
        'pymania.plugins.RemotePlugin': (),
        'pymania.plugins.ChatPlugin': (),
        'my.AwesomePlugin': {
            'some_value': 0,
        },
    }
"""

from pymania.plugins.database import DatabasePlugin
from pymania.plugins.remote import RemotePlugin
from pymania.plugins.players import PlayerManagementPlugin
from pymania.plugins.chat import ChatPlugin
from pymania.plugins.reload import ReloadPlugin
from pymania.plugins.gui import GuiPlugin
from pymania.plugins.map import MapPlugin
from pymania.plugins.info import InfoPlugin
from pymania.plugins.privileges import PrivilegeManagementPlugin
from pymania.plugins.help import HelpPlugin
from pymania.plugins.records import RecordManagementPlugin
from pymania.plugins.duel_chase import DuelChasePlugin
