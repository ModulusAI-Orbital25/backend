from flask import jsonify
from profile import bp  # type: ignore
from models import User


@bp.route("/profile/<int:user_id>")
def profile(user_id):
    user = User.query.get(user_id)

    return jsonify(user.serialize())
