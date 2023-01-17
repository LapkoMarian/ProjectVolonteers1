from .. import db
from datetime import datetime
import locale

set_locale = locale.setlocale(locale.LC_ALL, '')
time_now = datetime.today()
time_post = time_now.strftime("%d.%b.%Y | %H:%M")

class Statuspost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), nullable=False)
    post = db.relationship('Posts', backref='status', lazy=True)


class Categorypost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60), nullable=False)
    post = db.relationship('Posts', backref='category', lazy=True)


class Citypost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)
    post = db.relationship('Posts', backref='city', lazy=True)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(60), nullable=False, default='postdefault.jpg')
    created = db.Column(db.String(30), default=time_post, nullable=False)
    category_post = db.Column(db.Integer, db.ForeignKey('categorypost.id'), nullable=True)
    status_post = db.Column(db.Integer, db.ForeignKey('statuspost.id'), nullable=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city_post = db.Column(db.Integer, db.ForeignKey('citypost.id'), nullable=True)


    def __repr__(self):
        return f"Post('{self.id}', '{self.title}')"