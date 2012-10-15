""" Development settings.
"""

from .production import *


MODE = 'develop'
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_ECHO = True

logging.info("Develop settings loaded.")

# pymode:lint_ignore=W0614,W404
