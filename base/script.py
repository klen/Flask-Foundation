from flask.ext.script import Command, prompt_bool


class CreateDB(Command):
    " Create DB structure. "

    def run(self):
        from base.ext import db
        db.create_all()

        # Evolution support
        from flask import current_app
        from flask.ext.evolution import db as evolution_db
        evolution_db.init_app(current_app)
        evolution_db.create_all()

        print "Database created successfuly"


class DropDB(Command):
    " Drops all database tables. "
    def run(self):
        from base.ext import db

        if prompt_bool("Are you sure? You will lose all your data!"):
            db.drop_all()

            # Evolution support
            from flask import current_app
            from flask.ext.evolution import db as evolution_db
            evolution_db.init_app(current_app)
            evolution_db.drop_all()

            print "Database clearing"


class ResetDB(Command):
    " Reset DB. "
    def run(self):
        DropDB().run()
        CreateDB().run()
