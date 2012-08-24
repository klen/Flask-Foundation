" Core configuration settings. "

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
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = 'password_here'
DEFAULT_MAIL_SENDER = 'Admin <%s>' % MAIL_USERNAME
