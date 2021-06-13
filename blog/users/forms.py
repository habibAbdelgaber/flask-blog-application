from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, BooleanField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Email, EqualTo, DataRequired, Length


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Password confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_field(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('this username already exist, please choose different username!')

    def validate_field(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('this email already exist, please choose different email!')


class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    img = FileField('Update image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Profile')

    def validate_field(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('this username already exist, please choose different username!')

    def validate_field(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('this email already exist, please choose different email!')


class RequestPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_field(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if not user:
                raise ValidationError('the user you have request to reset password not exist')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Password confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')