from ortools.sat.python import cp_model
from flask import request, jsonify
from collections import defaultdict

from modules import bp
from modules.basic import Timeslot, get_timeslots_list
from flask_login import current_user
from models.timetable import Timetable


@bp.route("/modules/optimizer", methods=["GET", "POST"])
def optimize():
    timetable: Timetable = Timetable.query.filter_by(user_id=current_user.id).first()

    if not timetable:
        return "Timetable not found", 404

    for i in range(1, 9):
        completed = getattr(timetable, f"com{i}")
        if not completed:
            modules_str = getattr(timetable, f"sem{i}")
            break
    else:
        return "All semesters completed", 400

    modules = [m.strip() for m in modules_str.split(",") if m.strip()]
    if not modules:
        return "No modules in current semester", 400

    model = cp_model.CpModel()

    timeslots = get_timeslots_list(modules)

    variables: dict[tuple[str, str], cp_model.IntVar] = dict()

    for lessonType, classList in timeslots.items():
        for classNumber in classList:
            variables[(lessonType, classNumber)] = model.new_bool_var(
                f"{lessonType}/{classNumber}"
            )

    for lessonType, classList in timeslots.items():
        _ = model.add_exactly_one(
            variables[(lessonType, classNumber)] for classNumber in classList
        )

    slots: dict[Timeslot, list[cp_model.IntVar]] = defaultdict(list)

    for lessonType, classList in timeslots.items():
        for classNumber, lst in classList.items():
            for slot in lst:
                slots[slot].append(variables[(lessonType, classNumber)])

    for slot, lst in slots.items():
        _ = model.add_at_most_one(lst)


    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen: list[dict] = []

        for (lessonType, classNumber), var in variables.items():
            if solver.value(var):
                module, ltype = lessonType.split("/", 1) 

                chosen.append(
                    {
                        "module": module,
                        "lessonType": ltype,
                        "classNumber": classNumber,
                        "timeslots": timeslots[lessonType][classNumber],
                    }
                )

        return jsonify(chosen), 200

    elif status == cp_model.INFEASIBLE:
        return "Infeasible", 409
    elif status == cp_model.MODEL_INVALID:
        return "Model invalid", 500
    else:
        return "Unknown error", 500

