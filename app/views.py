from flask import render_template
from app import app

# Define your view functions and routes here
# For example:
@app.route("/")
def index():
    return render_template("index.html")
