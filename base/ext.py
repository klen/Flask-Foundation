from flask import request
from flask_sqlalchemy import SQLAlchemy
from flaskext.babel import Babel
from flaskext.cache import Cache
from flaskext.mail import Mail
from flaskext.script import Manager
from flask_collect import Collect

from .app import create_app


babel = Babel()
cache = Cache()
db = SQLAlchemy()
main = Mail()

manager = Manager(create_app)
manager.add_option("-c", "--config", dest="config", required=False)

collect = Collect()
collect.init_script(manager)


def config_extensions(app):
    " Init application with extensions. "

    cache.init_app(app)
    db.init_app(app)
    main.init_app(app)
    collect.init_app(app)

    config_babel(app)


def config_babel(app):
    " Init application with babel. "

    babel.init_app(app)

    def get_locale():
        return request.accept_languages.best_match(app.config['BABEL_LANGUAGES'])
    babel.localeselector(get_locale)


# pymode:lint_ignore=F0401
