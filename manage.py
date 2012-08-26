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
    " Alembic migration utils. "

    from flask import current_app
    from alembic.config import main
    from os import path as op

    global ARGV

    config = op.join(op.dirname(__file__), 'migrate', 'develop.ini' if current_app.debug else 'production.ini')

    ARGV = ['-c', config] + ARGV

    main(ARGV)


@manager.command
def test():
    " Run tests. "
    try:
        from unittest2.loader import defaultTestLoader
        from unittest2.runner import TextTestRunner
    except ImportError:
        from unittest.loader import defaultTestLoader
        from unittest.runner import TextTestRunner

    suites = [defaultTestLoader.loadTestsFromModule(mod) for mod in loader.load_submod('tests')]
    suite = defaultTestLoader.suiteClass(suites)
    TextTestRunner().run(suite)


ARGV = []

if __name__ == '__main__':
    argv = sys.argv[1:]
    if argv and argv[0] == 'migrate':
        ARGV = filter(lambda a: not a in ('-c', 'migrate') and not a.startswith('base.config.'), argv)
        argv = filter(lambda a: not a in ARGV, argv)
        sys.argv = [sys.argv[0]] + argv

    manager.run()


# pymode:lint_ignore=F0401,W801,W0603
