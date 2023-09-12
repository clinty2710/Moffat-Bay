#    Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
#    CSD460 Capstone Project
#
#    run.py

from app import app, create_tables
import argparse
from flask_debugtoolbar import DebugToolbarExtension 
import secrets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Flask app')
    parser.add_argument('--init', action='store_true', help='Initialize the database')
    #add debug option
    parser.add_argument('--debug', action='store_true', help='Run in debug mode, with toolbar')
    args = parser.parse_args()
    if args.init:
        create_tables()  # Initialize the database tables
    #set debug mode
    if args.debug:
        app.debug = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        app.config['SQLALCHEMY_ECHO'] = True
    else:
        app.debug = False



    toolbar = DebugToolbarExtension(app)
    app.run()