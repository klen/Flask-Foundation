" Settings for running tests. "

from .production import *


# TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_ECHO = True
CSRF_ENABLED = False
CACHE_TYPE = 'simple'

AUTH_USER_MIXINS = 'base.auth.tests.TestUserMixin',

# pymode:lint_ignore=W0614,W404
