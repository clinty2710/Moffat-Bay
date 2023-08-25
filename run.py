from app import app, create_tables
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Flask app')
    parser.add_argument('--init', action='store_true', help='Initialize the database')
    args = parser.parse_args()
    if args.init:
        create_tables()  # Initialize the database tables

    from app import views  # Import views after initializing app and db
    app.debug = True
    app.run()  # Run the Flask app
