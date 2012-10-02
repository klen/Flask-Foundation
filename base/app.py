from flask import Flask
from os import environ, path as op

from .config import production


def create_app(config=None, **settings):
    app = Flask(__name__)
    app.config.from_envvar("APP_SETTINGS", silent=True)
    app.config.from_object(config or production)

    # Settings from mode
    mode = environ.get('MODE')
    if mode:
        app.config.from_object('base.config.%s' % mode)

    # Local settings
    app.config.from_pyfile(op.join(op.dirname(production.__file__), 'local.py'), silent=True)

    # Overide settings
    app.config.update(settings)

    with app.test_request_context():

        from .ext import config_extensions
        config_extensions(app)

        from .loader import loader
        loader.register(app)

    return app
