from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms import validators
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from incollege.models import User


class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    lname = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    username = StringField('Username', validators=[DataRequired(), 
                            Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(),
                            Length(min=8, max=12)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
                            Length(min=8, max=12), EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
                            Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists!')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')