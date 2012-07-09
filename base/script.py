from flask.ext.script import Command, Option, prompt_bool


class CreateDB(Command):
    " Create DB structure. "

    def run():
        from base.app import db
        db.create_all()
        print "Database created successfuly"


class DropDB(Command):
    " Drops all database tables. "
    def run():
        from base.app import db
        if prompt_bool("Are you sure ? You will lose all your data !"):
            db.drop_all()
            print "Database clearing"


class LoadFixtures(Command):
    " Load SQL dump. "
    option_list = (
        Option('-d', '--dump', dest='dump', default='fixture.sql')
    )

    def run(dump=None):
        from base.app import db
        with open(dump) as f:
            for line in f.readlines():
                db.session.execute(line)
                db.session.commit()
