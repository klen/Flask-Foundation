from flask import request
from flask_collect import Collect
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_script import Manager
from flask_squll import Squll
from flaskext.babel import Babel
from flask_cache import Cache
from dealer.contrib.flask import Dealer

from .app import create_app


babel = Babel()
cache = Cache()
db = Squll()
dealer = Dealer()
mail = Mail()

manager = Manager(create_app)
manager.add_option("-c", "--config", dest="config", required=False)

collect = Collect()
collect.init_script(manager)


def config_extensions(app):
    " Init application with extensions. "

    cache.init_app(app)
    collect.init_app(app)
    db.init_app(app)
    dealer.init_app(app)
    mail.init_app(app)

    DebugToolbarExtension(app)

    config_babel(app)


def config_babel(app):
    " Init application with babel. "

    babel.init_app(app)

    def get_locale():
        return request.accept_languages.best_match(
            app.config['BABEL_LANGUAGES'])
    babel.localeselector(get_locale)


# pymode:lint_ignore=F0401
