from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


def mainMenu(user_id) -> ReplyKeyboardMarkup:
    is_admin = db.user_is_admin(user_id)
    main_Menu = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Добавить объявление')
    btn2 = KeyboardButton('Мои объявления')
    main_Menu.add(btn1).add(btn2)
    if is_admin:
        return adminMenu(main_Menu)
    return main_Menu


def adminMenu(keyboard: ReplyKeyboardMarkup()) -> ReplyKeyboardMarkup():
    btn1 = KeyboardButton('Управление админами')
    btn2 = KeyboardButton('Управление объявлениями')
    keyboard.add(btn1).add(btn2)
    return keyboard


def cancel_kb() -> ReplyKeyboardMarkup():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Отмена')
    return keyboard
