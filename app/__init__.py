from flask import Flask
from .views import configure_views

app = Flask(__name__, template_folder="templates")
configure_views(app)
