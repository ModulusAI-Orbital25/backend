from flask import request, jsonify, url_for
from app import db
from models import Module
from modules import bp
from flask_login import current_user, login_required
@bp.route("/modules/alll", methods=["GET"])
@login_required
def get_all_modules():
    modules = Module.query.with_entities(Module.code).all()
    return jsonify({"modules": [m.code for m in modules]})
