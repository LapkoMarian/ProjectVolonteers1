import os
import pathlib

import google_auth_oauthlib
from flask import Flask, session, abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from google_auth_oauthlib.flow import Flow

from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

bcrypt = Bcrypt()

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "627612776804-0468ba8rg3cilmgon20l5krpue6p3qcs.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "static/google_login/client_secret.json")

flow1 = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/auth/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    app.config['RECAPTCHA_PUBLIC_KEY'] = "6LfovwgjAAAAAGJCFxD0eMYEIfBLzBQloEx1IbND"
    app.config['RECAPTCHA_PRIVATE_KEY'] = "6LfovwgjAAAAADXSdGCpU3Lw_r2kOhy6MoNRRO5l"


    with app.app_context():
        from . import view

        from .auth import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .posts import post_blueprint
        app.register_blueprint(post_blueprint, url_prefix='/post')

        return app
