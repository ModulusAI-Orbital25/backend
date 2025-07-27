from flask_login import LoginManager

login_manager = LoginManager()

from flask import Blueprint

bp = Blueprint("auth_page", __name__)

from auth import login
