from flask import Blueprint

bp = Blueprint("profile page", __name__)

from profile import info, register
