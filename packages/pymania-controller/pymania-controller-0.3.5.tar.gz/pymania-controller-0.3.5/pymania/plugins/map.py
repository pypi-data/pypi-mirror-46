"""
.. Note::
   This plugin is _not_ scalable.

Stores map data persistently and has the ability to download maps from TMX.
"""

import cgi
import collections
import logging
import pathlib
import random
import shutil
import urllib.request

import defusedxml.xmlrpc as defused_xmlrpc
import sqlalchemy

import pymania

from pymania.plugins.chat import CommandParser, PrivilegeError, MissingOptionsError
from pymania.plugins.gui import Manialink, generate_pagination

STATE_REMOVE = 'maps_to_remove'
STATE_PAGE = 'current_list_page'
STATE_CRITERIA = 'list_criteria'
STATE_QUEUE_SIZE = 'queue_size'

class MapError(Exception):
    """ Raised when an error in a public function of the map plugin occured. """

class Map:
    """ Defines a map with a filename, an environment and more. """
    __tablename__ = 'maps'

    uid = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    raw_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False) # stripped off formatting
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    file = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    author = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    environment = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    mood = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    bronze_time = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    silver_time = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    gold_time = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    author_time = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    coppers = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    is_multilap = sqlalchemy.Column(sqlalchemy.Boolean(), nullable=False)
    lap_count = sqlalchemy.Column(sqlalchemy.Integer())
    cp_count = sqlalchemy.Column(sqlalchemy.Integer())

class MapPlugin:
    """ Manages match settings and chat commands related to maps. """
    version = pymania.__version__
    name = 'map'
    depends = 'database', 'remote', 'chat', 'players', 'gui'
    logger = logging.getLogger(__name__)

    __slots__ = (
        'database',
        'remote',
        'gui',
        'config',
        'map_class',
        'match_settings',
        'queued_maps',
    )

    def __init__(self):
        self.database = None
        self.remote = None
        self.gui = None
        self.config = {}
        self.map_class = Map
        self.match_settings = None
        self.queued_maps = collections.deque()

    # pylint: disable=too-many-arguments
    def get(self, uid=None, name=None, author=None, environment=None, mood=None):
        """ Retrieves a list with tracks that match the specified criteria.

        :param str name: Raw name to query for (without formatters)
        :param str author: Name of the author to query for
        :param str environment: Environment to query for
        :param str mood: Mood to query for
        :return: A query object to use offset(), limit(), all() and first() on.
        """
        result_set = self.database.session.query(self.map_class)
        if uid is not None:
            return result_set.filter_by(uid=uid)
        if name is not None:
            op1 = sqlalchemy.func.lower(self.map_class.raw_name)
            op2 = sqlalchemy.func.lower(name)
            result_set = result_set.filter(op1.contains(op2))
        if author is not None:
            op1 = sqlalchemy.func.lower(self.map_class.author)
            op2 = sqlalchemy.func.lower(author)
            result_set = result_set.filter(op1.contains(op2))
        if environment is not None:
            op1 = sqlalchemy.func.lower(self.map_class.environment)
            op2 = sqlalchemy.func.lower(environment)
            result_set = result_set.filter(op1.contains(op2))
        if mood is not None:
            op1 = sqlalchemy.func.lower(self.map_class.mood)
            op2 = sqlalchemy.func.lower(mood)
            result_set = result_set.filter(op1.contains(op2))
        return result_set

    async def get_map_info(self, file_name):
        """ Retrieves information about the given map file. """
        info = await self.remote.execute('GetChallengeInfo', file_name)
        return self.map_class(
            uid=info['UId'],
            raw_name=pymania.remove_formatting(info['Name']),
            file=info['FileName'],
            name=info['Name'],
            author=info['Author'],
            environment=info['Environnement'],
            mood=info['Mood'],
            bronze_time=info['BronzeTime'],
            silver_time=info['SilverTime'],
            gold_time=info['GoldTime'],
            author_time=info['AuthorTime'],
            coppers=info['CopperPrice'],
            is_multilap=info['LapRace']
        )

    async def add_map(self, file_name):
        """ Adds a map.

        :param file_name: Path relative to the tracks directory
        :return: A :class:`Map` instance containing map information
        :raises MapError: Map does not match the current match settings
        """
        try:
            await self.remote.execute('CheckChallengeForCurrentServerParams', file_name)
        except defused_xmlrpc.xmlrpc_client.Fault:
            raise MapError(f'Map "{file_name}" does not match the current match settings')
        try:
            await self.remote.execute('AddChallenge', file_name)
        except defused_xmlrpc.xmlrpc_client.Fault:
            raise MapError(f'Map "{file_name}" already added')

        info = await self.get_map_info(file_name)
        self.database.session.add(info)
        self.database.session.commit()
        return info

    async def remove_map(self, map_info):
        """ Removes a map.

        :param file_name: Path relative to tracks directory
        """
        if self.database.session.query(self.map_class.uid).count() == 1:
            raise MapError(f'Cannot remove the last remaining map on the server!')
        try:
            await self.remote.execute('RemoveChallenge', map_info.file)
        except defused_xmlrpc.xmlrpc_client.Fault:
            raise MapError(f'No such map "{map_info.raw_name}" on the server.')
        self.database.session.delete(map_info)

    async def sync_with_database(self):
        """ Syncs the database with the current match settings. """
        current_index = 0
        chunk_size = 50
        try:
            while True:
                chunk = await self.remote.execute('GetChallengeList', chunk_size, current_index)
                current_index += len(chunk)
                for challenge in chunk:
                    if not self.get(uid=challenge['UId']).all():
                        self.database.session.add(await self.get_map_info(challenge['FileName']))
                if len(chunk) < chunk_size:
                    break
        except defused_xmlrpc.xmlrpc_client.Fault:
            pass # o.k, no more maps to process
        self.database.session.commit()

    async def download_map(self, url):
        """ Downloads a map and returns its original file name.

        :return: File name of downloaded map (in the tracks directory)
        :raises MapError: Unable to download map
        """
        try:
            if not urllib.request.urlparse(url).scheme:
                url = 'http://' + url
        except urllib.request.URLError:
            raise MapError(f'URL {url} is erroneous')
        try:
            with urllib.request.urlopen(url) as response:
                map_dir = await self.remote.execute('GetTracksDirectory')
                file_name = cgi.parse_header(response.info()['Content-Disposition'])[1]["filename"]
                with open(pathlib.Path(map_dir) / file_name, 'wb') as handle:
                    shutil.copyfileobj(response, handle)
        except urllib.request.URLError:
            raise MapError(f'Unable to download map from {url}')
        except TypeError:
            raise MapError(f'Downloaded file from {url} does not provide a map name')
        return file_name

    @staticmethod
    def _build_command_parser():
        parser = CommandParser('map', description='Add or remove maps')
        subparsers = parser.add_subparsers()
        add_parser = subparsers.add_parser('add', help='Add one or multiple maps')
        add_parser.add_argument('--url', nargs='+', help='Fetch the track from an URL')
        add_parser.add_argument('--tmx', metavar='ID', nargs='+', help='Fetch the track from TMX')
        remove_parser = subparsers.add_parser('remove', help='Remove one or multiple maps')
        remove_parser.add_argument('--uid', help='Remove by UID')
        remove_parser.add_argument('--name', help='Remove by name')
        remove_parser.add_argument('--author', help='Remove by author')
        remove_parser.add_argument('--environment', help='Remove by environment')
        remove_parser.add_argument('--mood', help='Remove by mood')
        remove_parser.add_argument('--continue', action='store_true', help='Continue to remove')
        subparsers.add_parser('shuffle', help='Shuffle the map queue')
        queue_parser = subparsers.add_parser('queue', help='Queue a map of your choice')
        queue_parser.add_argument('uid', help='Unique identifier of the map')
        list_parser = subparsers.add_parser('list', help='Query maps on this server')
        list_parser.add_argument('--name', help='Query by name')
        list_parser.add_argument('--author', help='Query by author')
        list_parser.add_argument('--environment', help='Query by environment')
        list_parser.add_argument('--mood', help='Query by mood')
        return parser

    @staticmethod
    def _get_sub_privileges(config):
        return config['add_privilege'] \
            | config['remove_privilege'] \
            | config['shuffle_privilege'] \
            | config['queue_privilege'] \
            | config['list_privilege']

    async def load(self, config, dependencies):
        """ Loads the match settings and syncs the database with them. """
        self.remote = dependencies['remote']
        self.database = dependencies['database']
        self.gui = dependencies['gui']
        self.map_class = self.database.add_table(Map)
        self.config = config

        self.match_settings = config['match_settings_file']
        self.logger.info('Trying to load match settings from "%s"', self.match_settings)
        try:
            if await self.remote.execute('LoadMatchSettings', self.match_settings) == 0:
                reason = f'Unable to load any maps from "{self.match_settings}"'
                self.logger.error(reason)
                raise pymania.ControllerInterrupt(pymania.ControllerState.SHUTDOWN, reason)
        except defused_xmlrpc.xmlrpc_client.Fault:
            pass # o.k, file does not exist

        await self.sync_with_database()

        @self.remote.callback('TrackMania.BeginChallenge')
        async def _begin_challenge(challenge, _warmup, _continuation):
            track = self.get(uid=challenge['UId']).first()
            if track is None:
                raise RuntimeError(f"Challenge with {challenge['UId']} must exist in the DB")
            track.lap_count = challenge['NbLaps']
            track.cp_count = challenge['NbCheckpoints']
            self.database.session.commit()

        @self.remote.callback('TrackMania.EndChallenge')
        async def _end_challenge(_rankings, _challenge, _wu, _continue, is_restarted):
            if not is_restarted:
                try:
                    entry = self.queued_maps.popleft()
                    entry[1].states[STATE_QUEUE_SIZE] -= 1
                    await self.remote.execute('ChooseNextChallenge', entry[0].file)
                    await self.remote.send_message(self.config['next_queued'].format(
                        map=entry[0].raw_name,
                        player=entry[1].nickname
                    ))
                except IndexError:
                    pass # o.k, no queued maps

        chat = dependencies['chat']
        @chat.command(self._build_command_parser(), sub_privs=self._get_sub_privileges(config))
        async def _chat_map(player, **kwargs):
            await self._map_command(player, **kwargs)

    async def _map_command(self, player, **kwargs):
        if not kwargs:
            await self.remote.send_message(self.config['map_usage'], player.login)
            return
        command = kwargs.pop('command')
        if command == 'add':
            if not player.has_privileges(self.config['add_privilege']):
                raise PrivilegeError(self.config['add_privilege'])
            if kwargs.get('url') is None and kwargs.get('tmx') is None:
                raise MissingOptionsError('map add')
            await self._add_command(player, **kwargs)
        elif command == 'remove':
            if not player.has_privileges(self.config['remove_privilege']):
                raise PrivilegeError(self.config['remove_privilege'])
            await self._remove_command(player, **kwargs)
        elif command == 'shuffle':
            if not player.has_privileges(self.config['shuffle_privilege']):
                raise PrivilegeError(self.config['shuffle_privilege'])
            await self._shuffle_command(player)
        elif command == 'queue':
            if not player.has_privileges(self.config['queue_privilege']):
                raise PrivilegeError(self.config['queue_privilege'])
            await self._queue_command(player, **kwargs)
        elif command == 'list':
            if not player.has_privileges(self.config['list_privilege']):
                raise PrivilegeError(self.config['list_privilege'])
            await self._list_command(player, **kwargs)

    async def _add_command(self, player, **kwargs):
        urls = kwargs.get('url') or []
        for tmx_id in kwargs.get('tmx') or []:
            urls.append(self.config['default_download_link'].format(id=tmx_id))
        for url in urls:
            try:
                info = await self.add_map(await self.download_map(url))
                await self.remote.send_message(self.config['add_message'].format(
                    player=player.nickname,
                    map=info.raw_name
                ))
            except MapError as exc:
                msg = self.config['map_error'].format(error=str(exc))
                await self.remote.send_message(msg, player.login)

    async def _remove_command(self, player, **kwargs):
        if kwargs.pop('continue'):
            if not player.states.get(STATE_REMOVE):
                await self.remote.send_message(self.config['cannot_continue'], player.login)
                return
            for track in player.states[STATE_REMOVE]:
                try:
                    await self.remove_map(track)
                    await self.remote.send_message(self.config['del_message'].format(
                        player=player.nickname,
                        map=track.raw_name
                    ))
                except MapError as exc:
                    msg = self.config['map_error'].format(error=str(exc))
                    await self.remote.send_message(msg, player.login)
            del player.states[STATE_REMOVE]
        else:
            player.states[STATE_REMOVE] = self.get(**kwargs).all()
            if player.states[STATE_REMOVE]:
                names = ', '.join([f'"{x.raw_name}"' for x in player.states[STATE_REMOVE]])
                msg = self.config['prompt_continue'].format(maps=names)
                await self.remote.send_message(msg, player.login)
            else:
                await self.remote.send_message(self.config['invalid_query'], player.login)

    async def _shuffle_command(self, player):
        maps = self.database.session.query(self.map_class).all()
        random.shuffle(maps)
        msg = self.config['shuffle_message'].format(player=player.nickname)
        await self.remote.execute('ChooseNextChallengeList', [x.file for x in maps])
        await self.remote.send_message(msg, player.login)

    async def _queue_command(self, player, **kwargs):
        uid = kwargs.get('uid')
        for entry in self.queued_maps:
            if entry[0].uid == uid:
                await self.remote.send_message(self.config['already_queued'], player.login)
                return

        track = self.get(uid=uid).first()
        if track is None:
            msg = self.config['invalid_uid'].format(uid=uid)
            await self.remote.send_message(msg, player.login)
        else:
            if not STATE_QUEUE_SIZE in player.states:
                player.states[STATE_QUEUE_SIZE] = 0
            max_size = self.config['max_queue_amount']
            if player.states[STATE_QUEUE_SIZE] >= max_size:
                if not player.has_privileges(self.config['infinite_queue_size_privilege']):
                    msg = self.config['exceed_queue_size'].format(amount=max_size)
                    await self.remote.send_message(msg, player.login)
                    return
            player.states[STATE_QUEUE_SIZE] += 1

            self.queued_maps.append((track, player))
            await self.remote.send_message(self.config['add_queue'].format(
                player=player.nickname,
                map=track.raw_name
            ))

    async def _list_command(self, player, **kwargs):
        player.states[STATE_PAGE] = 0
        player.states[STATE_CRITERIA] = kwargs
        await self._show_list_gui(player)

    async def _show_list_gui(self, player):
        manialink = Manialink(self.gui, [player])

        limit = self.config['list_maps_per_page']
        query = self.get(**player.states[STATE_CRITERIA])
        map_count = query.count()
        max_page = max(int(map_count / limit - 1), 0)
        maps = query.offset(player.states[STATE_PAGE] * limit).limit(limit).all()
        for track in maps:
            async def _juke(player, track=track):
                await self._queue_command(player, uid=track.uid)
            async def _filter_author(player, track=track):
                await self._list_command(player, author=track.author)
            async def _filter_env(player, track=track):
                await self._list_command(player, environment=track.environment)
            async def _filter_mood(player, track=track):
                await self._list_command(player, mood=track.mood)
            track.juke_action = manialink.allocate_action(_juke)
            track.author_action = manialink.allocate_action(_filter_author)
            track.env_action = manialink.allocate_action(_filter_env)
            track.mood_action = manialink.allocate_action(_filter_mood)

        pagination = generate_pagination(
            manialink,
            player,
            self.config['list_page_jump_count'],
            max_page,
            STATE_PAGE,
            self._show_list_gui
        )
        manialink.render(
            self.config['list_manialink_template'],
            maps=maps,
            pagination=pagination,
            current_page=int(player.states[STATE_PAGE] + 1),
            amount_pages=int(max_page + 1)
        )
        await manialink.show()

    async def unload(self):
        """ Saves the current match settings back into the file. """
        if self.remote is not None:
            await self.remote.execute('SaveMatchSettings', self.match_settings)
