from flask import request, render_template, flash, redirect, url_for, current_app
from flaskext.babel import lazy_gettext as _

from ..ext import db
from .forms import RegisterForm, LoginForm
from .models import User
from .utils import UserManager


auth = UserManager(
    'auth', __name__, url_prefix='/auth', template_folder='templates')


if not current_app.config.get('AUTH_PROFILE_VIEW'):

    @auth.route('/profile/')
    @auth.login_required
    def profile():
        return render_template("auth/profile.html")


@auth.route('/login/', methods=['POST'])
def login():
    " View function which handles an authentication request. "
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # we use werzeug to validate user's password
        if user and user.check_password(form.password.data):
            auth.login(user)
            flash(_('Welcome %(user)s', user=user.username))
            redirect_name = current_app.config.get('AUTH_PROFILE_VIEW', 'auth.profile')
            return redirect(url_for(redirect_name))
        flash(_('Wrong email or password'), 'error-message')
    return redirect(request.referrer or url_for(auth._login_manager.login_view))


@auth.route('/logout/', methods=['GET'])
@auth.login_required
def logout():
    " View function which handles a logout request. "
    auth.logout()
    return redirect(request.referrer or url_for(auth._login_manager.login_view))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    " Registration Form. "
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # create an user instance not yet stored in the database
        user = User(
            username=form.username.data,
            email=form.email.data,
            pw_hash=form.password.data)

        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        auth.login(user)

        # flash will display a message to the user
        flash(_('Thanks for registering'))

        # redirect user to the 'home' method of the user module.
        redirect_name = current_app.config.get('AUTH_PROFILE_VIEW', 'auth.profile')
        return redirect(url_for(redirect_name))

    return render_template("auth/register.html", form=form)


# pymode:lint_ignore=F0401
