from flask import request, jsonify, url_for
from models import db
from models import Academics, Module
from models.timetable import Timetable
from modules import bp
from flask_login import current_user, login_required

@bp.route("/modules/savePlan", methods=["POST"])
@login_required
def save_timetable():
    data = request.get_json()
    semesters = data.get("semesters", [])
    if not semesters:
        return jsonify({"error": "Invalid input"}), 400

    timetable = Timetable.query.filter_by(user_id=current_user.id).first()
    if not timetable:
        timetable = Timetable(user_id=current_user.id)
        db.session.add(timetable)

    all_completed = set()

    for sem in semesters:
        idx = sem["semester"]
        mods = [m.strip() for m in sem["modules"] if m.strip()]
        valid_mods = Module.query.filter(Module.code.in_(mods)).all()

        if len(valid_mods) != len(mods):
            return jsonify({"error": f"Invalid module in semester {idx}"}), 400

        setattr(timetable, f"sem{idx}", ",".join(mods))
        setattr(timetable, f"com{idx}", sem["completed"])

        if sem["completed"]:
            all_completed.update(mods)

    db.session.commit()

    user = Academics.query.filter_by(user_id=current_user.id).first()
    if user:
        user.completedModules = ",".join(sorted(all_completed))
        db.session.commit()

    return jsonify({"status": "saved"})
