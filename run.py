from app import app, create_tables

if __name__ == "__main__":
    create_tables()  # Initialize the database tables

    from app import views  # Import views after initializing app and db

    app.run()  # Run the Flask app
