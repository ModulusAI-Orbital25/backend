from flask import jsonify, redirect, url_for
from flask_login import login_required, current_user
from profile import bp  # type: ignore
from models import User


@bp.route("/profile/<int:user_id>")
def profile(user_id):
    user = User.query.get(user_id)

    return jsonify(user.serialize())


@bp.route("/profile")
@login_required
def current_profile():
    return redirect(url_for("profile_page.profile", user_id=current_user.id))
