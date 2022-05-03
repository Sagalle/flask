from .models import User, Post, Comment, Album, Photo, Todo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


class AddUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 128)])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 128),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 128),
                                             Email()])
    street = StringField('Street', validators=[DataRequired(), Length(1, 128)])
    suite = StringField('Suite', validators=[DataRequired(), Length(1, 128)])
    city = StringField('City', validators=[DataRequired(), Length(1, 128)])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(1, 128)])
    lat = StringField('Latitude', validators=[DataRequired(), Length(1, 128)])
    lng = StringField('Longitude', validators=[DataRequired(), Length(1, 128)])
    phone = StringField('Phone', validators=[DataRequired(), Length(1, 128)])
    website = StringField('Website', validators=[DataRequired(), Length(1, 128)])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(1, 128)])
    company_catchPhrase = StringField('CatchPhrase', validators=[DataRequired(), Length(1, 128)])
    company_bs = StringField('Company Description', validators=[DataRequired(), Length(1, 128)])

    password_hash = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(1, 128)])
    username = StringField('Username', validators=[Length(1, 128)])
    city = StringField('Location', validators=[Length(1, 128)])
    phone = StringField('Phone Number', validators=[Length(1, 128)])
    company_name = StringField('Company Name', validators=[Length(1, 128)])
    company_bs = TextAreaField('About me')
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title of your post', validators=[Length(1, 128)])
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    name = StringField("Comment title", validators=[Length(1, 128)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 128),
                                             Email()])
    body = PageDownField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class TodoForm(FlaskForm):
    title = StringField('Title of your todo', validators=[Length(1, 128)])
    submit = SubmitField('Submit')

