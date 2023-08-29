from app import app, create_tables
import argparse
from flask_debugtoolbar import DebugToolbarExtension 
import secrets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Flask app')
    parser.add_argument('--init', action='store_true', help='Initialize the database')
    #add debug option
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()
    if args.init:
        create_tables()  # Initialize the database tables
    #set debug mode
    if args.debug:
        app.debug = True
    else:
        app.debug = False

    from app import views  # only way i could get this to work, should probably fix this
    app.config['SECRET_KEY'] = 'TheQuickBrownFoxJumpsOverTheLazyDog'
    app.secret_key = secrets.token_hex(16)
    toolbar = DebugToolbarExtension(app)
    app.run()