""" Immutable basic settings.
"""

import logging

from base.config import op, ROOTDIR


# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + op.join(ROOTDIR, '.db')

# WTForms
CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"

# Babel
BABEL_LANGUAGES = ['en', 'ru']
BABEL_DEFAULT_LOCALE = 'en'

# Auth
AUTH_USER_MIXINS = []
AUTH_LOGIN_VIEW = 'core.index'

# Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = None
MAIL_PASSWORD = None
DEFAULT_MAIL_SENDER = None

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d.%m %H:%M:%S')
logging.info("Core settings loaded.")
