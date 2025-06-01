from flask import request, jsonify, url_for
from models import Academics
from flask_login import current_user, login_required
from app import db
from profile import bp  
import traceback


@bp.route("/profile/userProfile", methods=["POST"])
@login_required 
def loadAcademics():
    try:
        user_id = current_user.id  
        data = request.get_json()

        academic = Academics.query.filter_by(user_id=user_id).first()

        if academic is None:
            academic = Academics(
                user_id=user_id,
                primaryMajor=data.get("primaryMajor"),
                secondaryMajor=data.get("secondaryMajor"),
                minor1=data.get("minor1"),
                minor2=data.get("minor2"),
                completedModules=data.get("completedModules"),
                currentSemester=data.get("currentSemester"),
                internshipSem=data.get("internshipSem"),
            )
            db.session.add(academic)
        else:
            academic.primaryMajor = data.get("primaryMajor")
            academic.secondaryMajor = data.get("secondaryMajor")
            academic.minor1 = data.get("minor1")
            academic.minor2 = data.get("minor2")
            academic.completedModules = data.get("completedModules")
            academic.currentSemester = data.get("currentSemester")
            academic.internshipSem = data.get("internshipSem")

        db.session.commit()
        return jsonify({"redirect": url_for("index")})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500
