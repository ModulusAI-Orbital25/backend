from flask import Blueprint

bp = Blueprint("modules_page", __name__)

from modules import basic
