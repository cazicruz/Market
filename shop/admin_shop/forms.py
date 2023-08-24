from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from .models import Users
from shop import bcrypt



class LoginForm(FlaskForm):
    username = StringField(' Username: ', validators=[InputRequired()], render_kw={"placeholder": "username"})
    password = PasswordField(' Password: ',validators=[DataRequired(message='Required'), Length(10)], render_kw={"placeholder": "password"})
    loginButton = SubmitField('Login')


class SignUpForm(FlaskForm):
    fname = StringField('firstname', validators=[DataRequired()],  render_kw={"placeholder": "first name"})
    lname = StringField('lastname', validators=[DataRequired()], render_kw={"placeholder": "last name"})
    email = EmailField('email', validators=[DataRequired()],  render_kw={"placeholder": "Email"})
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "pick a username"})
    address = StringField('address', validators=[DataRequired(), Length(10)], render_kw={"placeholder": "address"})
    password1 = PasswordField(U' Password: ',validators=[InputRequired(message='Required'), Length(10)])
    password2 = PasswordField(U'Confirm Password: ',validators=[InputRequired(message='Required'), Length(10), EqualTo('password1')])
    profile_img = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'image only pls')])
    submit = SubmitField('submit')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists.")
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists.")
