from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from datatypes import User
from loader import session


def mainMenu(user_id) -> ReplyKeyboardMarkup:
    user: User = session.query(User).filter(User.user_id == str(user_id)).first()
    is_admin = user.is_admin if user else False
    btn1 = KeyboardButton(text='Добавить объявление')
    btn2 = KeyboardButton(text='Мои объявления')
    main_menu = ReplyKeyboardMarkup(keyboard=[[btn1], [btn2]], resize_keyboard=True)
    if is_admin:
        return adminMenu(main_menu)
    return main_menu


def adminMenu(keyboard: ReplyKeyboardMarkup) -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text='Управление админами')
    btn2 = KeyboardButton(text='Управление объявлениями')
    keyboard.keyboard.extend([[btn1], [btn2]])
    return keyboard


def cancel_kb() -> ReplyKeyboardMarkup:
    btn = KeyboardButton(text='Отмена')
    keyboard = ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def no_or_cancel_kb() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text='Нет')
    btn2 = KeyboardButton(text='Отмена')
    keyboard = ReplyKeyboardMarkup(keyboard=[[btn1, btn2]], resize_keyboard=True, one_time_keyboard=True)
    return keyboard
