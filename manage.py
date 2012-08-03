#!/usr/bin/env python
# coding: utf-8
from base.app import load_modules
from base.ext import db, manager


load_modules('script')


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
