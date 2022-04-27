import os.path

from flask import Blueprint, render_template, request, flash, jsonify, current_app, url_for
from flask_login import login_required, current_user, logout_user, login_user
from sqlalchemy.orm import query
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .forms import LoginForm, EditProfileForm, PostForm, AddUserForm, CommentForm, TodoForm
from .models import User, Photo, Post, Comment, Todo, Album
from . import db

views = Blueprint('views', __name__)


@views.route('', methods=['GET', 'POST'])
def home():
    form = AddUserForm()
    users = User.query.filter_by().all()
    per_page = 5
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            street=form.street.data,
            suite=form.suite.data,
            city=form.city.data,
            zipcode=form.zipcode.data,
            lat=form.lat.data,
            lng=form.lng.data,
            phone=form.phone.data,
            website=form.website.data,
            company_name=form.company_name.data,
            company_catchPhrase=form.company_catchPhrase.data,
            company_bs=form.company_bs.data,
            password_hash=form.password_hash.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User added succesfully!')
        return redirect(url_for('.home'))
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.member_since.desc()).paginate(
        page, per_page=per_page,
        error_out=False)
    posts = pagination.items
    return render_template('home.html', form=form, posts=posts,
                           pagination=pagination, users=users)


@views.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None and not user.check_password(form.password.data): # or
            flash('Invalid email or password.', 'danger')
        else:
            login_user(user, form.remember_me.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('.user_profile', username=user.username))
    return render_template('login.html', form=form, user=current_user)


@views.route('edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated successfully', 'success')
        return redirect(url_for('.user_profile', username=current_user.username))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@views.route('comment/<username>', methods=['GET', 'POST'])
@login_required
def comment(username):
    user = User.query.filter_by(username=username).first_or_404()
    comments = Comment.query.filter_by().all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(name=form.name.data,
                          email=form.email.data,
                          body=form.body.data)

        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.comment', username=user.username))
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.date.asc()).paginate(
        page, per_page=10,
        error_out=False)
    items = pagination.items
    return render_template('comment.html', user=user, form=form,
                           comments=comments, items=items, pagination=pagination)


@views.route('logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('.home'))


@views.route('user/<username>', methods=['GET', 'POST'])
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by().all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data
                    )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.user_profile', username=user.username))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.date.desc()).paginate(
        page, per_page=10,
        error_out=False)
    items_ = pagination.items
    return render_template('profile.html', form=form, posts=posts, items_=items_, user=user,
                           pagination=pagination)


@views.route('delete-user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    user = User.query.get(id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('User was deleted successfully', 'success')
        return redirect(url_for('.home'))
    return jsonify({})


@views.route('edit-comment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    comment = Comment.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment.name = form.name.data
        comment.email = form.email.data
        comment.body = form.body.data
        db.session.add(comment)
        db.session.commit()
        flash('The comment has been updated successfully', 'success')
        return redirect(url_for('.comment', username=current_user.username))
    form.name.data = comment.name
    form.email.data = comment.email
    form.body.data = comment.body
    return render_template('edit_comment.html', form=form)



@views.route('album', methods=['GET', 'POST'])
def album():
    return render_template('album.html')


@views.route('todo/<username>', methods=['GET', 'POST'])
def todo(username):
    user = User.query.filter_by(username=username).first_or_404()
    todos = Todo.query.filter_by().all()
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(
            title=form.title.data)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('.todo', username=user.username))
    page = request.args.get('page', 1, type=int)
    pagination = Todo.query.order_by(Todo.date.desc()).paginate(
        page, per_page=10,
        error_out=False)
    items = pagination.items
    return render_template('todo.html', form=form, todos=todos, items=items, pagination=pagination, user=user)


@views.route('edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.city = form.city.data
        current_user.phone = form.phone.data
        current_user.company_name = form.company_name.data
        current_user.company_bs = form.company_bs.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been update!', 'success')
        return redirect(url_for('.user_profile', username=current_user.username))
    form.name.data = current_user.name
    form.username.data = current_user.username
    form.city.data = current_user.city
    form.phone.data = current_user.phone
    form.company_name.data = current_user.company_name
    form.company_bs.data = current_user.company_bs
    return render_template('edit_profile.html', form=form)

@views.route('edit-post', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post was deleted successfully', 'success')
        return redirect(url_for('.user_profile', username=current_user.username))
    return jsonify({})



@views.route('add-user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            street=form.street.data,
            suite=form.suite.data,
            city=form.city.data,
            zipcode=form.zipcode.data,
            lat=form.lat.data,
            lng=form.lng.data,
            phone=form.phone.data,
            website=form.website.data,
            company_name=form.company_name.data,
            company_catchPhrase=form.company_catchPhrase.data,
            company_bs=form.company_bs.data,
            password_hash=form.password_hash.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User added succesfully!', 'success')
        return redirect(url_for('.home'))
    return render_template('add_user.html', form=form)


@views.context_processor
def override_url():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(views.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)