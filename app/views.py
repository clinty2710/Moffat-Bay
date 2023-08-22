from flask import render_template

def configure_views(app):
    @app.route("/")
    def index():
        return render_template("index.html")
