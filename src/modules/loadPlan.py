from flask import request, jsonify, url_for
from models import db
from models import Academics, Module
from models.timetable import Timetable
from modules import bp
from flask_login import current_user, login_required


@bp.route("/modules/loadPlan", methods=["GET"])
@login_required
def load_plan():
    user_id = current_user.id
    timetable = Timetable.query.filter_by(user_id=user_id).first()

    if not timetable:
        return jsonify({"semesters": []})

    def parse_field(field):
        return field.split(",") if field else []

    semesters = []
    for i in range(1, 9):
        modules = parse_field(getattr(timetable, f"sem{i}"))
        semesters.append({
            "semester": i,
            "modules": modules,
            "completed": getattr(timetable, f"com{i}")
        })

    return jsonify({"semesters": semesters})
