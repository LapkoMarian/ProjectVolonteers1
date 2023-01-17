import enum
from .. import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='../static/profile_pictures/default.jpg')
    about_me = db.Column(db.Text, nullable=True)
    last_date = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, username, email, password, about_me='', image_file='default.jpg'):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.about_me = about_me
        self.image_file = image_file

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

