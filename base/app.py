from flask import Flask, render_template

import settings
from .ext import config_extensions


def create_app(config=None, **skip):
    app = Flask(__name__)
    app.config.from_object(config or settings.Production)
    app.config.from_envvar("APP_SETTINGS", silent=True)

    # Main urlconfig
    from views import urls
    app.register_blueprint(urls)

    # Users support
    from users.views import bp
    app.register_blueprint(bp)

    app.errorhandler(404)(lambda e: (render_template('404.html'), 404))

    config_extensions(app)

    return app
