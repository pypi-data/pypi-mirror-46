"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances.

Establishes a remote connection to the dedicated server and wraps basic dedicated functionality in
several methods. It also provides a main loop for use with the controller. Managing the dedicated
server is nice and tidy using the callback decorator:

.. code-block:: python

    database = dependencies['database']
    remote = dependencies['remote']

    @remote.callback('TrackMania.PlayerConnect')
    async def _player_connect(login, _is_spectator):
        self.players[login] = Player(login=login)

    @remote.callback('TrackMania.PlayerDisconnect')
    async def _player_disconnect(login):
        del self.players[login]

    @remote.callback('TrackMania.PlayerInfoChanged')
    async def _player_changed(login, nickname, *_args):
        # ...

For dedicated server reponses that return a simple list of arguments, use the following notation:

.. code-block:: python

    async def handler(arg1, arg2, *_unused_args):
        pass

For responses that return a structure (i.e. a dictionary), use the following notation:

.. code-block:: python

    async def handler(some_kwarg1, some_kwarg2, **_unused_kwargs):
        pass

"""

import asyncio
import collections
import enum
import random
import struct
import logging

import defusedxml.xmlrpc as defused_xmlrpc

import pymania

# patch xmlrpc to fix common exploits
defused_xmlrpc.monkey_patch()

class GameType(enum.Enum):
    """ Defines an enumeration containing all supported game types. """
    FOREVER = enum.auto()

    @classmethod
    def from_string(cls, game_type):
        """
        Retrieves the game type enum value from a string.

        :param str game_type: Type of the game, as returned by gbx_remote.GetVersion()['Name']
        """
        return {'TmForever': cls.FOREVER,}[game_type]

class InvalidDedicatedServer(Exception):
    """ Raised when trying to connect to an invalid dedicated server. """

class DedicatedServer:
    """ Defines a remote connection to the dedicated server. """
    __slots__ = (
        '_identifier',
        '_methods',
        '_game_type',
        '_callbacks',
        '_handlers',
        '_reader',
        '_writer',
        '_listen_task',
        '_exception',
    )

    def __init__(self, identifier='GBXRemote 2'):
        self._identifier = identifier
        self._methods = None
        self._game_type = None
        self._callbacks = collections.defaultdict(set)
        self._handlers = {}
        self._reader = None
        self._writer = None
        self._listen_task = None
        self._exception = Exception()

    async def connect(self, host, port):
        """ Opens a connection to the dedicated server.

        :param str host: Hostname, IP or URL of the dedicated server
        :param int port: Port of the dedicated server
        """
        try:
            self._reader, self._writer = await asyncio.open_connection(host, port)
        except OSError:
            raise InvalidDedicatedServer(f'Unable to connect to dedicated server at {host}:{port}')

        header = struct.unpack_from('<L11s', await self._reader.readexactly(15))[1].decode()
        if header != self._identifier:
            raise InvalidDedicatedServer(f'Invalid dedicated server, got header "{header}"')

    def disconnect(self):
        """ Closes the current connection to the dedicated server. """
        if self._writer is not None:
            self._writer.close()

    def start_listening(self):
        """ Starts listening to incoming messages from the dedicated server.

        :param on_error: Function to execute when a callback raises an exception
        """
        if self._listen_task is None or self._listen_task.cancelled():
            self._listen_task = asyncio.create_task(self._listening_loop())

    async def wait_listening(self):
        """ Waits for the listening task to finish. """
        try:
            await self._listen_task
        except asyncio.CancelledError:
            # this is dodgy, but there seems to be no way to handle the very particular problem of
            # not being able to properly propagate exceptions raised in callbacks to this function
            # in asyncio without using a callback-based approach
            raise self._exception

    def stop_listening(self):
        """ Stops listening to incoming messages. """
        if self._listen_task is not None and not self._listen_task.cancelled():
            self._listen_task.cancel()

    async def _listening_loop(self):
        while True:
            header = await self._reader.readexactly(8)
            size, handler_id = struct.unpack_from('<LL', header)
            response = await self._reader.readexactly(size)
            try:
                exception = None
                data, method = defused_xmlrpc.xmlrpc_client.loads(response, use_builtin_types=True)
                if data is not None and len(data) == 1:
                    data = data[0] # simplify single-value tuple
            except defused_xmlrpc.xmlrpc_client.Fault as exc:
                exception = exc
            try:
                handler = self._handlers.pop(handler_id)
                if exception is None:
                    handler.set_result(data)
                else:
                    handler.set_exception(exception)
            except KeyError:
                # I hate asyncio for making me do callback-based workarounds
                task = asyncio.create_task(self._handle_callback(method, data))
                task.add_done_callback(self._on_error)

    async def get_available_methods(self):
        """ Gets all available methods. Caches the result. """
        if self._methods is None:
            self._methods = await self.execute('system.listMethods')
        return self._methods

    async def get_game_type(self):
        """ Gets the game type of the dedicated server. Caches the result. """
        if self._game_type is None:
            info = await self.execute('GetVersion')
            try:
                game_name = info['Name']
                self._game_type = GameType.from_string(game_name)
            except KeyError:
                raise InvalidDedicatedServer(f'Unsupported game client "{game_name}"')
        return self._game_type

    async def execute(self, method_name, *args, **kwargs):
        """ Executes a method on the dedicated server and returns its response.

        :param str method_name: XML-RPC method to execute
        :param args: Arguments to pass to the XML-RPC method
        :param kwargs: timeout: Time in seconds to wait for a response
        :return: Tuple containing the response data
        """
        byte_order = 'little'
        handler_id = self._generate_handler_id()
        request_data = defused_xmlrpc.xmlrpc_client.dumps(
            args,
            methodname=method_name,
            allow_none=True
        ).encode()

        self._writer.write(
            len(request_data).to_bytes(4, byteorder=byte_order) +
            handler_id.to_bytes(4, byteorder=byte_order) +
            request_data
        )

        if not self._listen_task.cancelled():
            # if listening task is cancelled, still allow plugins to execute methods without waiting
            # for a response
            self._handlers[handler_id] = future = asyncio.get_event_loop().create_future()
            return await asyncio.wait_for(future, kwargs.get('timeout', 10))

    async def _handle_callback(self, method, data):
        for handler in self._callbacks[method]:
            if isinstance(data, dict):
                await handler(**data)
            elif isinstance(data, tuple):
                await handler(*data)
            else:
                await handler(data)

    def _on_error(self, task):
        if task.exception() is not None:
            self._exception = task.exception()
            self._listen_task.cancel()

    def _generate_handler_id(self):
        min_handler = 2147483648
        max_handler = 4294967295

        # prevent handler ID collision
        while True:
            handler_id = random.randint(min_handler, max_handler)
            if handler_id not in self._handlers:
                return handler_id

class RemotePlugin:
    """
    Establishes a remote connection to the dedicated server and wraps several XML-RPC methods for
    convenient use. It also manages the current players on the server.
    """
    version = pymania.__version__
    name = 'remote'
    logger = logging.getLogger(__name__)

    __slots__ = '_exception', '_listen_task', '_dedicated'

    def __init__(self):
        self._exception = pymania.ControllerInterrupt(pymania.ControllerState.SHUTDOWN, '')
        self._listen_task = None
        self._dedicated = None

    async def load(self, config, _dependencies):
        """ Establishes a connection to the dedicated server and authenticates against it. """
        try:
            self._dedicated = DedicatedServer(identifier=config['id'])
            await self._dedicated.connect(config['host'], config['port'])
        except InvalidDedicatedServer as exc:
            self.logger.error(str(exc))
            raise pymania.ControllerInterrupt(pymania.ControllerState.SHUTDOWN, exc)
        try:
            self._dedicated.start_listening()
            await self.execute('Authenticate', config['user'], config['password'])
        except defused_xmlrpc.xmlrpc_client.Fault as exc:
            self.logger.error('Unable to authenticate to dedicated server. Reason: %s', str(exc))
            raise pymania.ControllerInterrupt(pymania.ControllerState.SHUTDOWN, exc)
        if not await self.execute('EnableCallbacks', True):
            msg = 'Unable to enable callbacks'
            self.logger.error(msg)
            raise pymania.ControllerInterrupt(pymania.ControllerState.SHUTDOWN, msg)

    async def unload(self):
        """ Disconnects from the dedicated server. """
        if self._dedicated is not None:
            self._dedicated.stop_listening()
            self._dedicated.disconnect()
            self._dedicated = None

    async def main(self):
        """
        Waits for the listen task to finish, be it through a controller interrupt or something else.
        """
        await self._dedicated.wait_listening()


    async def send_message(self, message, recipients=None):
        """ Sends a message to all given logins. Empty list or None means all players.

        :param str message: Message to send
        :param list/str recipients: One or multiple logins
        """
        if recipients:
            if isinstance(recipients, list):
                recipients = ','.join(recipients)
            return await self.execute('ChatSendServerMessageToLogin', message, recipients)
        return await self.execute('ChatSendServerMessage', message)

    async def execute(self, method_name, *args):
        """ Conveniently wraps the dedicated server execute function.

        :param str method_name: XML-RPC method to execute
        :param args: Arguments to pass to method call
        """
        return await self._dedicated.execute(method_name, *args)

    def callback(self, callback_name):
        """
        Intercept the callback with the given name. Note that the arguments are unpacked before the
        handler is invoked. This is a convenience feature to use arguments by name immediately
        since it is a hassle to access the data tuple by indices.

        Use as follows:

        .. code-block:: python

            def load(self, config, dependencies):
                remote = dependencies['remote']

                @remote.callback('Trackmania.PlayerChat')
                async def chat(args):
                    await asyncio.gather(remote.send_message('something'))

        :param callback_name: Name of the callback to intercept
        """
        def _decorator(function):
            #pylint: disable-msg=protected-access
            self._dedicated._callbacks[callback_name].add(function)
            return function
        return _decorator
