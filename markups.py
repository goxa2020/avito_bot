from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from admin import adminMenu


def mainMenu(is_admin: bool) -> ReplyKeyboardMarkup:
    main_Menu = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Добавить объявление')
    main_Menu.add(btn)
    if is_admin:
        return adminMenu(main_Menu)
    return main_Menu
