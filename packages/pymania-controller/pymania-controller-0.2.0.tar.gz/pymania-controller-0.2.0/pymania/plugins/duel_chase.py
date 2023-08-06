"""
.. Note::
   This plugin is not scalable.

Duel chase cup plugin.
"""

import asyncio
import enum
import pathlib
import random
import pymania

from pymania.plugins.chat import CommandParser

class _State(enum.Enum):
    STOPPED = enum.auto()
    RUNNING = enum.auto()
    PAUSED = enum.auto()

class DuelChasePlugin: # pylint: disable=too-many-instance-attributes
    """ Manages the duel-chase cup. """
    version = pymania.__version__
    name = 'duel_chase'
    depends = 'chat', 'remote', 'players'

    def __init__(self):
        self.chat = None
        self.remote = None
        self.players = None
        self.config = {}
        self.state = _State.STOPPED
        self.participants = []
        self.maps = []
        self.duelists = []
        self.current_stage = 1
        self.total_cps = 0
        self.duel_started = False
        self.is_warmup = False
        self.warmup_task = None
        self.skip_task = None

    async def load(self, config, dependencies):
        """ Register help chat command. """
        self.chat = dependencies['chat']
        self.remote = dependencies['remote']
        self.players = dependencies['players']
        self.config = config
        adm = config['admin_privilege']

        @self.chat.command(CommandParser('duel-start', description='Start the duel chase cup'), adm)
        async def _start_command(player):
            if self.state == _State.STOPPED:
                self.state = _State.RUNNING # we need this
                await self._start(player)
            else:
                self.state = _State.RUNNING

        @self.chat.command(CommandParser('duel-stop', description='Stop the duel chase cup'), adm)
        async def _stop_command(player):
            if self.state != _State.STOPPED:
                await self._stop(player)
            self.state = _State.STOPPED

        @self.chat.command(CommandParser('duel-pause', description='Pause the duel chase cup'), adm)
        async def _pause_command(player):
            if self.state == _State.RUNNING:
                await self._pause(player)
                self.state = _State.PAUSED

        @self.chat.command(CommandParser('duel-skip', description='Skip one duel'), adm)
        async def _duel_skip(player):
            if self.state == _State.RUNNING:
                await self.remote.send_message(self.config['msg_duel_skip'].format(player.nickname))
                await self._safe_skip()

        @self.remote.callback('TrackMania.EndRound')
        async def _begin_round():
            if self.state == _State.RUNNING:
                self.is_warmup = False

        @self.remote.callback('TrackMania.BeginChallenge')
        async def _begin_challenge(challenge, warmup, _continuation):
            if self.state == _State.RUNNING:
                self.total_cps = challenge['NbCheckpoints']
                await self._begin_challenge(warmup)

        @self.remote.callback('TrackMania.EndChallenge')
        async def _end_challenge(_rankings, _challenge, _warmup, _continue, _res):
            if self.state == _State.RUNNING:
                await self._end_challenge()

        @self.remote.callback('TrackMania.PlayerCheckpoint')
        async def _checkpoint(_uid, login, _time, lap, checkpoint):
            if self.state == _State.RUNNING:
                await self._checkpoint(self.players.get(login), lap, checkpoint)

        @self.remote.callback('TrackMania.PlayerConnect')
        async def _connect(login, _):
            if self.state == _State.RUNNING:
                player = self.players.get(login)
                if player not in self.participants:
                    msg = self.config['msg_connect_progress'].format(player=player.nickname)
                    await self.remote.execute('ForceSpectator', player.login, 1)
                elif player.stage < self.current_stage:
                    msg = self.config['msg_connect_outdated'].format(player=player.nickname)
                    await self.remote.execute('ForceSpectator', player.login, 1)
                else:
                    msg = self.config['msg_connect_eligible'].format(player=player.nickname)
                    player.here = True
                await self.remote.send_message(msg)

        @self.remote.callback('TrackMania.PlayerDisconnect')
        async def _disconnect(login):
            if self.state == _State.RUNNING:
                player = self.players.get(login)
                if player in self.participants:
                    player.here = False
                if player in self.duelists and self.duel_started:
                    self._mark_as_winner([x for x in self.duelists if x is not player][0])

    def _rotate_maps(self):
        self.maps[:] = self.maps[-1:] + self.maps[:-1]

    async def _post_cup(self):
        async for i in self.players.get_on_server():
            await self.remote.execute('ForceSpectator', i.login, 0)

    async def _start(self, player):
        self.current_stage = 1
        self.participants = []
        async for i in self.players.get_on_server():
            self.participants.append(i)
            i.stage = 1
            i.here = True
        await self.remote.send_message(self.config['msg_start'].format(player=player.nickname))

        self.maps = []
        map_dir = self.config['map_folder']
        map_root = pathlib.Path(await self.remote.execute('GetTracksDirectory'))
        for i in (map_root / map_dir).glob('*.gbx'):
            self.maps.append(str(pathlib.Path(map_dir) / i.name))
        random.shuffle(self.maps)

        # dodgy; for now, do not store and reset old settings
        await self.remote.execute('SetForceShowAllOpponents', 1)
        await self.remote.execute('SetGameMode', 0)
        await self.remote.execute('SetRoundForcedLaps', 99)
        await self.remote.execute('SetAllWarmUpDuration', 1)
        await self.remote.execute('SetWarmUp', True)
        await self.remote.execute('InsertChallengeList', self.maps)
        await self.remote.execute('ChooseNextChallenge', self.maps[0])

        if (await self.remote.execute('GetStatus'))['Code'] == 5: # scoreboard
            await self._end_challenge() # must simulate this on scoreboard
        else:
            await self.remote.execute('NextChallenge')
        await self.remote.send_message(self.config['msg_new_stage'].format(self.current_stage))

    async def _safe_skip(self):
        try:
            await self.remote.execute('NextChallenge')
        except Exception: # pylint: disable=broad-except
            timeout = self.config['deferred_skip_seconds']
            asyncio.get_event_loop().create_task(self._deferr_skip(timeout))
            await self.remote.send_message(self.config['map_deferred_skip'].format(timeout))

    async def _stop(self, player):
        await self._post_cup()
        await self.remote.send_message(self.config['msg_stop'].format(player=player.nickname))

    async def _pause(self, player):
        await self.remote.send_message(self.config['msg_pause'].format(player=player.nickname))

    def _get_ranking(self):
        def _encode_score(x):
            return x.current_lap * self.total_cps + x.current_cp
        return sorted(self.duelists, key=_encode_score, reverse=True)

    async def _remove_participant(self, participant):
        try:
            self.participants.remove(participant)
            if participant.here:
                await self.remote.execute('ForceSpectator', participant.login, 1)
        except ValueError:
            pass # o.k., not participating

    async def _end_challenge(self):
        if self.skip_task:
            self.skip_task.cancel()
            self.skip_task = None

        if self.duelists:
            winner, loser = tuple(self._get_ranking())
            winner.stage += 1
            msg = self.config['msg_duel_end'].format(winner=winner.nickname, loser=loser.nickname)
            await self._remove_participant(loser)
            await self.remote.send_message(msg)
        if len(self.participants) == 1:
            self.state = _State.STOPPED
            msg = self.config['msg_winner'].format(player=self.participants[0].nickname)
            await self.remote.send_message(msg)
            await self._post_cup()
            return

        remaining = [x for x in self.participants if x.stage == self.current_stage]
        if len(remaining) == 1:
            msg = self.config['msg_free_win'].format(player=remaining[0].nickname)
            await self.remote.send_message(msg)
        if len(remaining) < 2 and len(remaining) != len(self.participants):
            self.current_stage += 1
            await self.remote.send_message(self.config['msg_new_stage'].format(self.current_stage))
            remaining = self.participants
        self.duelists = random.sample(set(remaining), 2)

        for i in self.duelists:
            i.current_lap = 0
            i.current_cp = -1
            await self.remote.execute('ForceSpectator', i.login, 2)
        for i in [x for x in self.participants if x not in self.duelists]:
            if i.here:
                await self.remote.execute('ForceSpectator', i.login, 1)
        self.duel_started = False
        await self.remote.send_message(self.config['msg_duel_start'].format(
            player1=self.duelists[0].nickname,
            player2=self.duelists[1].nickname
        ))

    async def _deferr_skip(self, timeout):
        await asyncio.sleep(timeout)
        await self.remote.execute('NextChallenge')

    async def _warmup(self, timeout):
        await asyncio.sleep(timeout)
        if self.is_warmup:
            await self.remote.send_message(self.config['msg_warmup_over'])
            await self.remote.execute('ForceEndRound')

    async def _mark_as_winner(self, player):
        player.current_cp = self.config['cp_win_difference'] + 1
        msg = self.config['msg_duel_quit'].format(
            quitter=[x for x in self.duelists if x is not player][0].nickname,
            winner=player.nickname
        )
        await self.remote.send_message(msg)
        await self._safe_skip()


    async def _begin_challenge(self, warmup):
        self.duel_started = True
        still_there = [x for x in self.duelists if x.here]
        if not still_there:
            await self.remote.send_message(self.config['msg_both_left'])
            await self._safe_skip()
        if len(still_there) == 1:
            await self._mark_as_winner(still_there[0])
            return

        if warmup:
            self.is_warmup = True
            timeout = self.config['warmup_seconds']
            self.warmup_task = asyncio.get_event_loop().create_task(self._warmup(timeout))
            await self.remote.send_message(self.config['msg_warmup'].format(timeout))

    async def _checkpoint(self, player, lap, checkpoint):
        if self.is_warmup:
            return

        player.current_lap = lap
        player.current_cp = checkpoint
        other = [x for x in self.duelists if x is not player][0]

        if lap >= other.current_lap:
            player_total = self.total_cps * lap + checkpoint
            other_total = self.total_cps * other.current_lap + other.current_cp
            if player_total - other_total >= self.config['cp_win_difference']:
                self._rotate_maps()
                await self.remote.execute('ChooseNextChallenge', self.maps[0])
                await self._safe_skip()
