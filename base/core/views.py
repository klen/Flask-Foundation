from flask import render_template, Blueprint, current_app

from ..auth.forms import LoginForm


core = Blueprint('core', __name__, template_folder='templates')


if current_app and current_app.config.get('AUTH_LOGIN_VIEW') == 'core.index':

    @core.route('/')
    def index():
        " Main page. "
        return render_template('core/index.html', loginform=LoginForm())
