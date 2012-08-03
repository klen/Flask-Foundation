def register_app(app):
    " Configure application. "

    from .views import urls
    app.register_blueprint(urls)

    from .admin import admin
    admin.init_app(app)

    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap()
    bootstrap.init_app(app)
