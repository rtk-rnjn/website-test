import flask_login
from flask import Flask

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = "super secret string"

from .routes import *  # noqa: F401, F403, E402
