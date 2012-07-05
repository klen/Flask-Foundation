from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form, TextField, PasswordField, Required, Email, EqualTo


class LoginForm(Form):
    email = TextField(_('Email address'), [Required(), Email()])
    password = PasswordField(_('Password'), [Required()])


class RegisterForm(Form):
    username = TextField(_('NickName'), [Required()])
    email = TextField(_('Email address'), [Required(), Email()])
    password = PasswordField(_('Password'), [Required()])
    confirm = PasswordField(_('Repeat Password'), [
        Required(),
        EqualTo('password', message=_('Passwords must match'))
        ])
