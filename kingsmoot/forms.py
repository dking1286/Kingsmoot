from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email address already exists')


class RegisterForm(Form):
    first_name = StringField(
        'First name',
        validators=[
            DataRequired()
        ]
    )
    last_name = StringField(
        'Last name',
        validators=[
            DataRequired()
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message="Passwords must match")
        ]
    )
    password2 = PasswordField(
        'Confirm password',
        validators=[
            DataRequired()
        ]
    )


class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )


class NewQuestionForm(Form):
    text = TextAreaField(
        'Ask anything...',
        validators=[
            DataRequired()
        ]
    )


class NewAnswerForm(Form):
    text = TextAreaField(
        'Answer this question...',
        validators=[
            DataRequired()
        ]
    )
