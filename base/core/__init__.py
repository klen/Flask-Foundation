" base.core "
from flask import request
from flask_mail import Message
from logging import Handler, ERROR

from ..ext import mail


def loader_meta(app=None):
    " Configure application. "

    from .views import core
    app.register_blueprint(core)

    from .ext import admin
    admin.init_app(app)

    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    from flask import render_template
    app.errorhandler(404)(lambda e: (render_template('core/404.html'), 404))

    if not app.debug:
        mailhandler = FlaskMailHandler(ERROR)
        app.logger.addHandler(mailhandler)

loader_meta.priority = 100.0


class FlaskMailHandler(Handler):

    def emit(self, record):
        sbj = "APP ERROR: %s%s" % (request.host_url.rstrip('/'), request.path)
        msg = Message(sbj, body=self.format(record), recipients=mail.app.config.get('ADMINS', []))
        mail.send(msg)


# pymode:lint_ignore=F0401
