from unittest import TestCase

from base.app import create_app
from base.settings import Testing


app = create_app(Testing)
app.config['TESTING'] = True
app.config['DATABASE'] = 'memory:///'


class FlaskTest(TestCase):

    def setUp(self):

        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        response = self.app.get('/users/login/')
        self.assertEqual(response.status_code, 200)
