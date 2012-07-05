from sqlalchemy.ext.declarative import declared_attr

from .app import db


class AutoInitMixin(object):
    """
    Mixin for populating models columns automatically (no need
    to define an __init__ method) and set the default value if any.
    Also sets the model id and __tablename__ automatically.
    """
    id = db.Column(db.Integer, primary_key=True)

    # use the lowercased model class name as the __tablename__
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, *args, **kwargs):
        for attr in (a for a in dir(self) if not a.startswith('_')):
            attr_obj = getattr(self, attr)
            if isinstance(attr_obj, db.Column):
                if attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                else:
                    if hasattr(attr_obj, 'default'):
                        if callable(attr_obj.default):
                            setattr(self, attr, attr_obj.default())
                        else:
                            setattr(self, attr, attr_obj.default)
