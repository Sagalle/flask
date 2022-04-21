from flask import Blueprint, render_template, request, flash, jsonify, current_app, url_for
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .forms import LoginForm, EditProfileForm, PostForm, AddUserForm, CommentForm
from .models import User, Photo, Post, Comment, Todo, Album
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
def home():
    per_page = 5
    user = User.query.filter_by().all()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(User.timestamp.desc()).paginate(
        page, per_page,
        error_out=False)

    users = pagination.items

    return render_template('home.html', users=users, user=user,
                           pagination=pagination)


@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('.home')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('login.html', form=form)


@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.home'))


@views.route('/add_user')
def add_user():
    return render_template('login.html')


@views.route('/user/<int:id>')
def user_profile():
    return render_template('profile.html')


@views.route('/delete_user')
def delete_user():
    return render_template('delete_user.html')


@views.route('/update_user')
def update_user():
    return render_template('update_user.html')
