from flask import jsonify
from app import db
from profile import bp # type: ignore
from models import User


@bp.route("/profile/<int:user_id>")
def profile(user_id):
    user = db.one_or_404(db.select(User).filter_by(id=user_id))

    return jsonify(user.serialize())
