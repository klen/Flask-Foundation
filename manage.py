#!/usr/bin/env python
# coding: utf-8
import importlib

from base.config.production import APPS
from base.ext import db, manager


for app in APPS:
    try:
        script = importlib.import_module("%s.script" % app)
        for cmd in script.__all__:
            cls = getattr(script, cmd)
            manager.add_command(cls.__name__.lower(), cls())
    except ImportError:
        continue


@manager.shell
def make_shell_context():
    " Update shell. "
    from flask import current_app
    return dict(app=current_app, db=db)


@manager.command
def migrate(action):
    " Migration utils [create, run, undo, redo]. "
    from flaskext.evolution import Evolution
    from flask import current_app
    evolution = Evolution(current_app)
    evolution.manager(action)


if __name__ == '__main__':
    manager.run()

# pymode:lint_ignore=F0401
