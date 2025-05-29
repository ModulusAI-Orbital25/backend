from flask import Blueprint

profile_page = Blueprint("profile page", __name__)


@profile_page.route("/profile/<int:user_id>")
def profile(user_id):
    return f"User ID: {user_id}"
