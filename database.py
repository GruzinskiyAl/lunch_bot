import json
from typing import TypedDict, List


class DataBaseScheme(TypedDict):
    users: dict
    users_id_list: List[str]
    commands_in_progress: dict
    menu: List[List[str]]


def get_db_data() -> DataBaseScheme:
    with open('db.json', 'r') as db:
        data = json.load(db)
    return data


def update_db(insert_data):
    with open('db.json', 'r+') as db:
        json.dump(insert_data, db, indent=2)
