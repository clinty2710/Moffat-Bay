#    Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
#    CSD460 Capstone Project
#
#    views.py

from flask import render_template, render_template, redirect, request, url_for, flash, session
from app import app, User, Reservation, db
from app.forms import LoginForm, NewReservation, RegistrationForm, ForgotPasswordForm, UpdateProfile
import bcrypt


#generate salt
salt = bcrypt.gensalt()

#session key for user logged in
@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return dict(user=user)
    return dict(user=None)

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
            session['user_id'] = user.uid  # Store user's ID in the session
            flash('Logged in successfully!', 'info')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user = User.query.filter_by(Email=request.form['Email']).first()
        if user:
            flash('Please check your email for a password reset link.', 'info')
            return redirect(url_for('index'))
        else:
            flash('Email address not found.', 'danger')
            return redirect(url_for('forgot_password'))
    else:
        form = ForgotPasswordForm()
        flash('Please enter your email address.', 'info')
        return render_template('forgot_password.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user's ID from the session
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = User.query.filter_by(uid=session['user_id']).first()
    form = UpdateProfile()

    if request.method == 'POST':

        form = UpdateProfile(request.form)
        new_password = form.Password.data
        if new_password:
            # Hash the new password and store it securely
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.Password = hashed_password

        # Update the user's information based on the form data
        user.Email = form.Email.data
        user.First_name = form.First_name.data
        user.Last_name = form.Last_name.data
        user.Phone_number = form.Phone_number.data

        # Save the changes to the database
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    form.Email.data = user.Email
    form.First_name.data = user.First_name
    form.Last_name.data = user.Last_name
    form.Phone_number.data = user.Phone_number

    return render_template('profile.html', form=form, user=user)

@app.route('/new_reservation', methods=['GET', 'POST'])
def new_reservation():
    if not session.get('user_id'):
        flash('Please login to make a reservation.', 'info')
        return redirect(url_for('login'))
    if request.method == 'POST':
        form = NewReservation(request.form)
        return render_template('confirm_reservation.html', form=form)
    elif request.method == 'GET':
        form = NewReservation()
        return render_template('reservation.html', form=form)
    
@app.route('/confirm_reservation', methods=['POST'])
def confirm_reservation():
    form = NewReservation(request.form)
    if form.validate_on_submit():
        # Create a new reservation and save to the database
        new_reservation = Reservation(
            room_number=form.room_number.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            num_of_guests=form.num_of_guests.data,
            user_id=session['user_id']  # Store the user's ID in the reservation
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('Reservation created successfully!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Reservation failed. Please check your information and try again.', 'danger')
        return redirect(url_for('new_reservation'))

@app.route('/show_reservations', methods=['GET'])
def show_reservations():
    if not session.get('user_id'):
        flash('Please login to view your reservations.', 'info')
        return redirect(url_for('login'))
    reservations = Reservation.query.filter_by(user_id=session['user_id']).all()
    return render_template('show_reservations.html', reservations=reservations)