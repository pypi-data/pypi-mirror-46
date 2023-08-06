#!/usr/bin/env python3

"""
Spawns a controller instance with the given configuration.
"""

import os
import argparse
import asyncio
import importlib
import logging
import logging.handlers
import pathlib
import signal
import sys
import traceback

import pymania

def topological_plugin_sort(plugins):
    remaining = {k: set(v.depends) for k, v in plugins.items()}
    while remaining:
        missing_deps = {i for v in remaining.values() for i in v} - remaining.keys()
        if missing_deps:
            raise ImportError(f'Dependencies {missing_deps} do not exist')

        missing_deps = {k for k, v in remaining.items() if not v}
        if not missing_deps:
            raise RecursionError(f'Circular dependency in {remaining} detected')
        yield missing_deps

        remaining = {k: set(v) - missing_deps for k, v in remaining.items() if v}

def get_plugin_class(path, state):
    path = path.rsplit('.', 1)
    module = importlib.import_module(path[0])
    if state & pymania.ControllerState.RELOAD_PLUGINS:
        importlib.reload(module)
    return getattr(module, path[1])

class ControllerInstance:
    name = 'controller'
    logger = logging.getLogger('controller')

    def __init__(self, state, config):
        self.config = config
        self.plugins = self.get_plugin_instances(state)
        self.sorted_plugins = list(topological_plugin_sort(self.plugins))
        self.assign_logging_handler(self)

    async def __aenter__(self):
        for parallel in self.sorted_plugins:
            await asyncio.gather(*[self.load_plugin(x) for x in parallel])
        return self

    async def __aexit__(self, exc_type, exc_value, tback):
        await self.terminate()
        if exc_type is not None and exc_type not in (KeyboardInterrupt,):
            msg = ''.join(traceback.format_exception(exc_type, exc_value, tback))
            self.logger.critical('Unhandled exception thrown: %s', msg)

    async def terminate(self):
        for parallel in reversed(self.sorted_plugins):
            await asyncio.gather(*[self.unload_plugin(x) for x in parallel])

    async def run(self):
        coros = []
        for instance in self.plugins.values():
            try:
                coros.append(getattr(instance, 'main')())
            except AttributeError:
                pass # o.k, no main loop
        try:
            await asyncio.gather(*coros)
            return pymania.ControllerState.SHUTDOWN
        except pymania.ControllerInterrupt as interrupt:
            self.logger.info(
                'Controller interrupt received. Flags: %s; Reason: %s',
                str(interrupt.flags),
                str(interrupt)
            )
            return interrupt.flags

    async def load_plugin(self, name):
        instance = self.plugins[name]
        await instance.load(self.config['plugins'][instance.module_name], {
            x.name: x
            for x in self.plugins.values()
            if x.name in instance.depends
        })

    async def unload_plugin(self, name):
        try:
            await self.plugins[name].unload()
        except AttributeError:
            pass # o.k, plugin has nothing to clean up

    def assign_logging_handler(self, plugin):
        try:
            config = self.config['logging']
            logger = plugin.logger
        except AttributeError:
            return # o.k, no logging/loggers configured

        path = pathlib.Path(config['directory'])
        path.mkdir(parents=True, exist_ok=True)
        path = path / (plugin.name + '.log')
        handler = logging.handlers.RotatingFileHandler(
            path,
            mode='a',
            maxBytes=config['max_bytes'],
            backupCount=config['max_backups']
        )
        handler.setFormatter(logging.Formatter(config['format']))
        for i in logger.handlers[:]:
            logger.removeHandler(i)
        logger.addHandler(handler)
        logger.setLevel(config['level'])

    def get_plugin_instances(self, state):
        instances = {}
        for path in self.config['plugins'].keys():
            klass = get_plugin_class(path, state)
            self.assign_logging_handler(klass)
            setattr(klass, 'module_name', path)
            if not hasattr(klass, 'depends'):
                setattr(klass, 'depends', tuple())
            instances[klass.name] = klass()
        return instances

def load_config_module(state, file_):
    file_ = pathlib.Path(file_)
    if not file_.is_file():
        raise FileNotFoundError(file_)
    dir_ = str(file_.parent)
    if dir_ not in sys.path:
        sys.path.append(dir_)
    module = importlib.import_module(file_.stem)
    if state & pymania.ControllerState.RELOAD_CONFIG:
        importlib.reload(module)
    return module

async def main(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config_file', help='Configuration Python script to use')
    namespace = parser.parse_args(args)
    current_instance = None
    state = pymania.ControllerState.STARTUP

    def handle_terminate():
        if current_instance is not None:
            msg = ''.join(traceback.format_exception(*sys.exc_info()))
            current_instance.logger.critical('Controller was terminated forcefully: %s', msg)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(loop.create_task(current_instance.terminate()))

    signal.signal(signal.SIGTERM, handle_terminate)
    if os.name == 'nt':
        # HACK: Windows does not support KeyboardInterrupt together with asyncio loops
        # Apparently resolved in Python 3.8
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    else:
        signal.signal(signal.SIGINT, handle_terminate)

    while not state & pymania.ControllerState.SHUTDOWN:
        config = vars(load_config_module(state, namespace.config_file))
        async with ControllerInstance(state, config) as instance:
            current_instance = instance
            state = await instance.run()

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
