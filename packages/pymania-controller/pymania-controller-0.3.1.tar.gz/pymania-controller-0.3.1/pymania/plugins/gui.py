"""
.. Note::
   This plugin is scalable, as long as the minimums/maximums of the manialink ID and action ID do
   not overlap between the instances.

Allocates manialink and action IDs automatically and handles responses thereof.
"""

import logging
import random

import jinja2

import pymania

STATE_MANIALINKS = 'manialinks'

class Manialink:
    """ Generates XML in manialink flavor and shows/hides them.

    :ivar int timeout: Amount of seconds to show this manialink
    :ivar bool close_on_action: Close and dereference the manialink upon doing an action
    """
    __slots__ = (
        '_plugin',
        '_recipients',
        '_xml',
        '_ident',
        '_actions',
        'timeout',
        'close_on_action',
    )

    def __init__(self, gui_plugin, recipients):
        """
        :param GuiPlugin gui_plugin: Plugin instance to use for managing IDs
        :param list recipients: List of :class:`pymania.plugin.players.Player` instances
        """
        self._plugin = gui_plugin
        self._recipients = recipients
        self._ident = self._allocate_manialink_id()
        self._actions = []
        self._xml = None
        self.timeout = 0
        self.close_on_action = True

    def __del__(self):
        # deallocate all associated actions and the ID for other manialinks to use after all
        # references to this instance are gone
        self._plugin.manialinks.remove(self._ident)
        for id_ in self._actions:
            del self._plugin.actions[id_]
        self._plugin.logger.debug('Free link ID %d and actions %s', self._ident, str(self._actions))

    def allocate_action(self, handler):
        """ Allocates an unique action ID for the given handler.

        :param handler: Coroutine to associate to the action ID
        :return: A unique action ID to use in templates
        """
        while True:
            id_ = random.randint(*self._plugin.minmax_actions)
            if id_ not in self._plugin.actions:
                self._plugin.actions[id_] = handler
                self._actions.append(id_)
                return id_

    def render(self, template_file, **kwargs):
        """ Renders the given template file with the specified arguments. """
        self._xml = f'<?xml version="1.0" encoding="utf-8"?><manialink id="{self._ident}">' \
            + self._plugin.jinja_env.get_template(template_file).render(**kwargs) \
            + '</manialink>'

    async def show(self):
        """ Shows this manialink using the settings from this instance.

        :return: Identifier of this manialink. Can be used to retrieve this instance from a player.
        """
        if self._xml is None:
            raise RuntimeError(f'Manialink with ID {self._ident} must be rendered before showing')
        for player in self._recipients:
            if STATE_MANIALINKS not in player.states:
                player.states[STATE_MANIALINKS] = {}
            player.states[STATE_MANIALINKS][self._ident] = self
        if not self._recipients:
            await self._plugin.remote.execute(
                'SendDisplayManialinkPage', self._xml, self.timeout, self.close_on_action
            )
        else:
            await self._plugin.remote.execute(
                'SendDisplayManialinkPageToLogin',
                ','.join([x.login for x in self._recipients]),
                self._xml, self.timeout, self.close_on_action
            )

    async def hide(self):
        """ Hides this manialink. """
        xml = f'<?xml version="1.0" encoding="utf-8"?><manialink id="{self._ident}"/>'
        for player in self._recipients:
            del player.states[STATE_MANIALINKS][self._ident]
        if not self._recipients:
            await self._plugin.remote.execute('SendDisplayManialinkPage', xml, 1, False)
        else:
            await self._plugin.remote.execute(
                'SendDisplayManialinkPageToLogin',
                ','.join([x.login for x in self._recipients]),
                xml, 1, False
            )

    def _allocate_manialink_id(self):
        while True:
            id_ = random.randint(*self._plugin.minmax_manialinks)
            if id_ not in self._plugin.manialinks:
                self._plugin.manialinks.append(id_)
                return id_

class GuiPlugin:
    """ Holds manialink IDs, actions and handles action responses. """
    version = pymania.__version__
    name = 'gui'
    depends = 'remote', 'players', 'chat'
    logger = logging.getLogger(__name__)

    __slots__ = (
        'remote',
        'players',
        'minmax_manialinks',
        'minmax_actions',
        'manialinks',
        'actions',
        'jinja_env',
    )

    def __init__(self):
        self.remote = None
        self.players = None
        self.minmax_manialinks = None
        self.minmax_actions = None
        self.manialinks = []
        self.actions = {}
        self.jinja_env = None

    async def load(self, config, dependencies):
        """ Intercepts the PlayerManialinkPageAnswer callback. """
        self.players = dependencies['players']
        self.remote = dependencies['remote']
        self.minmax_manialinks = config['minmax_manialinks']
        self.minmax_actions = config['minmax_actions']
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(config['template_directory'])),
            autoescape=jinja2.select_autoescape(['xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

        @self.remote.callback('TrackMania.PlayerManialinkPageAnswer')
        async def _manialink_answer(_uid, login, action_id):
            try:
                handler = self.actions[action_id]
            except KeyError:
                return # o.k, action ID does not belong to this instance or dummy ID was taken

            player = self.players.get(login)
            await handler(player)

            try:
                # pylint: disable=protected-access
                for manialink in player.states[STATE_MANIALINKS].copy().values():
                    if action_id in manialink._actions and manialink.close_on_action:
                        del player.states[STATE_MANIALINKS][manialink._ident]
                        break
            except KeyError:
                pass # o.k, manialink was shown to everyone

        @self.remote.callback('TrackMania.PlayerDisconnect')
        async def _player_quit(login):
            player = self.players.get(login)
            try:
                for manialink in player.states[STATE_MANIALINKS].copy().values():
                    # pylint: disable=protected-access
                    del player.states[STATE_MANIALINKS][manialink._ident]
            except KeyError:
                pass # o.k, player never had any manialinks

    async def unload(self):
        """ Hide all GUIs that belong to this controller instance. """
        if self.remote is not None:
            await self._hide_all_manialinks()

    async def _hide_all_manialinks(self):
        for id_ in self.manialinks:
            xml = f'<?xml version="1.0" encoding="utf-8"?><manialink id="{id_}"/>'
            await self.remote.execute('SendDisplayManialinkPage', xml, 1, False)

# pylint: disable=too-many-arguments
def generate_pagination(manialink, player, jump, max_page, state, show_func):
    """ Generates generic pagination for a manialink. """
    pagination = {
        'first': None, 'prev_jump': None, 'prev': None, 'next': None, 'next_jump': None,
        'last': None, 'close': 0
    }

    if player.states[state] != 0:
        async def _first_page(player):
            player.states[state] = 0
            await show_func(player)
        async def _prev_page_jump(player):
            player.states[state] = max(player.states[state] - jump, 0)
            await show_func(player)
        async def _prev_page(player):
            player.states[state] -= 1
            await show_func(player)
        pagination['first'] = manialink.allocate_action(_first_page)
        pagination['prev_jump'] = manialink.allocate_action(_prev_page_jump)
        pagination['prev'] = manialink.allocate_action(_prev_page)

    if player.states[state] != max_page:
        async def _last_page(player):
            player.states[state] = max_page
            await show_func(player)
        async def _next_page_jump(player):
            player.states[state] = min(player.states[state] + jump, max_page)
            await show_func(player)
        async def _next_page(player):
            player.states[state] += 1
            await show_func(player)
        pagination['next'] = manialink.allocate_action(_next_page)
        pagination['next_jump'] = manialink.allocate_action(_next_page_jump)
        pagination['last'] = manialink.allocate_action(_last_page)

    return pagination
