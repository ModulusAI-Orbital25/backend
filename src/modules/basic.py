from app import db
from models import Module
import requests
from typing import Any

NUSMODS_API = "https://api.nusmods.com/v2"
ACAD_YEAR = "2024-2025"


def load_basic_information():
    response = requests.get(f"{NUSMODS_API}/{ACAD_YEAR}/moduleInfo.json")

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
