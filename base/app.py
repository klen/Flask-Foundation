from flask import Flask, render_template
import importlib

from .config import production


def create_app(config=None, **skip):
    app = Flask(__name__)
    app.config.from_object(config or production)
    app.config.from_envvar("APP_SETTINGS", silent=True)

    app.errorhandler(404)(lambda e: (render_template('404.html'), 404))

    from .ext import config_extensions
    config_extensions(app)

    for mod in load_modules('register', app):
        try:
            mod.register_app(app)
        except AttributeError:
            app.logger.error('Invalid mod: %s' % mod)

    return app


def load_modules(name, app=None):
    " Load modules by apps. "

    apps = app and app.config.get('APPS') or production.APPS
    mods = []
    for app in apps:
        try:
            mods.append(importlib.import_module('base.%s.%s' % (app, name)))
        except ImportError:
            continue
    return mods
