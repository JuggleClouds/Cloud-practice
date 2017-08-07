from flask_wtf import Form
from flask_babel import gettext
from wtforms import StringField, BooleanField, TextAreaField,  PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from .models import User


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class loginpassForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired()])
    about_me = TextAreaField('About_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(gettext(
                'This nickname has invalid characters. '
                'Please use letters, numbers, dots and underscores only.'))
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append(gettext(
                'This nickname is already in use. '
                'Please choose another one.'))
            return False
        return True


class PostForm(Form):
    post = StringField('Post', validators=[DataRequired()])


class SearchForm(Form):
    search = StringField('Search', validators=[DataRequired()])

class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    nickname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(),Length(min=6, max=25),EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
