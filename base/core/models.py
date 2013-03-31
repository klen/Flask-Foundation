from datetime import datetime

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.session import object_session

from ..ext import db


class UpdateMixin(object):
    """Provides the 'update' convenience function to allow class
    properties to be written via keyword arguments when the object is
    already initialised.

    .. code-block: python

        class Person(Base, UpdateMixin):
            name = db.Column(String(19))

        >>> person = Person(name='foo')
        >>> person.update(**{'name': 'bar'})
        >>> person.update(login='foo')

    """

    def update(self, **kw):
        for k, v in kw.items():
            if hasattr(self, k):
                setattr(self, k, v)


class TimestampMixin(object):
    """Adds automatically updated created_at and updated_at timestamp
    columns to a table, that unsurprisingly are updated on record INSERT and
    UPDATE. UTC time is used in both cases.
    """

    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)


class BaseMixin(UpdateMixin, TimestampMixin):
    """ Defines an id column to save on boring boilerplate.
    """

    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        """ Set default tablename.
        """
        return self.__name__.lower()

    @property
    def __session__(self):
        return object_session(self)


class Alembic(db.Model):
    __tablename__ = 'alembic_version'
    version_num = db.Column(db.String(32), nullable=False, primary_key=True)


def before_signal(session, *args):
    map(lambda o: hasattr(o, 'before_new') and o.before_new(), session.new)
    map(lambda o: hasattr(o, 'before_delete') and o.before_delete(), session.deleted)

event.listen(db.session.__class__, 'before_flush', before_signal)
