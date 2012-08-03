from flaskext.script import prompt_bool

from ..ext import manager


@manager.command
def create_db():
    " Create database. "

    from ..ext import db
    db.create_all()

    # Evolution support
    from flask import current_app
    from flaskext.evolution import db as evolution_db
    evolution_db.init_app(current_app)
    evolution_db.create_all()

    print "Database created successfuly"


@manager.command
def drop_db():
    " Drop all tables. "

    from ..ext import db

    if prompt_bool("Are you sure? You will lose all your data!"):
        db.drop_all()

        # Evolution support
        from flask import current_app
        from flaskext.evolution import db as evolution_db
        evolution_db.init_app(current_app)
        evolution_db.drop_all()

        print "Database clearing"


@manager.command
def reset_db():
    " Drop and create all tables. "

    drop_db()
    create_db()


# pymode:lint_ignore=F0401
