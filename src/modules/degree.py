from models.module import Module
from modules import bp


class Category:
    def __init__(self, check_function):
        self.check_function = check_function

    def verify(self, courses: list[Module]) -> bool:
        return self.check_function(courses)

    @staticmethod
    def from_courses(courses: list[str], credit: int = 4):
        def chk(m: list[Module]):
            return len(m) == 1 and m[0].code in courses and m[0].credit == credit

        return Category(chk)

    @staticmethod
    def from_prefix(prefix: str, credit: int = 4):
        def chk(m: list[Module]):
            return (
                len(m) == 1 and m[0].code.startswith(prefix) and m[0].credit == credit
            )

        return Category(chk)


# For CS degree
id_courses = [
    "CDE2501",
    "DTK1234",
    "EG1311",
    "IE2141",
    "PF1101A",
    "IS1128",
    "IS2218",
    "IS2238",
    "HSH1000",
    "HSS1000",
    "HSA1000",
    "HSI1000",
    "HSI2001",
    "HSI2002",
    "HSI2003",
    "HSI2004",
    "HSI2005",
    "HSI2007",
    "HSI2008",
    "HSI2009",
    "HSI2010",
    "HSI2011",
    "HSI2013",
    "HSI2014",
]

cd_courses = [
    "ACC1701X",
    "DAO2703",
    "MNO1706X",
    "SC1101E",
    "EL1101E",
    "PE2101P",
    "GE2103",
    "XD3103",
    "GE3253",
    "GE3255",
    "GE3256",
    "SPH2002",
    "SC2226",
    "NUR1113A",
    "CDE2300",
    "CDE2310",
    "EG2201A",
    "EG2310",
]


def idcd_check(courses: list[Module]):
    id_learnt = [m for m in courses if m.code in id_courses]
    cd_learnt = [m for m in courses if m.code in cd_courses]
    total_credit = sum(m.credit for m in id_learnt) + sum(m.credit for m in cd_learnt)
    return total_credit == 12 and len(cd_learnt) <= 1


focus_areas = [
    ["CS3230", "CS3231", "CS3236", "CS4231", "CS4232", "CS4234"],
    [
        "CS2109S",
        "CS3243",
        "CS3244",
        "CS3263",
        "CS3264",
        "CS4243",
        "CS4244",
        "CS4246",
        "CS4248",
    ],
    ["CS3241", "CS3242", "CS3247", "CS4247", "CS4350"],
    ["CS2107", "CS3235", "CS4236", "CS4230", "CS4238", "CS4239"],
    ["CS2102", "CS3223", "CS4221", "CS4224", "CS4225"],
    ["CS2108", "CS3245", "CS4242", "CS4248", "CS4347"],
    ["CS2105", "CS3103", "CS4222", "CS4226", "CS4231"],
    ["CS3210", "CS3211", "CS4231", "CS4223"],
    ["CS2104", "CS3211", "CS4212", "CS4215"],
    ["CS2103", "CS2103T", "CS3213", "CS3219", "CS4211", "CS4218", "CS4239"],
]


def breadth_and_depth_check(courses: list[Module]):
    if sum(m.credit for m in courses) != 32:
        return False

    def check_prefix_code(course):
        return (
            course.code.startswith("CS")
            or course.code.startswith("IFS")
            or course.code.startswith("CP")
        )

    if any(not check_prefix_code(m) for m in courses):
        return False

    if "CP4101" not in [m.code for m in courses]:
        return False

    def get_level(course):
        for i in range(len(course.code)):
            if "0" <= course.code[i] and course.code[i] <= "9":
                return int(course.code[i])
        return 0

    if sum(m.credit for m in courses if get_level(m) >= 4) < 12:
        return False

    focus_check = False
    for area in focus_areas:
        focus_courses = [m for m in courses if m.code in area]
        valid = True
        if len(focus_courses) < 3:
            valid = False
        elif max(get_level(m) for m in focus_courses) < 4:
            valid = False
        if valid:
            focus_check = True

    if not focus_check:
        return False

    return True


def electives_check(courses: list[Module]):
    return sum([m.credit for m in courses]) >= 40


categories = [
    Category.from_courses(["CS1101S"]),
    Category.from_courses(["ES2660"]),
    Category.from_prefix("GEC"),
    Category.from_courses(["GEA1000", "BT1101", "ST1131", "DSA1101"]),
    Category.from_prefix("GES"),
    Category.from_prefix("GEN"),
    Category.from_courses(["IS1108"]),
    Category(idcd_check),
    Category.from_courses(["CS1231S"]),
    Category.from_courses(["CS2030S"]),
    Category.from_courses(["CS2040S"]),
    Category.from_courses(["CS2100"]),
    Category.from_courses(["CS2101"]),
    Category.from_courses(["CS2103T"]),
    Category.from_courses(["CS2106"]),
    Category.from_courses(["CS2109S"]),
    Category.from_courses(["CS3230"]),
    Category(breadth_and_depth_check),
    Category.from_courses(["MA1521"]),
    Category.from_courses(["MA1522"]),
    Category.from_courses(["ST2334"]),
    Category(electives_check),
]

sample_courses_code = [
    ["CS1101S"],
    ["ES2660"],
    ["GEC1007"],
    ["GEA1000"],
    ["GESS1020"],
    ["GEN2004"],
    ["IS1108"],
    ["HSI1000", "EL1101E", "IS1128"],
    ["CS1231S"],
    ["CS2030S"],
    ["CS2040S"],
    ["CS2100"],
    ["CS2101"],
    ["CS2103T"],
    ["CS2106"],
    ["CS2109S"],
    ["CS3230"],
    ["CS2104", "CS3211", "CS4215", "CS4212", "CS3234", "CP4101"],
    ["MA1521"],
    ["MA1522"],
    ["ST2334"],
    [
        "CS5218",
        "CS2105",
        "MA2101",
        "MA2214",
        "MA2108",
        "CP3108B",
        "CS2107",
        "CS2108",
        "CS3210",
        "CS3233",
    ],
]


@bp.route("/modules/requirements")
def degree_requirements():
    courses_code = sample_courses_code

    courses = [
        [Module.query.filter_by(code=code).first() for code in code_list]
        for code_list in courses_code
    ]

    message = ""

    for i in range(len(categories)):
        message += f"DEBUG: Category #{i + 1}, courses_code = f{courses_code[i]}, courses = {courses[i]}\n"
        message += f"verdict = {categories[i].verify(courses[i])}\n"

    return message
