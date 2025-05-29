from flask import Flask
from profile import profile_page

app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(profile_page)

@app.route("/")
def index():
    return "Index page"
