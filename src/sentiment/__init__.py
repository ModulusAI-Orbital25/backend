from flask import Blueprint

bp = Blueprint("sentiment_page", __name__)

from sentiment import bert