from flaskext.script import prompt_bool

from .ext import manager
from .utils import load_modules


load_modules('script')


@manager.command
def create_db():
    from base.ext import db
    db.create_all()

    # Evolution support
    from flask import current_app
    from flaskext.evolution import db as evolution_db
    evolution_db.init_app(current_app)
    evolution_db.create_all()

    print "Database created successfuly"


@manager.command
def drop_db():
    from base.ext import db

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
    drop_db()
    create_db()


# pymode:lint_ignore=F0401
