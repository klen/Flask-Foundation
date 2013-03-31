from flask import url_for

from ..core.tests import FlaskTest
from ..ext import db


class AuthTest(FlaskTest):

    def test_model_mixin(self):
        from .models import User
        self.assertTrue(User.do_true())

    def test_users(self):
        from .models import User

        response = self.client.post('/auth/login/', data=dict())
        self.assertRedirects(response, '/')

        user = User(username='test', pw_hash='test', email='test@test.com')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.updated_at)

        response = self.client.post('/auth/login/', data=dict(
            email='test@test.com',
            action_save=True,
            password='test'))
        redirect_url = url_for(self.app.config.get('AUTH_PROFILE_VIEW', 'auth.profile'))
        self.assertRedirects(response, redirect_url)

        response = self.client.get('/auth/logout/')
        self.assertRedirects(response, '/')

        response = self.client.post('/auth/register/', data=dict(
            username='test2',
            email='test2@test.com',
            action_save=True,
            password='test',
            password_confirm='test',
        ))
        redirect_url = url_for(self.app.config.get('AUTH_PROFILE_VIEW', 'auth.profile'))
        self.assertRedirects(response, redirect_url)

        user = User.query.filter(User.username == 'test2').first()
        self.assertEqual(user.email, 'test2@test.com')

    def test_manager(self):
        from .models import Role, User
        from .manage import create_role, create_user, add_role

        create_role('test')
        role = Role.query.filter(Role.name == 'test').first()
        self.assertEqual(role.name, 'test')

        create_user('test', 'test@test.com', active=True, password='12345')
        user = User.query.filter(User.username == 'test').first()

        add_role('test', 'test')
        self.assertTrue(role in user.roles)

    def test_oauth(self):
        from flask import url_for

        if self.app.config.get('OAUTH_TWITTER'):
            self.assertTrue(url_for('oauth_twitter_login'))

        if self.app.config.get('OAUTH_GITHUB'):
            self.assertTrue(url_for('oauth_github_login'))

        if self.app.config.get('OAUTH_FACEBOOK'):
            self.assertTrue(url_for('oauth_facebook_login'))


class TestUserMixin(object):

    @staticmethod
    def do_true():
        return True
