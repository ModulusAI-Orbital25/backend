from flask import Flask
from profile import profile_page
from db import db

app = Flask(__name__)
app.config.from_object("config.Config")

app.register_blueprint(profile_page)
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route("/")
def index():
    return "Index page"
