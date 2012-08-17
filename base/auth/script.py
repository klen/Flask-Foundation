from flaskext.script import Command, Option, prompt_pass

from ..ext import manager


class Create_user(Command):
    "  Create a user. "

    option_list = (
        Option('username'),
        Option('email'),
        Option('-a', '--active', dest='active', action='store_true'),
        Option('-p', '--password', dest='password', default=''),
    )

    @staticmethod
    def run(username=None, email=None, active=False, password=''):
        from .models import User
        from base.ext import db

        password = password or prompt_pass("Set password")
        user = User(username=username,
                    email=email,
                    pw_hash=password,
                    active=active)

        db.session.add(user)
        db.session.commit()

        print 'User created successfully.'
manager.add_command('create_user', Create_user())


class Create_role(Command):
    "  Create a role. "

    option_list = (
        Option('name'),
    )

    @staticmethod
    def run(name=None):
        from .models import Role
        from base.ext import db
        role = Role(name=name)

        db.session.add(role)
        db.session.commit()

        print 'Role "%s" created successfully.' % name

manager.add_command('create_role', Create_role())


class Add_role(Command):
    "  Add a role to a user. "

    option_list = (
        Option('username'),
        Option('role'),
    )

    @staticmethod
    def run(username=None, role=None):
        from .models import User, Role
        from base.ext import db
        u = User.query.filter_by(username=username).first()
        r = Role.query.filter_by(name=role).first()
        if u and r:
            u.roles.append(r)
            db.session.add(u)
            db.session.commit()
            print "Role '%s' added to user '%s' successfully" % (
                role, username)
manager.add_command('add_role', Add_role())


class Remove_role(Command):
    "  Remove a role from user. "

    option_list = (
        Option('username'),
        Option('role'),
    )

    @staticmethod
    def run(username=None, role=None):
        from .models import User, Role
        from base.ext import db
        u = User.query.filter_by(username=username).first()
        r = Role.query.filter_by(name=role).first()
        if r in u.roles:
            u.roles.remove(r)
            db.session.add(u)
            db.session.commit()
        print "Role '%s' removed from user '%s' successfully" % (
            role, username)

manager.add_command('remove_role', Add_role())

# pymode:lint_ignore=F0401
