from flask import request, jsonify, redirect, url_for, flash
from flask_login import login_user, current_user, login_required
from app import login_manager
from auth import bp
from models import User
import traceback

@bp.route("/me", methods=["GET"])
def me():
    if current_user.is_authenticated:
        return jsonify({"logged_in": True, "username": current_user.name})
    return jsonify({"logged_in": False})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route("/login", methods=["POST"])
def login():
    try:
        username = request.get_json().get("username")
        password = request.get_json().get("password")

        user = User.query.filter_by(name=username).first()

        if (not user) or (not user.check_password(password)):
            return jsonify({"redirect": url_for("auth_page.login")})

        login_user(user=user)
        return jsonify({"redirect": url_for("index")})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500
