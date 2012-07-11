from flask.ext.script import Command, prompt_bool


class CreateDB(Command):
    " Create DB structure. "

    def run(self):
        from base.app import db
        db.create_all()
        print "Database created successfuly"


class DropDB(Command):
    " Drops all database tables. "
    def run(self):
        from base.app import db
        if prompt_bool("Are you sure? You will lose all your data!"):
            db.drop_all()
            print "Database clearing"


class ResetDB(Command):
    " Reset DB. "
    def run(self):
        DropDB().run()
        CreateDB().run()
