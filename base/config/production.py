" Production settings must be here. "

from .core import *


SECRET_KEY = 'SecretKeyForSessionSigning'

# Mail (gmail config)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = '*********'
DEFAULT_MAIL_SENDER = 'Admin < %s >' % MAIL_USERNAME

ADMINS = frozenset([MAIL_USERNAME])
