" Settings for running tests. "

from .production import *


# TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_ECHO = True
CSRF_ENABLED = False
CACHE_TYPE = 'simple'

# pymode:lint_ignore=W0614,W404
