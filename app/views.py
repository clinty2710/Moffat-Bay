from flask import render_template, render_template, redirect, request, url_for, flash, session
from app import app, User, Reservation, db
from app.forms import LoginForm, RegistrationForm
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
            flash('Login successful!', 'success')
            session['user_id'] = user.uid  # Store user's ID in the session
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user's ID from the session
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))
