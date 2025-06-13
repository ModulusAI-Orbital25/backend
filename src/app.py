from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
app.config.from_object("config.Config")

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth_page.login"

import models

with app.app_context():
    db.drop_all()
    db.create_all()

from profile import bp as profile_bp

app.register_blueprint(profile_bp)

from auth import bp as auth_bp

app.register_blueprint(auth_bp)

from chat import bp as chat_bp

app.register_blueprint(chat_bp)

from modules import bp as modules_bp

app.register_blueprint(modules_bp)

with app.app_context():
    from modules.basic import load_basic_information

    load_basic_information()


@app.route("/")
def index():
    return "Index page"
