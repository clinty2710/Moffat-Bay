from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import pymysql

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_DATABASE']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define User and Reservation models
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), nullable=False)
    First_name = db.Column(db.String(255))
    Last_name = db.Column(db.String(255))
    Phone_number = db.Column(db.String(20))
    Password = db.Column(db.String(255))

class Reservation(db.Model):
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    room_number = db.Column(db.String(10))
                            
# Function to create tables and insert sample data
def create_tables():
    with app.app_context():
        try:
            # Create the database if it doesn't exist
            connection = pymysql.connect(
                host=os.environ['DB_HOST'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.environ['DB_DATABASE']}")
            connection.commit()
            connection.close()
            db.create_all()

            # Insert data into the User table
            users_to_insert = [
                User(Email="user1@example.com", First_name="John", Last_name="Doe", Phone_number="123-456-7890", Password="password1"),
                User(Email="user2@example.com", First_name="Jane", Last_name="Smith", Phone_number="987-654-3210", Password="password2")
            ]
            db.session.bulk_save_objects(users_to_insert)
            db.session.commit()

            # Insert data into the Reservation table
            reservations_to_insert = [
                Reservation(start_date="2023-08-21", end_date="2023-08-23", room_number="2b"),
                Reservation(start_date="2023-09-05", end_date="2023-09-10", room_number="3a"),
                Reservation(start_date="2023-10-15", end_date="2023-10-20", room_number="8b")
            ]
            db.session.bulk_save_objects(reservations_to_insert)
            db.session.commit()

            print("Database initialization and data insertion successful!")

        except Exception as e:
            print("Error:", e)

# Import views after initializing app and db
from app import views

if __name__ == "__main__":
    create_tables()  # Initialize the database tables
    app.run()
