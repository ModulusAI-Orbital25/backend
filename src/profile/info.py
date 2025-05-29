from profile import bp


@bp.route("/profile/<int:user_id>")
def profile(user_id):
    return f"User ID: {user_id}"
