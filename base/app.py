from flask import Flask, render_template

from base.config import production


def create_app(config=None, **skip):
    app = Flask(__name__)
    app.config.from_object(config or production)
    app.config.from_envvar("APP_SETTINGS", silent=True)

    app.errorhandler(404)(lambda e: (render_template('404.html'), 404))

    from .ext import config_extensions
    config_extensions(app)
    config_blueprints(app)

    return app


def config_blueprints(app):

    # Main urlconfig
    from .views import urls
    app.register_blueprint(urls)

    # Users support
    from .auth.views import users
    app.register_blueprint(users)
