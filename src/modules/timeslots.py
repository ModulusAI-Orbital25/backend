Lesson = dict[str, str | int | list[int]]
Timeslot = tuple[int, int, int]


def convert_day(dayName: str) -> int:
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return DAYS.index(dayName)


def convert_time(timeValue: str) -> int:
    hour = timeValue[:2]
    return int(hour) - 8

# modules/timeslots.py

def lesson_to_timeslots(lesson):
    # extract raw fields
    dateStr  = lesson.get("day", "")
    startStr = lesson.get("startTime", "")
    endStr   = lesson.get("endTime", "")
    raw_weeks = lesson.get("weeks", [])

    # validate the basics
    assert isinstance(dateStr, str),    f"Bad day: {dateStr!r}"
    assert isinstance(startStr, str),   f"Bad startTime: {startStr!r}"
    assert isinstance(endStr, str),     f"Bad endTime: {endStr!r}"

    # normalize weeks into a list
    if isinstance(raw_weeks, list):
        weeks = raw_weeks
    elif isinstance(raw_weeks, int):
        weeks = [raw_weeks]
    else:
        # whatever unexpected type—treat as no weeks
        weeks = []

    # now you’re safe to convert
    dateInt  = convert_day(dateStr)
    startInt = convert_time(startStr)
    endInt   = convert_time(endStr)

    # build your timeslots
    timeslots: list[Timeslot] = [
        (w, dateInt, h)
        for w in weeks
        for h in range(startInt, endInt)
    ]
    return timeslots
