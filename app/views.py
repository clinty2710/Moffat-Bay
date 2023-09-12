#    Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
#    CSD460 Capstone Project
#
#    views.py

import datetime
from flask import jsonify, Blueprint, render_template, render_template, redirect, request, url_for, flash, session
from sqlalchemy import and_, or_
from app.forms import LoginForm, NewReservation, RegistrationForm, ForgotPasswordForm, SearchByEmailOrRID, UpdateProfile
import bcrypt
from app.models import User, Reservation

bp = Blueprint('app', __name__)


@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

#generate salt
salt = bcrypt.gensalt()

#session key for user logged in
@bp.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return dict(user=user)
    return dict(user=None)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route('/show_database')
def show_database():
    users = User.query.all()
    reservations = Reservation.query.all()
    return render_template('db.html', users=users, reservations=reservations)

@bp.route('/register', methods=['GET', 'POST'])
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
        session['user_id'] = new_user.uid #login a user automatically when registering.
        return redirect(url_for('app.index'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Fetch the user from the database based on the provided email
        user = User.query.filter_by(Email=form.username.data).first()

        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.Password.encode('utf-8')):
            session['user_id'] = user.uid  # Store user's ID in the session
            flash('Logged in successfully!', 'info')
            next_url = request.args.get('next', '/')
            return redirect(next_url)
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user = User.query.filter_by(Email=request.form['Email']).first()
        if user:
            flash('Please check your email for a password reset link.', 'info')
            return redirect(url_for('app.index'))
        else:
            flash('Email address not found.', 'danger')
            return redirect(url_for('app.forgot_password'))
    else:
        form = ForgotPasswordForm()
        flash('Please enter your email address.', 'info')
        return render_template('forgot_password.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user's ID from the session
    flash('Logged out successfully!', 'info')
    return redirect(url_for('app.index'))

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user_id'):
        flash('Please login to change your profile.', 'info')
        return redirect(url_for('app.login', next=request.url))
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
        #below line commented out to stop changing the email address
        #user.Email = form.Email.data
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

@bp.route('/reservation/new', methods=['GET', 'POST'])
def new_reservation():
    if not session.get('user_id'):
        flash('Please login to make a reservation.', 'info')
        return redirect(url_for('app.login', next=request.url))

    form = NewReservation()
    reservation_id = None 

    if form.validate_on_submit():
        if form.confirmation.data:
            room_number = form.room_number.data
            start_date = form.start_date.data
            end_date = form.end_date.data
            num_of_guests = form.num_of_guests.data
            room_price = price_of_room(num_of_guests) * (end_date - start_date).days

            if start_date > end_date:
                flash('Please select a valid date range.', 'danger')
                return redirect(url_for('app.new_reservation'))
            if start_date < datetime.date.today():
                flash('Please select a valid date (after today).', 'danger')
                return redirect(url_for('app.new_reservation'))
            
            new_reservation = Reservation(
                room_number=room_number,
                start_date=start_date,
                end_date=end_date,
                num_of_guests=num_of_guests,
                price=room_price,
                user_id=session['user_id']
            )
            db.session.add(new_reservation)
            db.session.commit()

            flash('Reservation added successfully!', 'success')
            return redirect(url_for('app.show_reservations'))
        else:
            return render_template('reservation.html', reservation_id=reservation_id, form=form)

    return render_template('reservation.html', reservation_id=reservation_id, form=form)

@bp.route('/reservation/edit/<int:reservation_id>', methods=['GET', 'POST'])
def edit_reservation(reservation_id):
    if not session.get('user_id'):
        flash('Please login to edit a reservation.', 'info')
        return redirect(url_for('app.login', next=request.url))

    reservation = Reservation.query.get(reservation_id)

    if reservation is None:
        flash('Reservation not found.', 'danger')
        return redirect(url_for('app.show_reservations'))

    if reservation.user_id != session['user_id']:
        flash('You do not have permission to edit this reservation.', 'danger')
        return redirect(url_for('app.show_reservations'))

    form = NewReservation(obj=reservation)

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        if start_date > end_date:
            flash('Please select a valid date range.', 'danger')
            return redirect(url_for('app.new_reservation'))
        if start_date < datetime.date.today():
            flash('Please select a valid date (after today).', 'danger')
            return redirect(url_for('app.new_reservation'))

        if form.confirmation.data:
            form.populate_obj(reservation)
            #price of room * number of days:
            reservation.price = price_of_room(reservation.num_of_guests) * (reservation.end_date - reservation.start_date).days
            #check if date is already taken by someone else
            reservations = Reservation.query.filter(
                and_(
                    Reservation.start_date <= end_date,
                    Reservation.end_date >= start_date
                )
            ).all()
            for r in reservations:
                if r.room_number == reservation.room_number and r.rid != reservation.rid:
                    flash('Room is already reserved for that date.', 'danger')
                    return redirect(url_for('app.edit_reservation', reservation_id=reservation_id))
            db.session.commit()
            flash('Reservation updated successfully!', 'success')
            return redirect(url_for('app.show_reservations'))
        else:
            return render_template('reservation.html', form=form, reservation_id=reservation_id)

    return render_template('reservation.html', form=form, reservation_id=reservation_id)

def price_of_room(num_guests):
    guests = int(num_guests)
    if guests <= 2:
        return 115 * 1.05
    elif guests <= 5:
        return 150 * 1.05
    elif guests >= 6:
        return None

@bp.route('/show_reservations', methods=['GET'])
def show_reservations():
    if not session.get('user_id'):
        flash('Please login to view your reservations.', 'info')
        return redirect(url_for('app.login', next=request.url))
    reservations = Reservation.query.filter_by(user_id=session['user_id']).all()
    return render_template('show_reservations.html', reservations=reservations)

@bp.route('/delete_reservation')
def delete_reservation():
    if not session.get('user_id'):
        flash('Please login to delete a reservation.', 'info')
        return redirect(url_for('app.login', next=request.url))
    reservation_id = request.args.get('reservation_id')
    reservation = Reservation.query.get(reservation_id)
    if reservation is None:
        flash('Reservation not found.', 'danger')
        return redirect(url_for('app.show_reservations'))
    if reservation.user_id != session['user_id']:
        flash('You do not have permission to delete this reservation.', 'danger')
        return redirect(url_for('app.show_reservations'))
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation deleted successfully!', 'success')
    return redirect(url_for('app.show_reservations'))

@bp.route('/get_room_availability', methods=['GET'])
def get_room_availability():
    if not session.get('user_id'):
        flash('Please login to view room availability.', 'info')
        return redirect(url_for('app.login', next=request.url))

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date and end_date:
        reservations = Reservation.query.filter(
            and_(
                Reservation.start_date <= end_date,
                Reservation.end_date >= start_date
            )
        ).all()

        unavailable_rooms = [str(r.room_number) for r in reservations]

        return jsonify(unavailable_rooms)

    return jsonify([])

@bp.route('/get_room_price', methods=['GET'])
def get_room_price():
    num_of_guests = request.args.get('num_of_guests')
    num_of_days = int(request.args.get('num_of_days', 1))
    if num_of_guests:
        price = f"Price: ${price_of_room(num_of_guests) * num_of_days:.2f}"
        return jsonify(price)
    else:
        return jsonify(None)
    

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/attractions')
def attractions():
    return render_template('attractions.html')

@bp.route('/global_search', methods=['GET', 'POST'])
def global_search():
    form = SearchByEmailOrRID()

    email = None
    reservations = []

    if request.method == 'POST':
        email = form.email.data
        reservation = form.reservation.data

        if email or reservation:
            query = Reservation.query
            if email:
                user = User.query.filter_by(Email=email).first()
                if user:
                    query = query.filter(Reservation.user_id == user.uid)
                else:
                    flash('Email address not found.', 'danger')

            if reservation:
                if email:
                    query = query.filter(Reservation.rid == reservation, Reservation.user_id == user.uid)
                else:
                    query = query.filter(Reservation.rid == reservation)
                    if not email:
                        email = Reservation.query.filter_by(rid=reservation).first().user.Email
                        email = email[:3] + '...' + email[-3:]

            reservations = query.all()

            if not reservations:
                flash('No reservations found.', 'warning')

    return render_template('global_search.html', form=form, reservations=reservations, email=email)

