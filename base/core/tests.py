from flask import current_app
from flask_testing import TestCase
from flask_mixer import Mixer

from ..ext import db


class QueriesContext():
    """ Test's tool for check database queries.

        >>> with self.assertNumQueries(4):
        >>>     do_something()
    """

    def __init__(self, num, testcase):

        self.num = num
        self.echo = None
        self.testcase = testcase
        self.start = 0

    def __enter__(self):
        from flask_sqlalchemy import get_debug_queries

        self.start = len(get_debug_queries())
        self.echo = db.engine.echo
        db.engine.echo = True

    def __exit__(self, exc_type, exc_value, traceback):
        db.engine.echo = self.echo
        if exc_type is not None:
            return

        from flask_sqlalchemy import get_debug_queries

        executed = len(get_debug_queries()) - self.start
        self.testcase.assertEqual(
            executed, self.num, "%d queries executed, %d expected" % (
                executed, self.num
            )
        )


class FlaskTest(TestCase):
    """ Base flask test class.

        Initialize database.
        Create objects generator.
    """

    def create_app(self):
        return current_app

    def setUp(self):
        db.create_all()
        self.mixer = Mixer(self.app, session_commit=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assertNumQueries(self, num, func=None):
        " Check number of queries by flask_sqlalchemy. "

        context = QueriesContext(num, self)
        if func is None:
            return context

        with context:
            func()


class CoreTest(FlaskTest):

    def test_home(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_admin(self):
        with self.assertNumQueries(0):
            response = self.client.get('/admin/')
        self.assert404(response)

    def test_cache(self):
        from ..ext import cache

        cache.set('key', 'value')
        testkey = cache.get('key')
        self.assertEqual(testkey, 'value')

    def test_after_change(self):
        from .models import Alembic
        from mock import Mock
        Alembic.before_new = Mock()
        a = Alembic()
        a.version_num = '345'
        db.session.add(a)
        db.session.commit()
        self.assertEqual(Alembic.before_new.call_count, 1)

    def test_mail_handler(self):
        """ Handle errors by mail.
        """
        from . import FlaskMailHandler
        from ..ext import mail

        mail.username = 'test@test.com'
        mail.password = 'test'
        self.app.config['ADMINS'] = ['test@test.com']
        self.app.config['DEFAULT_MAIL_SENDER'] = 'test@test.com'
        self.app.logger.addHandler(FlaskMailHandler(40))
        propagate_exceptions = self.app.config.get('PROPAGATE_EXCEPTIONS')
        self.app.config['PROPAGATE_EXCEPTIONS'] = False

        @self.app.route('/error')
        def error():
            raise Exception('Error content')
        assert error

        with mail.record_messages() as outbox:
            self.app.logger.error('Attention!')
            self.assertTrue(outbox)
            msg = outbox.pop()
            self.assertEqual(msg.subject, 'APP ERROR: http://localhost/')

            self.client.get('/error')
            msg = outbox.pop()
            self.assertTrue('Error content', )

        self.app.config['PROPAGATE_EXCEPTIONS'] = propagate_exceptions
