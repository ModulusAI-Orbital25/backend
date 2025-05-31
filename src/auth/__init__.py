from flask import Blueprint

bp = Blueprint("auth_page", __name__)

from auth import login
