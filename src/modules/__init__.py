from flask import Blueprint

bp = Blueprint("modules_page", __name__)

from modules import basic
from modules import alll
from modules import savePlan
from modules import loadPlan
