from app.db import db


class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        uid (int): The unique identifier for the user (primary key).
        Email (str): The user's email address (255 characters, not nullable).
        First_name (str): The user's first name (255 characters).
        Last_name (str): The user's last name (255 characters).
        Phone_number (str): The user's phone number (up to 20 characters).
        Password (str): The user's password (255 characters).
        
    Relationships:
        reservations (list of Reservation): A list of reservations associated with the user.

    """
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), nullable=False)
    First_name = db.Column(db.String(255))
    Last_name = db.Column(db.String(255))
    Phone_number = db.Column(db.String(20))
    Password = db.Column(db.String(255))
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Reservation(db.Model):
    """
    Represents a reservation in the application.

    Attributes:
        rid (int): The unique identifier for the reservation (primary key).
        start_date (Date): The start date of the reservation.
        end_date (Date): The end date of the reservation.
        room_number (str): The room number for the reservation (up to 10 characters).
        num_of_guests (int): The number of guests for the reservation.
        price (float): The price associated with the reservation.
        user_id (int): The foreign key referencing the associated user.

    Relationships:
        user (User): The user associated with this reservation.

    """
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    room_number = db.Column(db.String(10))
    num_of_guests = db.Column(db.Integer)
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))  # Foreign key to User table