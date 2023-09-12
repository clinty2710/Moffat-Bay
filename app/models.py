from app.db import db


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), nullable=False)
    First_name = db.Column(db.String(255))
    Last_name = db.Column(db.String(255))
    Phone_number = db.Column(db.String(20))
    Password = db.Column(db.String(255))
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Reservation(db.Model):
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    room_number = db.Column(db.String(10))
    num_of_guests = db.Column(db.Integer)
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))  # Foreign key to User table