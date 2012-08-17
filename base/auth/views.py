from flask import request, render_template, flash, redirect, url_for
from flaskext.babel import lazy_gettext as _

from ..ext import db
from .forms import RegisterForm, LoginForm
from .manager import UserManager
from .models import User


users = UserManager(
    'users', __name__, url_prefix='/users', template_folder='templates')


@users.route('/profile/')
@users.login_required
def profile():
    return render_template("users/profile.html")


@users.route('/login/', methods=['POST'])
def login():
    " View function which handles an authentication request. "
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # we use werzeug to validate user's password
        if user and user.check_password(form.password.data):
            users.login(user)
            flash(_('Welcome %(user)s', user=user.username))
            return redirect(url_for('users.profile'))
        flash(_('Wrong email or password'), 'error-message')
    return redirect(request.referrer or url_for(users._login_manager.login_view))


@users.route('/logout/', methods=['GET'])
@users.login_required
def logout():
    " View function which handles a logout request. "
    users.logout()
    return redirect(request.referrer or url_for(users._login_manager.login_view))


@users.route('/register/', methods=['GET', 'POST'])
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

        users.login(user)

        # flash will display a message to the user
        flash(_('Thanks for registering'))
        # redirect user to the 'home' method of the user module.
        return redirect(url_for('users.profile'))
    return render_template("users/register.html", form=form)


# pymode:lint_ignore=F0401
