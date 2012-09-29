"""Flask-Script support.
"""
from flask_script import prompt_pass, Manager


auth_manager = Manager(usage='Authentication operations.')


def loader_meta(manager):
    " Register submanager with loader as manager init. "

    manager.add_command('auth', auth_manager)


@auth_manager.option('username')
@auth_manager.option('email')
@auth_manager.option('-a', '--active', dest='active', action='store_true')
@auth_manager.option('-p', '--password', dest='password', default='')
def create_user(username=None, email=None, active=False, password=''):
    " Create a user. "

    from .models import User
    from ..ext import db

    password = password or prompt_pass("Set password")
    user = User(username=username,
                email=email,
                pw_hash=password,
                active=active)

    db.session.add(user)
    db.session.commit()

    print 'User created successfully.'


@auth_manager.option('name')
def create_role(name):
    " Create a role. "

    from .models import Role
    from ..ext import db

    role = Role(name=name)

    db.session.add(role)
    db.session.commit()

    print 'Role "%s" created successfully.' % name


@auth_manager.option('username')
@auth_manager.option('role')
def add_role(username, role):
    " Add a role to a user. "

    from .models import User, Role
    from ..ext import db

    u = User.query.filter_by(username=username).first()
    r = Role.query.filter_by(name=role).first()
    if u and r:
        u.roles.append(r)
        db.session.add(u)
        db.session.commit()
        print "Role '%s' added to user '%s' successfully" % (
            role, username)


@auth_manager.option('username')
@auth_manager.option('role')
def remove_role(username, role):
    " Remove a role from user. "

    from .models import User, Role
    from ..ext import db

    u = User.query.filter_by(username=username).first()
    r = Role.query.filter_by(name=role).first()
    if r in u.roles:
        u.roles.remove(r)
        db.session.add(u)
        db.session.commit()
    print "Role '%s' removed from user '%s' successfully" % (
        role, username)

# pymode:lint_ignore=F0401
