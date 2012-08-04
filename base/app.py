from flask import Flask

from .config import production


def create_app(config=None, **skip):
    app = Flask(__name__)
    app.config.from_object(config or production)
    app.config.from_envvar("APP_SETTINGS", silent=True)

    from .ext import config_extensions
    config_extensions(app)

    from .loader import loader
    loader.register(app)

    return app
