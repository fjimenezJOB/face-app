from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from models import User
from wtforms.validators import (DataRequired,ValidationError, Email, Regexp, Length, EqualTo)


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Ya existe un usuario con este nombre')

def email_exists(form, field):
        if User.select().where(User.email == field.data).exists():
            raise ValidationError('Este email ya está registrado')


class RefisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$'
            ),
            name_exists
        ])

    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ])
    
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=5),
            EqualTo('password2', message='La contraseña debe de coincidir')
        ])
    
    password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )