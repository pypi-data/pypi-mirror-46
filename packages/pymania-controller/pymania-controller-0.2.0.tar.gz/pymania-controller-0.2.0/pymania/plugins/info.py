"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances, but might print multiple
   messages at the same time at some point.

Broadcasts an info message every X seconds.
"""

import asyncio
import random
import pymania

class InfoPlugin:
    """ Broadcasts info messages. """
    version = pymania.__version__
    name = 'info'
    depends = {'remote'}
    __slots__ = '_config', '_remote'

    def __init__(self):
        self._config = None
        self._remote = None

    async def load(self, config, dependencies):
        """ Copy config and remote dependency. """
        self._config = config
        self._remote = dependencies['remote']

    async def main(self):
        """ Broadcasts after every configured amount of seconds. """
        while True:
            await asyncio.sleep(self._config['interval'])
            await self._remote.send_message(random.choice(self._config['messages']))
