" base.auth "


def loader_meta(app):
    " Configure application. "

    from .views import users
    app.register_blueprint(users)

    from .oauth import config_rauth
    config_rauth(app)

loader_meta.priority = 1.0
