"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances.

Manages players and their privileges. All plugins that depend on this plugin and have tasks only
executable by specifically privileged players should expose configuration attributes instead of
hardcoding the privilege:

.. code-block:: python

    # config.py
    class Privilege(enum.Flag):
        CHAT = enum.auto()
        ADD_TRACK = enum.auto()
        ADMIN = ADD_TRACK

    plugins = {
        'pymania.plugins.PlayerManagementPlugin': {},
        'my.track.Plugin': {
            'add_track_privilege': Privilege.ADD_TRACK,
        }
    }

    # awesome.py (pseudo)
    async def some_command(player):
        if int(player.privileges) & add_track_privilege.value:
            add_track()

The nice thing about Python flags is that they are unbound due to the unbound integer data type,
meaning that you have no constraint on the amount of privileges you can use.

.. Important::
   To set non-persistent player attributes, use the `states` attribute of :class:`Player`.
"""

import logging

import defusedxml.xmlrpc as defused_xmlrpc
import sqlalchemy

import pymania

class Player:
    """ Defines a player with a unique login and a formatted nickname. """
    __tablename__ = 'players'

    login = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    nickname = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    privileges = sqlalchemy.Column(sqlalchemy.String(255), default='0')
    states = {}

    def has_privileges(self, privs):
        """ Determines whether this player has the given privileges. """
        if privs is None or privs.value == 0:
            return True
        return (int(self.privileges) & privs.value) != 0

class PlayerManagementPlugin:
    """ Adds a player table and listens to players joining and leaving. """
    version = pymania.__version__
    name = 'players'
    depends = 'database', 'remote'
    logger = logging.getLogger(__name__)

    __slots__ = '_remote', 'database', 'player_class'

    def __init__(self):
        self._remote = None
        self.database = None
        self.player_class = None

    def get(self, login):
        """
        Retrieves the player with the given login. In case you modify the player instance, issue a
        call to PlayerManagementPlugin.database.session.commit() afterwards.
        """
        return self.database.session.query(self.player_class).filter_by(login=login).first()

    async def get_on_server(self):
        """
        Retrieves the database instance of all players that are currently playing on the server.
        """
        async for chunk in self._get_in_chunks():
            for player in chunk:
                yield self.get(player['Login'])

    async def load(self, config, dependencies):
        """ Adds the player table and defines all necessary callbacks. """
        masters = config['masters']
        self._remote = dependencies['remote']
        self.database = dependencies['database']
        self.player_class = self.database.add_table(Player)

        @self._remote.callback('TrackMania.PlayerConnect')
        async def _player_connect(login, _is_spectator):
            self.logger.info('Player with login "%s" connected', login)
            player = self.get(login)
            if player is None:
                base_privileges = str(config['base_privileges'].value)
                player = self.player_class(login=login, privileges=base_privileges)
                self.database.session.add(player)
                self.database.session.commit()
            if login in masters:
                # make sure that the masters have the master privileges in case the config changed
                player.privileges = str(config['master_privileges'].value)
                self.database.session.commit()

        @self._remote.callback('TrackMania.PlayerDisconnect')
        async def _player_disconnect(login):
            self.logger.info('Player with login "%s" disconnected', login)

        @self._remote.callback('TrackMania.PlayerInfoChanged')
        async def _player_changed(Login, NickName, **_kwargs): # pylint: disable=invalid-name
            player = self.get(Login)
            player.nickname = NickName
            self.database.session.commit()

        # there might already be players on the server; simulate a connect and change event to
        # ensure that no weird edge cases happen
        async for chunk in self._get_in_chunks():
            for player in chunk:
                await _player_connect(player['Login'], False)
                await _player_changed(player['Login'], player['NickName'])

    async def _get_in_chunks(self):
        current_index = 0
        chunk_size = 10
        try:
            while True:
                chunk = await self._remote.execute('GetPlayerList', chunk_size, current_index)
                current_index += len(chunk)
                yield chunk
                if len(chunk) < chunk_size:
                    break
        except defused_xmlrpc.xmlrpc_client.Fault:
            pass # o.k, no more players to process
