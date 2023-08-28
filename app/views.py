from flask import render_template, render_template, redirect, request, url_for, flash
from markupsafe import Markup
from app import app, User, Reservation, db
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
import bcrypt

#generate salt
salt = bcrypt.gensalt()

class RegistrationForm(FlaskForm):
    First_name = StringField('First Name', validators=[DataRequired()])
    Last_name = StringField('Last Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Phone_number = StringField('Phone Number', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    Confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/show_database')
def show_database():
    users = User.query.all()
    reservations = Reservation.query.all()
    return render_template('db.html', users=users, reservations=reservations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created successfully!', 'success')
        
        # Generate a salt and hash the password before saving to the database
        hashed_password = bcrypt.hashpw(form.Password.data.encode('utf-8'), salt)
        
        # Create a new user and save to the database
        new_user = User(
            Email=form.Email.data,
            First_name=form.First_name.data,
            Last_name=form.Last_name.data,
            Phone_number=form.Phone_number.data,
            Password=hashed_password  # Save the hashed password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Fetch the user from the database based on the provided email
        user = User.query.filter_by(Email=form.username.data).first()

        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.Password.encode('utf-8')):
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

