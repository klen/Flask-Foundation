from flask import render_template, Blueprint

from ..auth.forms import LoginForm


urls = Blueprint('urls', __name__, template_folder='templates')


@urls.route('/')
def index():
    " Main page. "
    return render_template('core/index.html', loginform=LoginForm())
