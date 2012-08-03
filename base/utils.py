import importlib

from base.config.production import APPS


def load_modules(name, app=None):
    " Load modules by apps. "

    apps = app and app.config.get('APPS') or APPS
    mods = []
    for app in apps:
        try:
            mods.append(importlib.import_module('base.%s.%s' % (app, name)))
        except ImportError:
            continue
    return mods
