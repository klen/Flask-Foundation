" Settings for develop process. "

from .production import *


DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_ECHO = True


# pymode:lint_ignore=W0614,W404
