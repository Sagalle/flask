from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Too very hard to guess.'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupe6:groupe6@localhost/myflaskbase'
    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    from .views import views  # import the blueprint package

    app.register_blueprint(views, url_prefix='/')

    from .models import User, Post, Comment, Photo, Todo, Album
    from .forms import AddUserForm, EditProfileForm, PostForm, CommentForm, LoginForm, TodoForm

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/myflaskbase.db'):
        db.create_all(app=app)
        print('Database Created!')
