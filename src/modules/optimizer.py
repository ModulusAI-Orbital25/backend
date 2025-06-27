from ortools.sat.python import cp_model
from flask import request
from collections import defaultdict

from modules import bp
from modules.basic import Timeslot, get_timeslots_list


@bp.route("/modules/optimizer")
def optimize():
    modules: list[str] = request.args.getlist("module")

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

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        answer: list[str] = []
        for lessonType, classNumber in variables:
            if solver.value(variables[(lessonType, classNumber)]):
                answer.append(f"{lessonType}/{classNumber}")
        return answer
    elif status == cp_model.INFEASIBLE:
        return "Infeasible"
    elif status == cp_model.MODEL_INVALID:
        return "Model invalid"
    else:
        return "???"
