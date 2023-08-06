# -*- tab-width: 4; encoding: utf-8; -*-
# ex: set tabstop=4 expandtab:
# Copyright (c) 2016-2018 by Lars Klitzke, Lars.Klitzke@hs-emden-leer.de.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import argparse

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine as SQLAlchemyEngine

# A global database factory
from sqlalchemy.exc import InternalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLALchemySession
from sqlalchemy_utils import create_database

from fasvaorm.models import *

SessionFactory = None

# The global database session
DBSession = None

# The global database SQLAlchemy engine
Engine = None


class EngineNotInitializedError(RuntimeError):
    pass


def cleanup():
    """
    Remove all references.
    """
    global DBSession, SessionFactory, Engine

    DBSession = None
    SessionFactory = None
    Engine = None


def get_session(new=False):
    """
    Get the current active session or create a new one

    Returns:
        SQLALchemySession: The current active global session

    """

    if new:
        factory = get_session_factory()

        return factory()
    else:
        global DBSession

        # check if the global session is initialized
        if not DBSession:
            # if this is not the case, setup a session
            DBSession = init_session()

        return DBSession


def get_session_factory():
    """
    Get the current active session factory

    Returns:
        sessionmaker: The session factory
    """

    global SessionFactory

    # verify that the session is initialized
    if not SessionFactory:
        # otherwise setup the session factory
        SessionFactory = init_session_factory()

    return SessionFactory


def get_engine():
    """
    Get the current active engine

    Returns:
        Engine: The current engine
    """
    global Engine
    return Engine


def initialize_engine(engine):
    """
    Initialize the database of the given engine
    Args:
        engine (SQLAlchemyEngine): The engine to initialize

    """
    # try to create the database
    create_database(str(engine.url))

    # create all tables
    Base.metadata.create_all(engine)


def set_engine(engine):
    """
    Set the current active engine

    Args:
        engine (SQLAlchemyEngine): The new global engine
    """

    global Engine
    Engine = engine

    if Engine is not None:
        # setup bindings and create tables
        Base.metadata.bind = Engine

        try:
            Base.metadata.create_all(Engine)
        except InternalError as e:
            if 'Unknown database' in e.orig.args[1]:

                initialize_engine(Engine)

        # update the tables
        Base.metadata.reflect(Engine)


def init_engine(url, **kwargs):
    """
    Initialize the global SQLAlchemy database engine

    Args:
        url (str):  URL to connect with
        **kwargs:   Arguments passed to the `create_engine()` function.

    Returns:
        SQLAlchemyEngine: The global engine
    """
    engine = get_engine()

    # only init the global engine once
    if not engine:
        engine = create_engine(url, **kwargs)

    set_engine(engine)

    return engine


def init_session_factory(engine=None):
    """
    Initialize the global database session factory

    Args:
        engine (SQLAlchemyEngine): The SQLALchemy engine

    Returns:
        sessionmaker: The session factory to create sessions with

    Raises:
        EngineNotInitializedError: If the passed engine (if defined) or the global engine is not initialized.
    """

    if not engine:
        engine = get_engine()

    if not engine:
        raise EngineNotInitializedError('Either pass a engine to use or initialize the global engine.')

    global SessionFactory

    # only init the global session factory once
    if not SessionFactory:
        SessionFactory = sessionmaker(bind=engine)

    return SessionFactory


def init_session(factory=None):
    """
    Initialize the global SQLAlchemy database session

    Args:
        factory (sessionmaker): The session maker to create the session with

    Returns:
        SQLALchemySession: The global database session
    """
    if not factory:
        factory = get_session_factory()

    global DBSession
    # only init the global session once
    if not DBSession:
        DBSession = factory()

    return DBSession


def close_session(session=None):
    """
    Closes either the given or the global session.

    Args:
        session (SQLAlchemySession): The sesssion to close
    """
    if not session:
        session = get_session()

    session.flush()
    session.close()


def parse_arguments():
    """ Parses the arguments the user passed to this script """

    arg_parser = argparse.ArgumentParser(description="""Initialize a database.""")

    arg_parser.add_argument('--config', help="""
        Configuration file for database configuration and enrichment parametrisation""", required=False)

    arg_parser.add_argument('--log-level', help="""
        defines which messages should be logged (INFO, DEBUG, WARNING, ERROR).
        For further modes see the logging class.
        """, default='INFO', choices=['INFO', 'DEBUG', 'WARNING', 'ERROR'])

    return arg_parser.parse_args()


def initialize_database():
    """
    Initialize a database using parameters defined as program arguments
    """

    import os
    import sys
    import pymodconf as mc

    # Section for the information about the database
    database = "Database"

    mapping = {
        database: [
            "host",
            "port",
            "user",
            "password",
        ]
    }

    arguments = parse_arguments()

    config_file_name = arguments.config

    # load the configuration
    if not config_file_name:
        # we assume that the configuration file is in our
        config_file_name = os.path.join(sys.prefix, 'share', 'fasva', 'fasva.cfg')

    config = mc.parser.load(config_file_name, mapping)

    url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(**config[database])

    init_engine(url)


if __name__ == '__main__':
    initialize_database()
