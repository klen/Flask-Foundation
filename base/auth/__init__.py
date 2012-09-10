" base.auth "


def register_app(app):
    " Configure application. "

    from .views import users
    app.register_blueprint(users)

    from .oauth import config_rauth
    config_rauth(app)

register_app.priority = 1.0
