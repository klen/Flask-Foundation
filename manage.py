#!/usr/bin/env python
# coding: utf-8

from flaskext.script import Manager, prompt_bool
from src import create_app
from src.settings import Develop


app = create_app(Develop)
manager = Manager(app)


@manager.command
def createall():
    " Creates all database tables. "
    from src import db
    db.create_all()


@manager.command
def dropall():
    " Drops all database tables. "
    from src import db
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


@manager.shell
def make_shell_context():
    " Update shell. "
    from src import db
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
