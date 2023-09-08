#    Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
#    CSD460 Capstone Project
#
#    forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, IntegerField, BooleanField
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

class NewReservation(FlaskForm):
    room_number = SelectField(u'Room Choice', name="room_number", choices=[
        ('1a', '1a'), ('1b', '1b'), ('1c', '1c'), ('1d', '1d'), ('1e', '1e'),
        ('1f', '1f'), ('1g', '1g'), ('1h', '1h'), ('2a', '2a'), ('2b', '2b'),
        ('2c', '2c'), ('2d', '2d'), ('2e', '2e'), ('2f', '2f'), ('2g', '2g'), ('2h', '2h')
    ])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    num_of_guests = IntegerField('Number of Guests', validators=[DataRequired()])
    confirmation = BooleanField('Confirm Reservation', default=False)
    submit = SubmitField('Submit')
    # Add this to your Python code to include a hidden field for confirmation


class ConfirmReservation(FlaskForm):
    submit = SubmitField('Confirm Reservation')



