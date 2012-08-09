from flask import current_app
from flask_testing import TestCase

from ..ext import db


class BaseCoreTest(TestCase):

    def create_app(self):
        return current_app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
