from flask import jsonify
from flask_login import current_user, login_required
from models.timetable import Timetable
from models.module import Module
from modules import bp

from .degree import categories, id_courses, cd_courses

@bp.route("/modules/classify", methods=["GET"])
@login_required
def classify_modules():
    tt = Timetable.query.filter_by(user_id=current_user.id).first()
    if not tt:
        return jsonify({"error": "No timetable found for user"}), 404

    raw = [m for sem in tt.serialize()["semesters"] for m in sem["modules"]]
    seen = set()
    codes = []
    for c in raw:
        if c not in seen:
            seen.add(c)
            codes.append(c)

    modules = { code: Module.query.filter_by(code=code).first() for code in codes }

    courses_by_cat = [[] for _ in categories]
    used = set()

    GROUPS = {
        "Interdisciplinary & Cross-Disciplinary Education",
        "Computer Science Breadth and Depth",
        "Unrestricted Electives",
    }

    for idx, (cat, desc) in enumerate(categories):
        if desc in GROUPS:
            continue
        for code in codes:
            if code in used:
                continue
            mod = modules[code]
            if mod and cat.verify([mod]):
                courses_by_cat[idx].append(code)
                used.add(code)

    for idx, (cat, desc) in enumerate(categories):
        if desc == "Interdisciplinary & Cross-Disciplinary Education":
            for code in codes:
                if code in used:
                    continue
                if code in id_courses or code in cd_courses:
                    courses_by_cat[idx].append(code)
                    used.add(code)

    for idx, (cat, desc) in enumerate(categories):
        if desc == "Computer Science Breadth and Depth":
            for code in codes:
                if code in used:
                    continue
                mod = modules[code]
                if mod and any(mod.code.startswith(p) for p in ("CS", "IFS", "CP")):
                    courses_by_cat[idx].append(code)
                    used.add(code)

    for idx, (cat, desc) in enumerate(categories):
        if desc == "Unrestricted Electives":
            for code in codes:
                if code not in used:
                    courses_by_cat[idx].append(code)
                    used.add(code)

    return jsonify({ "courses": courses_by_cat })
