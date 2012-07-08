#!/usr/bin/env python
# coding: utf-8
from flaskext.script import Manager, prompt_bool

from base.app import create_app, db
from base.settings import Develop


app = create_app(Develop)
manager = Manager(app)


@manager.command
def createall():
    " Creates all database tables. "
    db.create_all()


@manager.command
def dropall():
    " Drops all database tables. "
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


@manager.command
def fixture():
    with open('fixture.sql') as f:
        db.session.execute(f.read())
        db.session.commit()


@manager.shell
def make_shell_context():
    " Update shell. "
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
