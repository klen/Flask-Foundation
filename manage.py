#!/usr/bin/env python
# coding: utf-8
from base.ext import db, manager
from base.loader import loader
import sys


# Load app scripts
loader.load_submod('script')


@manager.shell
def make_shell_context():
    " Update shell. "
    from flask import current_app
    return dict(app=current_app, db=db)


@manager.command
def migrate():
    " Migration utils. "
    from alembic.config import main
    main(ARGV)


@manager.command
def test():
    " Run tests. "
    from unittest.loader import defaultTestLoader
    from unittest.runner import TextTestRunner

    suites = [defaultTestLoader.loadTestsFromModule(mod) for mod in loader.load_submod('tests')]
    suite = defaultTestLoader.suiteClass(suites)
    TextTestRunner().run(suite)


ARGV = []

if __name__ == '__main__':
    argv = sys.argv[1:]
    if argv and argv[0] == 'migrate':
        ARGV = list(argv[1:])
        sys.argv[0] += ' migrate'
        sys.argv = sys.argv[:2]

    manager.run()

# pymode:lint_ignore=F0401
