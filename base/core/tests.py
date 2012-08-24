from flask import current_app
from flask_testing import TestCase

from ..ext import db


class FlaskTest(TestCase):
    " Base flask test class. "

    def create_app(self):
        return current_app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class CoreTest(FlaskTest):

    def test_home(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_admin(self):
        response = self.client.get('/admin/')
        self.assert403(response)

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
        from ..ext import mail
        with mail.record_messages() as outbox:
            self.app.logger.error('Attention!')
            self.assertTrue(outbox)
            msg = outbox[0]
            self.assertEqual(msg.subject, 'APP ERROR: http://localhost/')
