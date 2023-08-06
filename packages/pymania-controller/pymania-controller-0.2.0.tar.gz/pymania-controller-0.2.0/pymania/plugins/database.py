"""
.. Note::
   This plugin is scalable, i.e. usable in multiple pymania instances.

Stores game data persistently. Registering a table is achieved as follows:

.. code-block:: python

    import sqlalchemy

    class SomeObjectTemplate:
        __tablename__ = 'some_objects'

        field1 = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
        field2 = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

    async def load(self, config, dependencies):
        database = dependencies['database']
        SomeObject = database.add_table(SomeObjectTemplate)

        obj = SomeObject(field1='some', field2='object')
        # session attribute exposes an SQLAlchemy session, allowing to do something like this:
        database.session.add(obj)
        database.session.commit()

.. Important::
   For instantiating objects and executing SQLAlchemy queries *always* use the returned class object
   from `DatabasePlugin.add_table`. The reason is that SQLAlchemy normally requires all table
   classes to inherit from a declarative meta class, which is not made available (creating class
   objects inside the `load` function would get very messy, plus in order to be used outside of
   this function, one needs to assign it to a member anyway). The `add_table` function dynamically
   creates a class object that inherits from the passed table plus the declarative meta class.
"""

import logging
import pathlib

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

import pymania

def _generate_conn_string(config):
    if config['engine'] == 'sqlite':
        path = pathlib.Path(config['host'])
        if not path.is_file():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        return f"sqlite:///{path}"
    return '{}://{}:{}@{}:{}'.format(
        config['engine'],
        config['user'],
        config['password'],
        config['host'],
        config['port']
    )

def _create_database(engine, config):
    if config['engine'] != 'sqlite':
        # we need to re-open the connection because the connection string changed
        engine.execute('create database pymania')
        engine = sqlalchemy.create_engine(
            _generate_conn_string(config) + '/pymania',
            connect_args=config.get('ssl', {})
        )
    return engine

def _get_columns(table):
    for name, member in vars(table).items():
        if isinstance(member, sqlalchemy.Column):
            yield name, member

class DatabasePlugin:
    """ Gives the ability to add tables and exposes a SQLAlchemy engine. """
    version = pymania.__version__
    name = 'database'
    logger = logging.getLogger(__name__)

    __slots__ = 'session', '_engine', '_meta'

    def __init__(self):
        self.session = None
        self._engine = None
        self._meta = None

    async def load(self, config, _dependencies):
        """ Establishes a database connection and adds the player table. """
        ssl = config.get('ssl', {})
        self._meta = sqlalchemy.ext.declarative.declarative_base()
        self._engine = sqlalchemy.create_engine(_generate_conn_string(config), connect_args=ssl)
        self._engine = _create_database(self._engine, config)
        self.session = sqlalchemy.orm.sessionmaker(self._engine)()
        self.logger.info('Established connection to database')

    async def unload(self):
        """ Commits pending changes to the session and destroys it. """
        if self.session is not None:
            self.session.commit()
            self.session.close()
            self.logger.info('Closed session')
        if self._engine is not None:
            self._engine.dispose()
            self.logger.info('Closed connection')

    def add_table(self, table_class):
        """
        Adds a table to the database. Returns a modified version of the table required to execute
        queries with the SQLAlchemy ORM and to instantiate objects thereof.
        """
        # work around limitation that a declarative base cannot be assigned afterwards
        table = type(table_class.__name__, (table_class, self._meta), {})
        self._meta.metadata.create_all(self._engine)
        if self.logger.level <= logging.DEBUG:
            columns = '\n    '.join([f'{x}: {repr(y)}' for x, y in _get_columns(table_class)])
            self.logger.debug('Added table %s:\n    %s\n', table_class.__tablename__, columns)
        return table
