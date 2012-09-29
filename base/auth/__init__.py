" base.auth "


def loader_meta(app):
    " Configure application. "

    from .views import auth
    app.register_blueprint(auth)

    from .oauth import PROVIDERS
    map(lambda p: p.setup(app), PROVIDERS)

loader_meta.priority = 1.0
