#    Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
#    CSD460 Capstone Project
#
#    forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    """
    Represents a login form for user authentication.

    Fields:
        username (StringField): The field for entering the email (username) with validation.
        password (PasswordField): The field for entering the password with validation.
        submit (SubmitField): The submit button for submitting the form.

    Validators:
        - username: DataRequired (ensures the field is not empty) and Email (validates email format).
        - password: DataRequired (ensures the field is not empty).

    """
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """
    Represents a registration form for user account creation.

    Fields:
        First_name (StringField): The field for entering the user's first name with validation.
        Last_name (StringField): The field for entering the user's last name with validation.
        Email (StringField): The field for entering the user's email with validation.
        Phone_number (StringField): The field for entering the user's phone number with validation.
        Password (PasswordField): The field for entering the user's password with validation.
        Confirm_password (PasswordField): The field for confirming the user's password with validation.
        submit (SubmitField): The submit button for submitting the form.

    Validators:
        - First_name: DataRequired (ensures the field is not empty).
        - Last_name: DataRequired (ensures the field is not empty).
        - Email: DataRequired (ensures the field is not empty) and Email (validates email format).
        - Phone_number: DataRequired (ensures the field is not empty).
        - Password: DataRequired (ensures the field is not empty) and Length (minimum length of 8 characters).
        - Confirm_password: DataRequired (ensures the field is not empty) and EqualTo (compares with 'Password').

    """
    First_name = StringField('First Name', validators=[DataRequired()])
    Last_name = StringField('Last Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Phone_number = StringField('Phone Number', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=8) ])
    Confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Register')

class ForgotPasswordForm(FlaskForm):
    """
    Represents a form for users to request a password reset.

    Fields:
        Email (StringField): The field for entering the user's email with validation.
        submit (SubmitField): The submit button for submitting the form.

    Validators:
        - Email: DataRequired (ensures the field is not empty) and Email (validates email format).

    """
    Email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class UpdateProfile(FlaskForm):
    """
    Represents a form for users to update their profile information.

    Fields:
        First_name (StringField): The field for entering the user's updated first name with validation.
        Last_name (StringField): The field for entering the user's updated last name with validation.
        Email (StringField): The field for entering the user's updated email with validation.
        Phone_number (StringField): The field for entering the user's updated phone number with validation.
        Password (PasswordField): The field for entering the user's updated password with validation.
        submit (SubmitField): The submit button for updating the profile.

    Validators:
        - First_name: DataRequired (ensures the field is not empty).
        - Last_name: DataRequired (ensures the field is not empty).
        - Email: DataRequired (ensures the field is not empty) and Email (validates email format).
        - Phone_number: DataRequired (ensures the field is not empty).
        - Password: Length (minimum length of 8 characters).

    """
    First_name = StringField('First Name', validators=[DataRequired()])
    Last_name = StringField('Last Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Phone_number = StringField('Phone Number', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[Length(min=8)] )
    submit = SubmitField('Update Profile')

class NewReservation(FlaskForm):
    """
    Represents a form for users to create a new reservation.

    Fields:
        room_number (SelectField): The field for selecting a room choice.
        start_date (DateField): The field for entering the reservation's start date with validation.
        end_date (DateField): The field for entering the reservation's end date with validation.
        num_of_guests (IntegerField): The field for entering the number of guests with validation.
        confirmation (BooleanField): The field for confirming the reservation (default is False).
        submit (SubmitField): The submit button for submitting the form.

    Validators:
        - start_date: DataRequired (ensures the field is not empty).
        - end_date: DataRequired (ensures the field is not empty).
        - num_of_guests: DataRequired (ensures the field is not empty).

    """
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
    """
    Represents a form for users to confirm a reservation.

    Fields:
        submit (SubmitField): The submit button for confirming the reservation.

    """
    submit = SubmitField('Confirm Reservation')

class SearchByEmailOrRID(FlaskForm):
    """
    Represents a form for searching reservations by email or reservation ID.

    Fields:
        email (StringField): The field for entering an email address for searching reservations (with email validation).
        reservation (IntegerField): The field for entering a reservation ID for searching reservations.
        submit (SubmitField): The submit button for initiating the search.

    Validators:
        - email: Email (validates email format).

    """
    email = StringField('Email', validators=[Email()])
    reservation = IntegerField('Reservation ID')
    submit = SubmitField('Search')



