from flask import request, jsonify, url_for
from models import Academics, Module, User
from flask_login import current_user, login_required
from models import db
from profile import bp
import traceback


@bp.route("/profile/userProfile", methods=["POST"])
@login_required
def loadAcademics():
    try:
        user_id = current_user.id
        data = request.get_json()

        user = User.query.filter_by(id=user_id).first()

        if user.academics is None:
            user.academics = Academics(
                user_id=user_id,
                primaryMajor=data.get("primaryMajor"),
                secondaryMajor=data.get("secondaryMajor"),
                minor1=data.get("minor1"),
                minor2=data.get("minor2"),
                currentSemester=data.get("currentSemester"),
                internshipSem=data.get("internshipSem"),
            )
        else:
            user.academics.primaryMajor = data.get("primaryMajor")
            user.academics.secondaryMajor = data.get("secondaryMajor")
            user.academics.minor1 = data.get("minor1")
            user.academics.minor2 = data.get("minor2")
            user.academics.currentSemester = data.get("currentSemester")
            user.academics.internshipSem = data.get("internshipSem")

        # TODO: remove completedModules from the model

        # Parse the module list and add the modules to the user's list

        db.session.commit()
        return jsonify({"redirect": url_for("index")})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500
