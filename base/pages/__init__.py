" base.pages "


def loader_meta(app):
    " Configure application. "

    from .views import pages
    app.register_blueprint(pages)
