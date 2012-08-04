from flask_testing import TestCase

from ..app import create_app
from ..config import test
from ..ext import db


class BaseCoreTest(TestCase):

    def create_app(self):
        return create_app(test)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users(self):
        from base.auth.models import User

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

    def test_manager(self):
        from base.auth.models import Role, User
        from manage import manager
        manager.app = self.app

        manager.handle('manage', 'create_role', ['test'])
        role = Role.query.filter(Role.name == 'test').first()
        self.assertEqual(role.name, 'test')

        manager.handle('manage', 'create_user', 'test test@test.com -p 12345'.split())
        user = User.query.filter(User.username == 'test').first()
        manager.handle('manage', 'add_role', 'test test'.split())
        self.assertTrue(role in user.roles)

    def test_oauth(self):
        from flask import url_for

        self.assertTrue(url_for('login_twitter'))
