from flask import Blueprint

profile_bp = Blueprint("profile page", __name__)

from profile import info
