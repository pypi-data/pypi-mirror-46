"""
.. Note::
   This plugin is not scalable.

Shows an interface that displays the commands, their usage and required privileges.
"""

import pymania

from pymania.plugins.chat import CommandParser
from pymania.plugins.gui import Manialink, generate_pagination

STATE_PAGE = 'current_help_page'

class HelpPlugin:
    """ Shows a gui with all chat commands. """
    version = pymania.__version__
    name = 'help'
    depends = 'chat', 'gui'
    __slots__ = 'chat', 'gui', 'config'

    def __init__(self):
        self.chat = None
        self.gui = None
        self.config = {}

    async def load(self, config, dependencies):
        """ Register help chat command. """
        self.chat = dependencies['chat']
        self.gui = dependencies['gui']
        self.config = config

        @self.chat.command(CommandParser('help', description='Show help for all commands'))
        async def _help_command(player):
            player.states[STATE_PAGE] = 0
            await self._show_help_gui(player)

    async def _show_help_gui(self, player):
        limit = self.config['commands_per_page']
        max_page = max(int(len(self.chat.commands) / limit - 1), 0)
        manialink = Manialink(self.gui, [player])
        commands = list(self.chat.commands.values())[player.states[STATE_PAGE] * limit:limit]
        pagination = generate_pagination(
            manialink,
            player,
            self.config['page_jump_count'],
            max_page,
            STATE_PAGE,
            self._show_help_gui
        )
        manialink.render(
            self.config['manialink_template'],
            commands=pymania.plugins.chat.get_command_data(commands),
            pagination=pagination,
            current_page=int(player.states[STATE_PAGE] + 1),
            amount_pages=int(max_page + 1)
        )
        await manialink.show()
