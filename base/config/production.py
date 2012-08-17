" Production settings must be here. "

from .core import *
from os import path as op


SECRET_KEY = 'SecretKeyForSessionSigning'

# Mail (gmail config)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = '*********'
DEFAULT_MAIL_SENDER = 'Admin < %s >' % MAIL_USERNAME

ADMINS = frozenset([MAIL_USERNAME])
COLLECT_STATIC_ROOT = op.join(op.dirname(ROOTDIR), 'static')

OAUTH_TWITTER = dict(
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authorize',

    # flask-base-template app
    consumer_key='ydcXz2pWyePfc3MX3nxJw',
    consumer_secret='Pt1t2PjzKu8vsX5ixbFKu5gNEAekYrbpJrlsQMIwquc'
)

# pymode:lint_ignore=W0614,W404
# flake8: noqa
