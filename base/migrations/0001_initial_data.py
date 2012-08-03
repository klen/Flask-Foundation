from flaskext.evolution import BaseMigration


class Migration(BaseMigration):

    def up(self):
        from base.ext import db
        from base.auth.models import Role, User

        admin = Role(name='admin')
        staff = Role(name='staff')

        user = User(username='admin',
                email='admin@admin.com',
                pw_hash='admin')

        user.roles.append(admin)
        user.roles.append(staff)
        db.session.add(user)
        db.session.commit()

    def down(self):
        raise TypeError("down is not defined")
