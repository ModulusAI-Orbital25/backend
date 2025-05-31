from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)
app.config.from_object("config.Config")
app.debug = True
app.secret_key = "modulusai"

db = SQLAlchemy(app)
login_manager = LoginManager(app)

import models

with app.app_context():
    db.drop_all()
    db.create_all()

from profile import bp as profile_bp

app.register_blueprint(profile_bp)

from auth import bp as auth_bp

app.register_blueprint(auth_bp)


@app.route("/")
def index():
    return "Index page"
