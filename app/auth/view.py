from flask import url_for, render_template, flash, redirect, abort, current_app, request, session
from .. import db, bcrypt, GOOGLE_CLIENT_ID, flow1
from .forms import SignUpForm, LoginForm, UpdateAccountForm, ResetPasswordForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import auth_blueprint
import os
import secrets
from PIL import Image
import locale
import requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests


@auth_blueprint.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember.data)
        return redirect(url_for('auth.account'))
    return render_template('auth/signup.html', form_reg=form, title='Register')


@auth_blueprint.route("/signup_google")
def signup_google():
    authorization_url, state = flow1.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth_blueprint.route("/callback", methods=['GET', 'POST'])
def callback():
    flow1.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow1.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    user = User.query.filter_by(email=id_info.get("email")).first()
    if user:
        login_user(user)
        return redirect(url_for('auth.account'))
    else:
        user = User(username=id_info.get("name"), email=id_info.get("email"), password=id_info.get("at_hash"))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('auth.account'))


@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form_log = LoginForm()
    if form_log.validate_on_submit():
        user = User.query.filter_by(email=form_log.email.data).first()
        if User.query.filter_by(email=form_log.email.data).first():
            if user and user.verify_password(form_log.password.data):
                login_user(user, remember=form_log.remember.data)
                return redirect(url_for('auth.account'))
            else:
                flash('Неправильна ел.пошта або пароль!', category='warning')
        else:
            flash(f'Електронна пошта {form_log.email.data} ще не зареєстрована!', category='warning')
            return redirect(url_for('auth.signup'))
    return render_template('auth/login.html', form_log=form_log, title='Login')


#
# @auth_blueprint.route("/users", methods=['GET', 'POST'])
# @login_required
# def users():
#     all_users = User.query.all()
#     count = User.query.count()
#     if count == 0:
#         return render_template(url_for('templates/404.html'))
#     return render_template('auth/user_list.html', all_users=all_users, count=count)
#
#
@auth_blueprint.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_blueprint.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form_acc = UpdateAccountForm()
    if form_acc.validate_on_submit():
        if form_acc.picture.data:
            picture_file = save_picture(form_acc.picture.data)
            current_user.image_file = picture_file
        current_user.username = form_acc.username.data
        current_user.email = form_acc.email.data
        current_user.about_me = form_acc.about_me.data
        db.session.commit()
        return redirect(url_for('auth.account'))

    form_acc.about_me.data = current_user.about_me
    form_acc.username.data = current_user.username
    form_acc.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('auth/account.html', image_file=image_file, form_acc=form_acc, title='Account')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (400, 400)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@auth_blueprint.route("/reset-password", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.new_password1.data).decode('utf-8')
        db.session.commit()
        flash('Password changed', category='success')
        return redirect(url_for('auth.account'))
    return render_template('auth/reset_password.html', form=form)

#
# @auth_blueprint.before_request
# def before_request():
#     if current_user.is_authenticated:
#         set_locale = locale.setlocale(locale.LC_ALL, '')
#         current_user.last_date = datetime.now()
#         db.session.commit()
