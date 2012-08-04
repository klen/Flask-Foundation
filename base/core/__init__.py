" base.core "


def register_app(app):
    " Configure application. "

    from .views import urls
    app.register_blueprint(urls)

    from .ext import admin
    admin.init_app(app)

    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    from flask import render_template
    app.errorhandler(404)(lambda e: (render_template('core/404.html'), 404))

register_app.priority = 100.0
