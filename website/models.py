from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask import current_app, request
import hashlib


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, index=True)
    street = db.Column(db.String(128))
    suite = db.Column(db.String(128))
    city = db.Column(db.String(128))
    zipcode = db.Column(db.String(128))
    lat = db.Column(db.String(128))
    lng = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    website = db.Column(db.String(128))
    company_name = db.Column(db.String(128))
    company_catchPhrase = db.Column(db.String(128))
    company_bs = db.Column(db.String(128))
    posts = db.relationship('Post', backref='owned_user', lazy='dynamic')
    albums = db.relationship('Album', backref='owned_user', lazy='dynamic')
    todos = db.relationship('Todo', backref='owned_user', lazy='dynamic')


    password_hash = db.Column(db.String(128))

    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


class Post(db.Model):

    __tablename__ = 'posts'

    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment', backref='owned_post', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comments'

    postId = db.Column(db.Integer, db.ForeignKey('posts.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Album(db.Model):

    __tablename__ = 'albums'

    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    photos = db.relationship('Photo', backref='owned_album', lazy='dynamic')


class Photo(db.Model):
    __tablename__ = 'photos'

    albumId = db.Column(db.Integer, db.ForeignKey('albums.id'))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    url = db.Column(db.String(128))
    thumbnailUrl = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Todo(db.Model):
    __tablename__ = 'todos'

    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

