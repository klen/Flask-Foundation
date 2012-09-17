" Production settings must be here. "

from .core import *
from os import path as op


SECRET_KEY = 'SecretKeyForSessionSigning'
ADMINS = frozenset([MAIL_USERNAME])

# flask.ext.collect
# -----------------
COLLECT_STATIC_ROOT = op.join(op.dirname(ROOTDIR), 'static')

# auth.oauth
# ----------
OAUTH_TWITTER = dict(
    # flask-base-template app
    consumer_key='ydcXz2pWyePfc3MX3nxJw',
    consumer_secret='Pt1t2PjzKu8vsX5ixbFKu5gNEAekYrbpJrlsQMIwquc'
)

# dealer
DEALER_PARAMS = dict(
    backends=('git', 'mercurial', 'simple', 'null')
)


# pymode:lint_ignore=W0614,W404
