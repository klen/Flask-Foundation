#!/usr/bin/env python
# coding: utf-8
from base.ext import db, manager
from base.loader import loader


# Load app scripts
loader.load_submod('script')


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

@manager.command
def test():
    " Run tests. "
    from unittest.loader import defaultTestLoader
    from unittest.runner import TextTestRunner

    suites = [defaultTestLoader.loadTestsFromModule(mod) for mod in loader.load_submod('tests')]
    suite = defaultTestLoader.suiteClass(suites)
    TextTestRunner().run(suite)

if __name__ == '__main__':
    manager.run()

# pymode:lint_ignore=F0401
