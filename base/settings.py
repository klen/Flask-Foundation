from os import path as op


__basedir__ = op.abspath(op.dirname(op.dirname(__file__)))


class Config(object):
    " Core settings. "

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + op.join(__basedir__, '.db')

    # WTForms
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "somethingimpossibletoguess"

    # Babel
    BABEL_LANGUAGES = ['en', 'ru']
    BABEL_DEFAULT_LOCALE = 'en'

    # Mail (gmail config)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'username@gmail.com'
    MAIL_PASSWORD = '*********'
    DEFAULT_MAIL_SENDER = 'Admin < %s >' % MAIL_USERNAME


class Production(Config):
    " Production settings must be here. "

    ADMINS = frozenset(['youremail@yourdomain.com'])
    SECRET_KEY = 'SecretKeyForSessionSigning'


class Testing(Production):
    " Settings for running tests. "

    # TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CSRF_ENABLED = False
    CACHE_TYPE = 'simple'


class Develop(Production):
    " Settings for develop process. "

    DEBUG = True
    SQLALCHEMY_ECHO = True
