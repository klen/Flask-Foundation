from flask import request
from flaskext.babel import lazy_gettext as _
from flask_wtf import Form, TextField, PasswordField, Required, Email, EqualTo, BooleanField, HiddenField, SubmitField


class EmailFormMixin():
    email = TextField(_('Email address'),
                      validators=[Required(message=_("Email not provided")),
                                  Email(message=_("Invalid email address"))])


class PasswordFormMixin():
    password = PasswordField(_("Password"),
                             validators=[Required(message=_("Password not provided"))])


class PasswordConfirmFormMixin():
    password_confirm = PasswordField(_("Retype Password"),
                                     validators=[EqualTo('password', message=_("Passwords do not match"))])


class LoginForm(Form, EmailFormMixin, PasswordFormMixin):
    " The default login form. "

    remember = BooleanField(_("Remember Me"), default=True)
    next = HiddenField()
    submit = SubmitField(_("Login"))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        if request.method == 'GET':
            self.next.data = request.args.get('next', None)


class ForgotPasswordForm(Form, EmailFormMixin):
    "  The default forgot password form. "

    submit = SubmitField(_("Recover Password"))

    def to_dict(self):
        return dict(email=self.email.data)


class RegisterForm(Form, EmailFormMixin, PasswordFormMixin, PasswordConfirmFormMixin):
    "  The default register form. "

    username = TextField(_('UserName'), [Required(message=_('Required'))])
    # submit = SubmitField(_("Register"))

    def to_dict(self):
        return dict(email=self.email.data, password=self.password.data)


class ResetPasswordForm(Form,
                        EmailFormMixin,
                        PasswordFormMixin,
                        PasswordConfirmFormMixin):
    "  The default reset password form. "

    token = HiddenField(validators=[Required()])

    submit = SubmitField(_("Reset Password"))

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

        if request.method == 'GET':
            self.token.data = request.args.get('token', None)
            self.email.data = request.args.get('email', None)

    def to_dict(self):
        return dict(token=self.token.data,
                    email=self.email.data,
                    password=self.password.data)


# pymode:lint_ignore=F0401
