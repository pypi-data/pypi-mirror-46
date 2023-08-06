"""
.. Note::
   This plugin is not scalable.

Manipulates player privileges.
"""

import pymania

from pymania.plugins.chat import CommandParser

class PrivilegeManagementPlugin:
    """ Manipulates player privileges. """
    version = pymania.__version__
    name = 'privileges'
    depends = {'remote', 'chat', 'players'}

    async def load(self, config, dependencies):
        """ Registers a chat command that allows altering the privileges. """
        chat = dependencies['chat']
        remote = dependencies['remote']
        players = dependencies['players']
        Privilege = config['privilege_class'] # pylint: disable=invalid-name

        # pylint: disable=line-too-long
        parser = CommandParser('privileges', description='Modify privileges')
        parser.add_argument('login', nargs='?', help='Login of the player to modify privileges of')
        parser.add_argument('--add', metavar='PRIV', nargs='*', help='Add privilege(s) to the player')
        parser.add_argument('--remove', metavar='PRIV', nargs='*', help='Remove privilege(s) from the player')
        parser.add_argument('--get', action='store_true', help="Retrieves the player's privileges")
        parser.add_argument('--available', action='store_true', help='Lists available privileges')

        @chat.command(parser, config['modify_privileges'])
        async def _privilege_command(player, **kwargs):
            login = kwargs['login']
            if not login and not kwargs['available']:
                await remote.send_message(config['usage'], player.login)
                return
            if kwargs['available']:
                flags = ', '.join([str(x).rsplit('.', 2)[1] for x in Privilege])
                await remote.send_message(config['flags'].format(flags=flags), player.login)
                return
            instance = players.get(login)
            if instance is None:
                msg = config['invalid_player'].format(login=login)
                await remote.send_message(msg, player.login)
                return
            if kwargs['get']:
                flags = pymania.enum_to_list(Privilege(int(instance.privileges)))
                msg = config['player_flags'].format(player=instance.nickname, flags=flags)
                await remote.send_message(msg, player.login)
            else:
                flags = Privilege(0)
                for add in kwargs['add'] or []:
                    try:
                        flags = flags | Privilege[add]
                    except KeyError:
                        msg = config['invalid_privilege'].format(flag=add)
                        await remote.send_message(msg, player.login)
                        return
                if flags.value != 0:
                    instance.privileges = str(int(instance.privileges) | flags.value)
                    players.database.session.commit()
                    msg = config['add_privilege'].format(
                        granter=player.nickname,
                        player=instance.nickname,
                        flags=pymania.enum_to_list(flags)
                    )
                    await remote.send_message(msg, player.login)

                flags = Privilege(0)
                for remove in kwargs['remove'] or []:
                    try:
                        flags = flags | Privilege[remove]
                    except KeyError:
                        msg = config['invalid_privilege'].format(flag=remove)
                        await remote.send_message(msg, player.login)
                        return
                if flags.value != 0:
                    instance.privileges = str(int(instance.privileges) & ~flags.value)
                    players.database.session.commit()
                    msg = config['remove_privilege'].format(
                        granter=player.nickname,
                        player=instance.nickname,
                        flags=pymania.enum_to_list(flags)
                    )
                    await remote.send_message(msg, player.login)
