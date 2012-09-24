from ..core.tests import FlaskTest
from ..ext import db


class AuthTest(FlaskTest):

    def test_model_mixin(self):
        from base.auth.models import User
        self.assertTrue(User.do_true())

    def test_users(self):
        from base.auth.models import User

        response = self.client.post('/users/login/', data=dict())
        self.assertRedirects(response, '/')

        user = User(username='test', pw_hash='test', email='test@test.com')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.updated_at)

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
        from base.auth.script import create_role, create_user, add_role

        create_role('test')
        role = Role.query.filter(Role.name == 'test').first()
        self.assertEqual(role.name, 'test')

        create_user('test', 'test@test.com', active=True, password='12345')
        user = User.query.filter(User.username == 'test').first()

        add_role('test', 'test')
        self.assertTrue(role in user.roles)

    def test_oauth(self):
        from flask import url_for

        self.assertTrue(url_for('login_twitter'))


class TestUserMixin(object):

    @staticmethod
    def do_true():
        return True
