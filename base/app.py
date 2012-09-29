from flask import Flask
from os import environ

from .config import production


def create_app(config=None, **settings):
    app = Flask(__name__)

    app.config.from_object(config or production)
    app.config.from_envvar("APP_SETTINGS", silent=True)
    mode = environ.get('MODE')
    if mode:
        app.config.from_object('base.config.%s' % mode)
    app.config.update(settings)

    with app.test_request_context():

        from .ext import config_extensions
        config_extensions(app)

        from .loader import loader
        loader.register(app)

    return app
