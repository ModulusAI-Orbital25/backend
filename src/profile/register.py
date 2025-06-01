from flask import request, jsonify
from app import db
from profile import bp  # type: ignore
from models import User
from flask import url_for
import traceback


@bp.route("/profile/register", methods=["POST"])
def register():
    try:
        username = request.get_json().get("username")
        password = request.get_json().get("password")

        new_user = User(name=username, display_name=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"redirect" : url_for("index")})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500
