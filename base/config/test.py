" Settings for running tests. "

from production import *


# TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
CSRF_ENABLED = False
CACHE_TYPE = 'simple'
