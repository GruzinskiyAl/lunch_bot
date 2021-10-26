from datetime import date

import pymongo

from db import menu_collection
from settings import MENU_DELIMITER, DATE_FORMAT
from exceptions import NotCorrectMessage, DoesNotExist
from typing import NamedTuple, List


class Menu(NamedTuple):
    menu: List[List[str]]
    date: str


class MenuManager:
    @staticmethod
    def get_current() -> str:
        if menu_obj := menu_collection.find_one(sort=[('_id', pymongo.DESCENDING)]):
            menu_list = ['\n'.join(i) for i in menu_obj['menu']]
            menu_with_delimiter = f'\n{MENU_DELIMITER}\n'.join(menu_list)
            return menu_with_delimiter
        raise DoesNotExist('Cant find any menu')

    @staticmethod
    def update_current(menu_row: str):
        try:
            menu = [i.split('\n') for i in menu_row.split(f'\n{MENU_DELIMITER}\n')]
            menu_collection.insert_one({'menu': menu, 'date': date.today().strftime(DATE_FORMAT)})
        except Exception:
            raise NotCorrectMessage('Not valid menu format')
