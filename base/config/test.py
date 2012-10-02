" Settings for running tests. "

from .production import *


MODE = 'test'
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
CSRF_ENABLED = False
CACHE_TYPE = 'simple'

AUTH_USER_MIXINS += ['base.auth.tests.TestUserMixin']

logging.info("Test settings loaded.")

# pymode:lint_ignore=W0614,W404
