from modules.basic import Lesson

Timeslot = tuple[int, int, int]


def convert_day(dayName: str) -> int:
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return DAYS.index(dayName)


def convert_time(timeValue: str) -> int:
    hour = timeValue[:2]
    return int(hour) - 8


def lesson_to_timeslots(lesson: Lesson):
    dateStr = lesson["day"]
    startStr = lesson["startTime"]
    endStr = lesson["endTime"]
    weeks = lesson["weeks"]

    assert isinstance(dateStr, str)
    assert isinstance(startStr, str)
    assert isinstance(endStr, str)
    assert isinstance(weeks, list)

    dateInt = convert_day(dateStr)
    startInt = convert_time(startStr)
    endInt = convert_time(endStr)

    timeslots: list[Timeslot] = [
        (w, dateInt, h) for w in weeks for h in range(startInt, endInt)
    ]
    return timeslots
