from profile import profile_bp


@profile_bp.route("/profile/<int:user_id>")
def profile(user_id):
    return f"User ID: {user_id}"
