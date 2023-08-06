import unittest

from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database

from fasvaorm import init_engine, init_session_factory, init_session, close_session
from fasvaorm.models import Base

# check if running in gitlab-ci
import os

host = os.environ.get('GITLAB_CI')

if host is None:
    # local testing
    host = '127.0.0.1'
    user = 'testing'
else:
    host = 'mysql'
    user = 'root'


TEST_DB_CONFIG = {
    'user': user,
    'host': host,
    'database': 'testing',
    'password': 'mysql'
}

DB_URL = url = "mysql+pymysql://{user}:{password}@{host}/{database}".format(**TEST_DB_CONFIG)


class EngineTestCase(unittest.TestCase):

    def setUp(self):

        # create the test database
        try:
            create_database(DB_URL)
        except ProgrammingError:
            pass

        self.engine = init_engine(DB_URL,
                                  # unlimited number of connections
                                  pool_size=0,
                                  # set connection timeout to 50 minutes
                                  pool_timeout=300)

        init_session_factory(self.engine)
        self.session = init_session()

    def tearDown(self):
        close_session()

        Base.metadata.drop_all()
