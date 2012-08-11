from flask import render_template, Blueprint, current_app

from ..auth.forms import LoginForm


urls = Blueprint('urls', __name__, template_folder='templates')


if current_app and current_app.config.get('CORE_URLS'):

    @urls.route('/')
    def index():
        " Main page. "
        return render_template('core/index.html', loginform=LoginForm())
