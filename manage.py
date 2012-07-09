#!/usr/bin/env python
# coding: utf-8
from flask.ext.script import Manager

from base.app import create_app, db
from base.script import CreateDB, DropDB, LoadFixtures
from base.users.script import CreateUserCommand, CreateRoleCommand, AddRoleCommand, RemoveRoleCommand


manager = Manager(create_app)
manager.add_option("-c", "--config", dest="config", required=False)
manager.add_command('create_user', CreateUserCommand())
manager.add_command('create_role', CreateRoleCommand())
manager.add_command('add_role', AddRoleCommand())
manager.add_command('remove_role', RemoveRoleCommand())
manager.add_command('create_db', CreateDB())
manager.add_command('drop_db', DropDB())
manager.add_command('load_dump', LoadFixtures())


@manager.shell
def make_shell_context():
    " Update shell. "
    from flask import current_app
    return dict(app=current_app, db=db)


if __name__ == '__main__':
    manager.run()
