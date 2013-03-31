from flask import render_template

from ..core.models import BaseMixin, db
from ..ext import cache
from .config import TEMPLATE, ROOT


class Page(db.Model, BaseMixin):
    """ Site pages.
    """

    __tablename__ = 'pages_page'

    active = db.Column(db.Boolean, default=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    link = db.Column(db.String(256))
    content = db.Column(db.Text)

    parent_id = db.Column(db.Integer, db.ForeignKey('pages_page.id'))
    children = db.relation(
        'Page',
        cascade='all',
        backref=db.backref('parent', remote_side='Page.id'))

    def __unicode__(self):
        return self.slug

    def render(self):
        return render_template(TEMPLATE, page=self)

    @property
    def uri(self):
        cache_key = 'pages.uri.{slug}'.format(slug=self.slug)
        uri = cache.get(cache_key)
        if not uri:
            parent = self.parent_id and self.parent.uri or ('/%s/' % ROOT)
            uri = "{parent}{slug}/".format(parent=parent, slug=self.slug)
            cache.set(cache_key, uri)
        return uri

    @classmethod
    def route(cls, slug):
        page = cls.query.filter_by(slug=slug).first()
        if page is None:
            return page

        return page.uri
