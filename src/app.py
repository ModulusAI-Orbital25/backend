from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)

import models

with app.app_context():
    db.drop_all()
    db.create_all()

from profile import bp as profile_bp

app.register_blueprint(profile_bp)


@app.route("/")
def index():
    return "Index page"
