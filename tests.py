from flask.ext.testing import TestCase

from base.app import create_app, db

from base.settings import Testing


class BaseTest(TestCase):

    def create_app(self):
        return create_app(Testing)

    def setUp(self):
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_users(self):
        from base.users.models import User

        response = self.client.post('/users/login/', data=dict())
        self.assertRedirects(response, '/')

        user = User(username='test', pw_hash='test', email='test@test.com')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/users/login/', data=dict(
            email='test@test.com',
            action_save=True,
            password='test'))
        self.assertRedirects(response, '/users/profile/')

        response = self.client.get('/users/logout/')
        self.assertRedirects(response, '/')

        response = self.client.post('/users/register/', data=dict(
            username='test2',
            email='test2@test.com',
            action_save=True,
            password='test',
            password_confirm='test',
            ))
        self.assertRedirects(response, '/users/profile/')

        user = User.query.filter(User.username == 'test2').first()
        self.assertEqual(user.email, 'test2@test.com')
