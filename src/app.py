from flask import Flask
from profile import profile_bp
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")

app.register_blueprint(profile_bp)
db = SQLAlchemy(app)

with app.app_context():
    db.drop_all()
    db.create_all()


@app.route("/")
def index():
    return "Index page"
