from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .forms import CreatePostForm, CategoryForm, CityForm, StatusForm
from .models import Categorypost, Posts, Citypost, Statuspost
from .. import db, bcrypt
from flask_login import current_user, login_required
from . import post_blueprint
from ..auth.models import User
from PIL import Image
import secrets
import os
from datetime import datetime


@post_blueprint.route('/', methods=['GET', 'POST'])
def view_post():
    post = Posts.query.order_by(Posts.title).all()
    return render_template('view_post.html', posts=post)


@post_blueprint.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()

    form.category.choices = [(category.id, category.category) for category in Categorypost.query.all()]
    form.city.choices = [(city.id, city.city) for city in Citypost.query.all()]
    form.status.choices = [(status.id, status.status) for status in Statuspost.query.all()]


    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = 'postdefault.jpg'


        post = Posts(title=form.title.data, text=form.text.data, image_file=image,
                    category_post=form.category.data, status_post=form.status.data,
                    username=current_user.username, phone=form.phone.data, city_post=form.city.data)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.view_post'))

    return render_template('post_create.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/posts_pics', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@post_blueprint.route('/<id>', methods=['GET', 'POST'])
def detail_post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post_detail.html', post=post)


@post_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if current_user.username == post.username:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.view_post'))

    return redirect(url_for('post.detail_post', pk=id))


@post_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)

    form = CreatePostForm()
    form.category.choices = [(category.id, category.category) for category in Categorypost.query.all()]
    form.city.choices = [(city.id, city.city) for city in Citypost.query.all()]
    form.status.choices = [(status.id, status.status) for status in Statuspost.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.category_post = form.category.data
        post.status_post = form.status.data
        post.city_post = form.city.data
        post.phone = form.phone.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('post.detail_post', id=id))

        form.title.data = post.title
        form.text.data = post.text
        form.category.data = post.category_post
        form.status.data = post.status_post
        form.city.data = post.city_post
        form.phone.data = post.phone

    return render_template('film_create.html', form=form)


@post_blueprint.route('/category_crud', methods=['GET', 'POST'])
def category_crud():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Categorypost(category=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('.category_crud'))

    categories = Categorypost.query.all()
    return render_template('category_crud.html', categories=categories, form=form)


@post_blueprint.route('/update_category/<id>', methods=['GET', 'POST'])
def update_category(id):
    category = Categorypost.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.category = form.name.data

        db.session.add(category)
        db.session.commit()
        return redirect(url_for('.category_crud'))

    form.name.data = category.category
    categories = Categorypost.query.all()
    return render_template('category_crud.html', categories=categories, form=form)


@post_blueprint.route('/delete_category/<id>', methods=['GET'])
@login_required
def delete_category(id):
    category = Categorypost.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('.category_crud'))


@post_blueprint.route('/add_city', methods=['GET', 'POST'])
def add_city():
    form = CityForm()
    if form.validate_on_submit():
        city = Citypost(city=form.city.data)
        db.session.add(city)
        db.session.commit()
        return redirect(url_for('.add_city'))

    cities = Citypost.query.all()
    return render_template('add_city.html', cities=cities, form=form)


@post_blueprint.route('/update_city/<id>', methods=['GET', 'POST'])
def update_city(id):
    city = Citypost.query.get_or_404(id)
    form = CityForm()
    if form.validate_on_submit():
        city.city = form.city.data
        db.session.add(city)
        db.session.commit()
        return redirect(url_for('.add_city'))

    form.city.data = city.city
    cities = Citypost.query.all()
    return render_template('add_city.html', cities=cities, form=form)


@post_blueprint.route('/delete_city/<id>', methods=['GET'])
@login_required
def delete_city(id):
    city = Citypost.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()

    return redirect(url_for('.add_city'))

@post_blueprint.route('/add_status', methods=['GET', 'POST'])
def add_status():
    form = StatusForm()
    if form.validate_on_submit():
        status = Statuspost(status=form.status.data)
        db.session.add(status)
        db.session.commit()
        return redirect(url_for('.add_status'))

    statuses = Statuspost.query.all()
    return render_template('add_status.html', statuses=statuses, form=form)


