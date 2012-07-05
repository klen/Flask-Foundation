from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

import settings


db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or settings.Production)
    app.config.from_envvar("APP_SETTINGS", silent=True)
    db.init_app(app)

    # Main urlconfig
    from views import urls
    app.register_blueprint(urls)

    # Users support
    from users.views import users
    app.register_blueprint(users)

    # Admin
    from admin import admin
    admin.init_app(app)

    # Localization
    from flask.ext.babel import Babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'ru'
        return request.accept_languages.best_match(['en', 'ru'])

    app.errorhandler(404)(lambda e: (render_template('404.html'), 404))

    return app
