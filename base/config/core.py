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
