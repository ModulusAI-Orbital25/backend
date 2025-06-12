from flask import Blueprint

bp = Blueprint("chat_page", __name__)

from chat import groq