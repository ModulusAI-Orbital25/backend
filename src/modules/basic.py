from app import db
from models import Module
import requests
from typing import Any
from collections import defaultdict

NUSMODS_API = "https://api.nusmods.com/v2"
ACAD_YEAR = "2024-2025"

Lesson = dict[str, str | int | list[int]]
Timetable = list[Lesson]


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


def load_timetable(moduleCode: str):
    response = requests.get(get_url(f"/modules/{moduleCode}.json"))

    if response.status_code != 200:
        return

    data = response.json()
    timetable: Timetable = data["semesterData"]["timetable"]

    return parse_timetable(timetable)


def parse_timetable(timetable: Timetable):
    # Split by lessonType
    lesson_type_groups: dict[str, Timetable] = defaultdict(list)
    for lesson in timetable:
        assert isinstance(lesson["lessonType"], str)
        lesson_type_groups[lesson["lessonType"]].append(lesson)

    # Split by lessonType/classNo
    parsed_timetable: dict[str, Timetable] = dict()
    for lessonType, group in lesson_type_groups.items():
        for lesson in group:
            assert isinstance(lesson["classNo"], str)
            parsed_timetable[f"{lessonType}/{lesson['classNo']}"].append(lesson)

    return parsed_timetable
