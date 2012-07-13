from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.cache import Cache
from flask.ext.babel import Babel
from flask import request
from admin import FlaskAdmin


db = SQLAlchemy()
bootstrap = Bootstrap()
cache = Cache()
babel = Babel()
admin = FlaskAdmin(db)


def config_extensions(app):

    db.init_app(app)
    bootstrap.init_app(app)
    cache.init_app(app)
    babel.init_app(app)
    not admin.app and admin.init_app(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['BABEL_LANGUAGES'])
