from flask import render_template, Blueprint

from .auth.forms import LoginForm


urls = Blueprint('urls', __name__)


@urls.route('/')
def index():
    " Main page. "
    return render_template('index.html', loginform=LoginForm())
