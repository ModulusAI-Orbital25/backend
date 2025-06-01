from flask import Blueprint

bp = Blueprint("profile_page", __name__)

from profile import info, register
