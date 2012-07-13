from os import path as op


__basedir__ = op.abspath(op.dirname(op.dirname(__file__)))


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + op.join(__basedir__, '.db')
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "somethingimpossibletoguess"


class Production(Config):
    ADMINS = frozenset(['youremail@yourdomain.com'])
    SECRET_KEY = 'SecretKeyForSessionSigning'
    DATABASE_CONNECT_OPTIONS = {}
    BABEL_DEFAULT_LOCALE = 'en'


class Testing(Production):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class Develop(Production):
    DEBUG = True
    SQLALCHEMY_ECHO = True
