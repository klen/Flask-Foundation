from .ext import admin, ModelView
from .models import Alembic


class AlembicView(ModelView):
    column_filters = 'version_num',
    column_list = 'version_num',
    form_columns = 'version_num',

admin.add_model(Alembic, AlembicView)
