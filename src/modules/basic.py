from app import db
from models import Module
import requests

NUSMODS_API = "https://api.nusmods.com/v2"
ACAD_YEAR = "2024-2025"


def load_basic_information():
    response = requests.get(f"{NUSMODS_API}/{ACAD_YEAR}/moduleList.json")

    if response.status_code != 200:
        return

    data: list[dict[str, str | list[int]]] = response.json()

    for moduleInfo in data:
        module = Module(
            code=moduleInfo["moduleCode"],
            title=moduleInfo["title"],
        )

        db.session.add(module)

    db.session.commit()
    print("Loaded basic module information")
