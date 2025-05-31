from flask import request, jsonify
from app import db
from profile import bp # type: ignore
from models import User


@bp.route("/profile/register", methods=["POST"])
def register():
    try:
        name = request.get_json().get("name")

        # Validate data
        # Try-catch for error

        new_user = User(name=name, display_name=name)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created", "user": new_user.id}), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Server error", "details": str(e)}), 500
