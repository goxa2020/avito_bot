from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from admin import adminMenu


def mainMenu(is_admin: bool) -> ReplyKeyboardMarkup:
    if is_admin:
        return adminMenu()
    else:
        main_Menu = ReplyKeyboardMarkup(resize_keyboard=True)
        btn = KeyboardButton('Ничего')
        main_Menu.add(btn)
        return main_Menu