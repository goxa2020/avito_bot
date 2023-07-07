from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from datatypes import User
from loader import session


def mainMenu(user_id) -> ReplyKeyboardMarkup:
    user = session.query(User).filter(User.user_id == str(user_id)).first()
    is_admin = user.is_admin if user else False
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
