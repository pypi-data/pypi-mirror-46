"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances.

Handles chat commands and the visual appearance of messages. Registering a chat command is as simple
as follows:

.. code-block:: python

    chat = dependencies['chat']
    remote = dependencies['remote']
    players = dependencies['players']

    parser = chat.CommandParser('hi')
    parser.add_argument('login', nargs='?', help='Login of the player to say hi to')

    @chat.command(parser, config['privilege_to_say_hi'])
    async def say_hi(from_, login): # from is always a Player object
        if login is not None:
            player = players.get(login)
            if player is None:
                await remote.send_message(f'{login} is not a valid player', from_.login)
            else:
                await remote.send_message(f'Hello {player.nickname}!')
        else:
            await remote.send_message(f'Hello everyone!')

The CommandParser is a subclass of Pythons `ArgumentParser` that overrides the default error and
help behavior to better integrate with chat commands. Using it has multiple advantages:

- The argument name determines the name of the corresponding keyword argument in the handler
- Automatically generate help for that command
- Rapidly make something that just works

"""

import re
import argparse
import collections
import logging
import shlex

import defusedxml.xmlrpc as defused_xmlrpc

import pymania

_Command = collections.namedtuple('Command', ['argparser', 'privileges', 'handler', 'sub_privs'])
_CommandData = collections.namedtuple('CommandData', ['help', 'usage', 'privileges'])

class _HelpError(Exception):
    def __init__(self, usage):
        super().__init__()
        self.usage = usage

class _CommandError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

# pylint: disable=protected-access
class _CustomSubParserAction(argparse._SubParsersAction):
    def add_parser(self, name, **kwargs):
        parser = super().add_parser(name, **kwargs)
        parser.set_defaults(command=name)
        return parser

class _CustomHelpAction(argparse.Action):
    def __init__(self, **kwargs):
        super().__init__(nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        raise _HelpError(parser.format_usage())

def _parser_error(message):
    raise _CommandError(message)

def _prepare_usage(usage, prefix=''):
    return re.sub(r'\s+', ' ', usage.replace('usage: ', prefix).replace('\n', ''))

def get_command_data(commands):
    """ Get information (help, usage, privileges) about all commands. """
    return [
        _CommandData(
            help=x.argparser.description,
            usage=_prepare_usage(x.argparser.format_usage()),
            privileges=pymania.enum_to_list(x.privileges or x.sub_privs)
        )
        for x
        in commands
    ]

class CommandParser(argparse.ArgumentParser):
    """ Overrides the help and error action. """
    def __init__(self, command=None, **kwargs):
        if 'prog' not in kwargs:
            kwargs['prog'] = command
        super().__init__(add_help=False, **kwargs)
        self.error = _parser_error
        self.add_argument('-h', '--help', default=argparse.SUPPRESS, action=_CustomHelpAction)
        self.register('action', 'parsers', _CustomSubParserAction)

class PrivilegeError(Exception):
    """ Raised by chat commands that need even more fine-grained privileges. """
    def __init__(self, privileges):
        super().__init__()
        self.privileges = privileges

class MissingOptionsError(Exception):
    """ Raised by chat commands that need at least one of the optional arguments to be provided. """
    def __init__(self, command):
        super().__init__()
        self.command = command

class ChatPlugin:
    """ Manages chat commands and chat messages in general. """
    version = pymania.__version__
    name = 'chat'
    depends = 'remote', 'players'
    logger = logging.getLogger(__name__)

    __slots__ = 'commands', '_route_default_chat'

    def __init__(self):
        self.commands = {}
        self._route_default_chat = True

    async def load(self, config, dependencies):
        """ Creates a handler for the TrackMania.PlayerChat callback. """
        remote = dependencies['remote']
        players = dependencies['players']

        # disable sending the default-formatted message by the dedicated server
        try:
            await remote.execute('ChatEnableManualRouting', True, True)
        except defused_xmlrpc.xmlrpc_client.Fault:
            self._route_default_chat = False # prevent duplicated 'default' chat messages

        @remote.callback('TrackMania.PlayerChat')
        async def _chat(_uid, login, text, *_args):
            text = text.strip()
            player = players.get(login)

            if not text or not int(player.privileges) & config['privilege'].value:
                return # prevent spamming empty and a muted player's messages
            prefix = config['command_prefix']
            if not text.startswith(prefix) and self._route_default_chat: # normal chat message
                msg = config['message'].format(player=player.nickname, message=text)
                await remote.send_message(msg, login)
                return
            args = shlex.split(text[len(prefix):])
            if not args:
                return # an empty command is not worth notifying of

            try:
                cmd = self.commands[args[0]]
            except KeyError:
                await remote.send_message(config['invalid_command'].format(command=args[0]), login)
                return

            if cmd.privileges is not None and not player.has_privileges(cmd.privileges):
                msg = config['missing_privilege'].format(privileges=cmd.privileges, command=args[0])
                await remote.send_message(msg, login)
                return

            try:
                args = args[1:]
            except IndexError:
                args = []
            try:
                await cmd.handler(player, **vars(cmd.argparser.parse_args(args)))
            except _CommandError as exc:
                msg = config['command_error'].format(message=exc.message)
                await remote.send_message(msg, login)
            except _HelpError as exc:
                usage = _prepare_usage(exc.usage, prefix)
                await remote.send_message(config['command_usage'].format(usage=usage), login)
            except PrivilegeError as exc:
                msg = config['missing_privilege'].format(privileges=exc.privileges, command=args[0])
                await remote.send_message(msg, login)
            except MissingOptionsError as exc:
                msg = config['missing_options'].format(command=exc.command)
                await remote.send_message(msg, login)

    async def unload(self):
        """ Clears all commands. """
        self.commands.clear()

    def command(self, parser, privileges=None, sub_privs=None):
        """ Adds a command.

        :param parser: CommandParser to use for parsing the arguments
        :param privileges: Required privilege(s) to execute the command
        """
        def _decorator(function):
            self.commands[parser.prog] = _Command(parser, privileges, function, sub_privs)
            self.logger.info('Registered chat command "%s"', parser.prog)
            return function
        return _decorator
