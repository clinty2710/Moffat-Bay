from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    First_name = StringField('First Name', validators=[DataRequired()])
    Last_name = StringField('Last Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Phone_number = StringField('Phone Number', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=8) ])
    Confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Register')

class ForgotPasswordForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class UpdateProfile(FlaskForm):
    First_name = StringField('First Name', validators=[DataRequired()])
    Last_name = StringField('Last Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Phone_number = StringField('Phone Number', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[Length(min=8)] )
    submit = SubmitField('Update Profile')


