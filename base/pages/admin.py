from wtforms.fields import TextAreaField
from wtforms.widgets import TextArea

from ..core.ext import admin, AuthModelView
from .models import Page


class WysiwygWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs['class'] = 'span8 textarea'
        return super(WysiwygWidget, self).__call__(field, **kwargs)


class WysiwygTextAreaField(TextAreaField):
    widget = WysiwygWidget()


class PageView(AuthModelView):
    create_template = 'pages/admin/create.html'
    edit_template = 'pages/admin/edit.html'
    form_overrides = dict(content=WysiwygTextAreaField)
    column_list = 'slug', 'active', 'created_at', 'updated_at'


admin.add_model(Page, PageView)
