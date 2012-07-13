from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.cache import Cache

import settings


db = SQLAlchemy()


def create_app(config=None, **skip):
    app = Flask(__name__)
    app.config.from_object(config or settings.Production)
    app.config.from_envvar("APP_SETTINGS", silent=True)

    # Init ORM
    db.init_app(app)

    # Main urlconfig
    from views import urls
    app.register_blueprint(urls)

    # Users support
    from users.views import bp
    app.register_blueprint(bp)

    # Admin
    from admin import admin
    if not admin.app:
        admin.init_app(app)

    # Bootstrap
    Bootstrap(app)

    # Cache
    app.cache = Cache(app)

    # Localization
    from flask.ext.babel import Babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'ru'
        return request.accept_languages.best_match(['en', 'ru'])

    app.errorhandler(404)(lambda e: (render_template('404.html'), 404))

    return app
