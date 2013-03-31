from flask import render_template, Blueprint, current_app

from ..auth.forms import LoginForm


core = Blueprint('core', __name__,
                 template_folder='templates',
                 static_url_path='/static/core',
                 static_folder='static')


if current_app and current_app.config.get('AUTH_LOGIN_VIEW') == 'core.index':

    @core.route('/')
    def index():
        """
            Main page.

            Redifine `AUTH_LOGIN_VIEW` for customize index page.
        """

        return render_template('core/index.html', loginform=LoginForm())
