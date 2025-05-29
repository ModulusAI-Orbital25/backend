from flask import request
from app import db
from profile import bp
from models import User


@bp.route("/profile/register", methods=["POST"])
def register():
    name = request.form.get("name")

    # Validate data
    # Try-catch for error

    new_user = User(name=name, display_name=name)

    db.session.add(new_user)
    db.session.commit()

    return "User created"
