from flask import request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flaskext.babel import Babel
from flaskext.cache import Cache
from flaskext.mail import Mail
from flaskext.oauth import OAuth

from .admin import FlaskAdmin
from .oauth import config_oauth


admin = FlaskAdmin()
babel = Babel()
bootstrap = Bootstrap()
cache = Cache()
db = SQLAlchemy()
oauth = OAuth()
main = Mail()


def config_extensions(app):
    " Init application with extensions. "

    admin.init_app(app)
    bootstrap.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    main.init_app(app)

    config_babel(app)
    config_oauth(oauth, app)


def config_babel(app):
    " Init application with babel. "

    babel.init_app(app)

    def get_locale():
        return request.accept_languages.best_match(app.config['BABEL_LANGUAGES'])
    babel.localeselector(get_locale)


# pymode:lint_ignore=F0401
