import unittest

from fasvaorm import get_session, EngineNotInitializedError, init_engine, init_session_factory, init_session, \
    set_engine, cleanup
from tests.base import DB_URL


class TestCreateSessionWithoutEngine(unittest.TestCase):

    def setUp(self):
        super().setUp()

        cleanup()

    def test_get_session_without_engine_initialization(self):
        """
        Test if the EngineNotInitializedError is raised if we try to get a session without initialization.
        """
        with self.assertRaises(EngineNotInitializedError):
            get_session()


class TestCreateSessionWithEngine(unittest.TestCase):

    def setUp(self):
        super().setUp()

        cleanup()

    def test_get_session_with_engine_without_factory(self):
        """
        Test if we can get a session with an initialized engine but without a session factory.
        """

        engine = init_engine(url=DB_URL)
        self.assertIsNotNone(engine)

        session = get_session()
        self.assertIsNotNone(session)

    def test_get_session_with_engine_and_factory(self):
        engine = init_engine(url=DB_URL)
        self.assertIsNotNone(engine)

        factory = init_session_factory(engine=engine)
        self.assertIsNotNone(factory)

        session = init_session(factory=factory)
        self.assertIsNotNone(session)

        session2 = get_session()
        self.assertEqual(session, session2)

    def tearDown(self):
        set_engine(None)
