#    Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
#    CSD460 Capstone Project
#
#    __init__.py


from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_caching import Cache
from flask_bootstrap import Bootstrap

import os
import pymysql

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})  # Set a timeout (in seconds)
cache.init_app(app)
bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)
secret_key = "TheQuickBrownFoxJumpsOverTheLazyDog"
app.secret_key = secret_key

from . import views
app.register_blueprint(views.bp)

# Function to create tables and insert sample data
def create_tables():
    from .models import db, User, Reservation
    with app.app_context():
        try:
            # Create the database if it doesn't exist
            connection = pymysql.connect(
                host=os.environ['DB_HOST'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
            )
            cursor = connection.cursor()
            #drop database if exists
            cursor.execute(f"DROP DATABASE IF EXISTS {os.environ['DB_DATABASE']}")
            #create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.environ['DB_DATABASE']}")
            connection.commit()
            connection.close()
            db.create_all()

            # Insert data into the User table
            users_to_insert = [
                User(Email="user1@example.com", First_name="John", Last_name="Doe", Phone_number="123-456-7890", Password="password1"),
                User(Email="user2@example.com", First_name="Jane", Last_name="Smith", Phone_number="987-654-3210", Password="password2"),
                User(Email="user3@example.com", First_name="Alice", Last_name="Johnson", Phone_number="555-555-5555", Password="password3"),
            ]
            db.session.bulk_save_objects(users_to_insert)
            db.session.commit()

            # Insert data into the Reservation table
            reservations_to_insert = [
                Reservation(start_date="2023-08-21", end_date="2023-08-23", room_number="2b", num_of_guests=2, price=112.21, user_id=1),
                Reservation(start_date="2023-09-05", end_date="2023-09-10", room_number="1a", num_of_guests=1, price=112.21, user_id=2),
                Reservation(start_date="2023-10-15", end_date="2023-10-20", room_number="2b", num_of_guests=3, price=112.21, user_id=3),
                Reservation(start_date="2023-11-01", end_date="2023-11-05", room_number="1a", num_of_guests=2, price=112.21, user_id=1),
                Reservation(start_date="2023-12-10", end_date="2023-12-15", room_number="2b", num_of_guests=4, price=112.21, user_id=2),
            ]
            db.session.bulk_save_objects(reservations_to_insert)
            db.session.commit()

            print("Database initialization and data insertion successful!")

        except Exception as e:
            print("Error:", e)


