from flask import request, jsonify, redirect, url_for, flash
from flask_login import login_user
from app import login_manager
from auth import bp
from models import User
import traceback

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route("/login", methods=["POST"])
def login():
    try:
        username = request.get_json().get("username")
        # TODO: Add password field + check for password

        user = User.query.filter_by(name=username).first()

        if not user:
            flash("Wrong login details")
            return redirect(url_for("auth_page.login"))

        login_user(user=user)
        return redirect(url_for("index"))

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500
