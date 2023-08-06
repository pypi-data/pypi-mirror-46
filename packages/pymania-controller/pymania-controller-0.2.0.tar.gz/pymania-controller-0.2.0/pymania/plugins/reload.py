"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances.

Add chat commands to be able to reload the configuration or plugins while the controller is running.
"""

import pymania

from pymania.plugins.chat import CommandParser

class ReloadPlugin:
    """ Adds a chat command to reload the controller's config and/or plugins. """
    version = pymania.__version__
    name = 'reload'
    depends = 'chat', 'remote'

    async def load(self, plugin_config, dependencies):
        """ Defines the reload chat command. """
        chat = dependencies['chat']
        remote = dependencies['remote']

        parser = CommandParser('reload', description='Reload the controller')
        parser.add_argument('--config', action='store_true', help='Reload the configuration script')
        parser.add_argument('--plugins', action='store_true', help='Reload the plugin modules')

        @chat.command(parser, plugin_config['privilege'])
        async def _chat_reload(player, config, plugins):
            if not config and not plugins:
                await remote.send_message(plugin_config['missing_option'], player.login)
                return

            items = []
            flags = pymania.ControllerState(0)
            if config:
                items.append('configuration')
                flags = flags | pymania.ControllerState.RELOAD_CONFIG
            if plugins:
                items.append('plugins')
                flags = flags | pymania.ControllerState.RELOAD_PLUGINS
            await remote.send_message(
                plugin_config['message'].format(player=player.nickname, items=', '.join(items)),
                player.login
            )

            raise pymania.ControllerInterrupt(flags, f'{player.login} issued a reload command')
