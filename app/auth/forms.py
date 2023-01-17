from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, DataRequired, ValidationError, email
import re
from .models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from .. import bcrypt


class SignUpForm(FlaskForm):
    username = StringField('', validators=[InputRequired("Потрібно вказати ім'я користувача!"),
                                           Length(min=4, max=14,
                                                  message="Ім'я користуача має містити більше 4 символів і максимум 14 символів!"),
                                           Regexp("^[A-Za-z][A-Za-z0-9_. ]*$",
                                                  message="Ім'я користувача може містити лише літери, цифри, крапки або нижнє підкреслення!")])
    email = StringField('', validators=[InputRequired('Потрібно вказати адресу електронної пошти!'),
                                        email(message='Неправильна електронна пошта!')])
    password1 = PasswordField('', validators=[InputRequired('Необхідно ввести пароль!'),
                                              Length(min=8, max=20),
                                              Regexp(
                                                  r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                                                  message='Пароль має містити великі та малі літери, цифри та спец.символи(@$!%*#?&)!')])
    password2 = PasswordField('', validators=[InputRequired('Необхідно ввести пароль!'),
                                              Length(min=8, max=20, message='Пароль має містити мінімум 8 симолів!'),
                                              EqualTo('password1', message='Паролі мають співпадати!')])
    remember = BooleanField('')
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Потрібно пройти рекапчу!")])
    submit = SubmitField(label=(''))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), email(message="Неправильна електронна пошта!")])
    password = PasswordField('', validators=[DataRequired()])
    remember = BooleanField('')
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Потрбно пройти рекапчу!")])
    submit = SubmitField(label=(''))


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired('Email is required'),
                                             Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                                    message='Invalid Email')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('About Me', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('')

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already registered')


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Старий пароль', validators=[DataRequired()])

    new_password1 = PasswordField('Новий пароль',
                                  validators=[InputRequired('Потрібно ввести пароль!'),
                                              Length(min=8, max=20),
                                              Regexp(
                                                  r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                                                  message='Пароль має містити великі та малі літери, цифри та спец.символи(@$!%*#?&)!')])

    new_password2 = PasswordField('Повторіть новий пароль',
                                  validators=[InputRequired('Потрібно ввести пароль!'),
                                              Length(min=8, max=20, message='Пароль має містити мінімум 8 симолів!'),
                                              EqualTo('password1', message='Паролі мають співпадати!')])

    def validate_old_password(self, field):
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Помилка')
