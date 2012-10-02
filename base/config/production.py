" Production settings must be here. "

from .core import *
from os import path as op


MODE = 'production'
SECRET_KEY = 'SecretKeyForSessionSigning'
ADMINS = MAIL_USERNAME and [MAIL_USERNAME] or None

# flask.ext.collect
# -----------------
COLLECT_STATIC_ROOT = op.join(op.dirname(ROOTDIR), 'static')

# auth.oauth
# ----------
OAUTH_TWITTER = dict(
    consumer_key='750sRyKzvdGPJjPd96yfgw',
    consumer_secret='UGcyjDCUOb1q44w1nUk8FA7aXxvwwj1BCbiFvYYI',
)

OAUTH_FACEBOOK = dict(
    consumer_key='413457268707622',
    consumer_secret='48e9be9f4e8abccd3fb916a3f646dd3f',
)

OAUTH_GITHUB = dict(
    consumer_key='8bdb217c5df1c20fe632',
    consumer_secret='a3aa972b2e66e3fac488b4544d55eda2aa2768b6',
)

# dealer
DEALER_PARAMS = dict(
    backends=('git', 'mercurial', 'simple', 'null')
)

logging.info("Production settings loaded.")

# pymode:lint_ignore=W0614,W404
