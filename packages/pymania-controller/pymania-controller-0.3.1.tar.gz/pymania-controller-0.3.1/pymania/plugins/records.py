"""
.. Note::
   This plugin is _not_ scalable.

Persistently stores locally driven records.
"""

import collections

import sqlalchemy
import sqlalchemy.ext.declarative

import pymania

from pymania.plugins.gui import Manialink

STATE_RECORDS = 'record_manialink'

_Ranking = collections.namedtuple('Ranking', ['rank', 'score', 'nickname'])

class Records:
    """ Defines a local record. """
    __tablename__ = 'records'
    __table_args__ = (
        sqlalchemy.UniqueConstraint('track', 'player'),
    )

    uid = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    score = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)

    @sqlalchemy.ext.declarative.declared_attr
    def track(_unused): # pylint: disable=no-self-use,no-self-argument
        """ Track attribute """
        return sqlalchemy.Column(
            sqlalchemy.String(255),
            sqlalchemy.ForeignKey('maps.uid'),
            nullable=False
        )

    @sqlalchemy.ext.declarative.declared_attr
    def player(_unused): # pylint: disable=no-self-use,no-self-argument
        """ Player attribute """
        return sqlalchemy.Column(
            sqlalchemy.String(255),
            sqlalchemy.ForeignKey('players.login'),
            nullable=False
        )

class RecordManagementPlugin:
    """ Broadcasts info messages. """
    version = pymania.__version__
    name = 'info'
    depends = 'players', 'map', 'database', 'remote', 'gui'
    __slots__ = (
        '_config',
        '_remote',
        '_database',
        '_players',
        '_gui',
        '_current_map',
        'rec_class',
    )

    def __init__(self):
        self._config = None
        self._remote = None
        self._database = None
        self._players = None
        self._gui = None
        self._current_map = None
        self.rec_class = Records

    def get(self, login=None, track_id=None):
        """ Retrieves records matching the given criteria. """
        result_set = self._database.session.query(self.rec_class)
        if login is not None:
            result_set = result_set.filter_by(player=login)
        if track_id is not None:
            result_set = result_set.filter_by(track=track_id)
        return result_set

    def _slow_get_player_rank(self, ordering, login):
        for i, rec in enumerate(self.get(track_id=self._current_map).order_by(ordering)):
            if rec.player == login:
                return str(i + 1)
        return 'n/a'

    async def _refresh_record_widget(self, player, record_tuple=None):
        if record_tuple is None:
            records, rankings, ordering = await self._get_record_info()
        else:
            records, rankings, ordering = record_tuple
        player_index = -1
        for i, rec in enumerate(records):
            if rec.player == player.login:
                player_index = i

        # find rank of current player, if any
        rank = self.get(player.login, self._current_map)
        rec = rank.first()
        if rec is not None:
            try:
                row_num = sqlalchemy.func.row_number().over(
                    partition_by=self.rec_class.uid,
                    order_by=ordering
                ).label('row_number')
                rank = rank.add_column(row_num).from_self().first().row_number
            except sqlalchemy.exc.OperationalError:
                # o.k., db does not support ROW_NUMBER()
                rank = self._slow_get_player_rank(ordering, player.login)
            score = rec.score
        else:
            rank = 'n/a'
            score = 'n/a'
        player_rankings = rankings.copy()
        ranking = _Ranking(
            rank=rank,
            nickname=player.nickname,
            score=score
        )
        if not player_rankings:
            player_rankings.append(ranking)
        else:
            player_rankings[player_index] = ranking

        # generate widget
        if STATE_RECORDS not in player.states:
            player.states[STATE_RECORDS] = Manialink(self._gui, [player])
            player.states[STATE_RECORDS].close_on_action = False
        player.states[STATE_RECORDS].render(
            self._config['rankings_template'],
            rankings=player_rankings,
            player_rank=rank
        )
        await player.states[STATE_RECORDS].show()

    async def _get_record_info(self):
        if await self._remote.execute('GetGameMode') == 4:
            ordering = self.rec_class.score.desc() # for stunts
            transform = str
        else:
            ordering = self.rec_class.score.asc()
            transform = self._config['format_time_func']

        records = self.get(track_id=self._current_map) \
            .order_by(ordering) \
            .limit(self._config['max_records_gui']) \
            .all()

        # generate globally applicable rankings list
        rankings = []
        for i, rec in enumerate(records):
            rankings.append(_Ranking(
                rank=i,
                nickname=self._players.get(rec.player).nickname,
                score=transform(rec.score)
            ))
        return records, rankings, ordering

    async def _refresh_record_widgets(self):
        record_info = await self._get_record_info()
        async for player in self._players.get_on_server():
            await self._refresh_record_widget(player, record_info)

    async def load(self, config, dependencies):
        """ Copy config and remote dependency. """
        self._config = config
        self._remote = dependencies['remote']
        self._database = dependencies['database']
        self._players = dependencies['players']
        self._gui = dependencies['gui']
        self.rec_class = self._database.add_table(Records)

        self._current_map = (await self._remote.execute('GetCurrentChallengeInfo'))['UId']
        await self._refresh_record_widgets()

        @self._remote.callback('TrackMania.BeginChallenge')
        async def _begin_challenge(challenge, _warmup, _continuation):
            self._current_map = challenge['UId']
            await self._refresh_record_widgets()

        @self._remote.callback('TrackMania.PlayerConnect')
        async def _connect(login, _spec):
            await self._refresh_record_widget(self._players.get(login))

        @self._remote.callback('TrackMania.PlayerFinish')
        async def _finish(_uid, login, score):
            if score == 0:
                return

            record = self.get(login, self._current_map).first()
            if record is not None:
                if await self._remote.execute('GetGameMode') == 4:
                    if record.score >= score:
                        return
                else:
                    if record.score <= score:
                        return
                record.score = score
            else:
                record = self.rec_class(
                    score=score,
                    track=self._current_map,
                    player=login
                )
                self._database.session.add(record)
            self._database.session.commit()
            await self._refresh_record_widgets()

    async def unload(self):
        """ Dereferences the widgets. """
        for player in self._database.session.query(self._players.player_class):
            try:
                del player.states[STATE_RECORDS]
            except KeyError:
                pass # o.k, player has no records widget atm
