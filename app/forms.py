from wtforms import PasswordField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextAreaField
from wtforms import StringField
from wtforms.validators import DataRequired, Email
from wtforms.validators import EqualTo, Length, ValidationError, Regexp

from app.models import User


# class LoginForm(FlaskForm):
#     username = StringField('Ім\'я користувача', validators=[DataRequired()])
#     password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=10)])
#     remember = BooleanField('Запам\'ятати мене')



class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Todo')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp('^[a-zA-Z0-9_]*$', message='Only letters, numbers, and underscores are allowed.')
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')