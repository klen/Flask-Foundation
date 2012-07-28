#!/usr/bin/env python
# coding: utf-8
from flaskext.script import Manager

from base.app import create_app
from base.ext import db
from base.script import CreateDB, DropDB, ResetDB
from base.auth.script import CreateUserCommand, CreateRoleCommand, AddRoleCommand, RemoveRoleCommand


manager = Manager(create_app)
manager.add_option("-c", "--config", dest="config", required=False)
manager.add_command('create_user', CreateUserCommand())
manager.add_command('create_role', CreateRoleCommand())
manager.add_command('add_role', AddRoleCommand())
manager.add_command('remove_role', RemoveRoleCommand())
manager.add_command('create_db', CreateDB())
manager.add_command('drop_db', DropDB())
manager.add_command('reset_db', ResetDB())


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
