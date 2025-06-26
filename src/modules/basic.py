import requests

from app import db
from models import Module
from typing import Any
from collections import defaultdict
from flask import request

from modules import bp
from modules.timeslots import lesson_to_timeslots

NUSMODS_API = "https://api.nusmods.com/v2"
ACAD_YEAR = "2024-2025"

Lesson = dict[str, str | int | list[int]]
Timetable = list[Lesson]
Timeslot = tuple[int, int, int]


def get_url(path: str) -> str:
    return f"{NUSMODS_API}/{ACAD_YEAR}" + path


def load_basic_information():
    response = requests.get(get_url("/moduleInfo.json"))

    if response.status_code != 200:
        return

    data: list[dict[str, Any]] = response.json()

    for moduleInfo in data:
        module = Module(
            code=moduleInfo["moduleCode"],
            title=moduleInfo["title"],
            description=moduleInfo["description"],
            credit=float(moduleInfo["moduleCredit"]),
        )

        db.session.add(module)

    db.session.commit()
    print("Loaded basic module information")


def load_timetable(moduleCode: str) -> dict[str, Timetable]:
    response = requests.get(get_url(f"/modules/{moduleCode}.json"))

    if response.status_code != 200:
        return {}

    data = response.json()
    semesterData = data["semesterData"]
    timetable: Timetable = semesterData[0]["timetable"]

    return parse_timetable(moduleCode, timetable)


def parse_timetable(moduleCode: str, timetable: Timetable):
    # Split by lessonType
    lesson_type_groups: dict[str, Timetable] = defaultdict(list)
    for lesson in timetable:
        assert isinstance(lesson["lessonType"], str)
        lesson_type_groups[lesson["lessonType"]].append(lesson)

    # Split by lessonType/classNo
    parsed_timetable: dict[str, Timetable] = defaultdict(list)
    for lessonType, group in lesson_type_groups.items():
        for lesson in group:
            assert isinstance(lesson["classNo"], str)
            parsed_timetable[f"{moduleCode}/{lessonType}/{lesson['classNo']}"].append(
                lesson
            )

    return parsed_timetable


@bp.route("/modules/timeslots")
def get_timeslots_list():
    modules: list[str] = request.args.getlist("module")
    timetables = [load_timetable(module) for module in modules]

    total_timetable: dict[str, Timetable] = dict()
    for tt in timetables:
        total_timetable |= tt

    total_timeslots: dict[str, list[Timeslot]] = dict()
    for code, tt in total_timetable.items():
        slots = [lesson_to_timeslots(lesson) for lesson in tt]
        combined_timeslots = [e for slot in slots for e in slot]
        total_timeslots[code] = combined_timeslots

    return total_timeslots
