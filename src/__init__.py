import os
from typing import TYPE_CHECKING

import flask_login
from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient

if TYPE_CHECKING:
    from src.utils.types import FlaskClass
else:
    FlaskClass = Flask

csrf = CSRFProtect()
load_dotenv()

app: FlaskClass = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = os.getenv("SECRET_KEY", "")
csrf.init_app(app)

mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = int(os.getenv("MONGO_PORT", "27017"))

if mongo_uri := os.getenv("MONGO_URI"):
    mongo_client = MongoClient(mongo_uri, document_class=dict, tz_aware=True)
else:
    mongo_client = MongoClient(
        mongo_host, mongo_port, document_class=dict, tz_aware=True
    )

setattr(app, "mongo", mongo_client)

# ping to check if the connection is successful
try:
    response = mongo_client.admin.command("ping")
    ok = response["ok"]
    if int(ok) != 1:
        raise Exception("MongoDB connection failed")

except Exception as e:
    raise e

from .routes import *  # noqa: F401, F403, E402
