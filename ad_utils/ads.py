from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


async def send_user_ads(message: types.Message):
    print(message)
    user_ads = db.get_user_ads(message.from_user.id)
    if len(user_ads) > 1:
        text = 'Ваши объявления:\n'
    elif len(user_ads) == 1:
        text = 'Ваше объявление:\n'
    else:
        text = 'У вас ещё нет объявлений'

    for ad in user_ads:
        text += f'{ad[2]}   {"Опубликовано" if ad[10] else "Не опубликовано"}\n'

    inline_kb = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Просмотреть каждый подробнее', callback_data=f'show_ad_to_user')

    inline_kb.add(inline_btn)

    await message.answer(text, reply_markup=inline_kb)
    # TODO: ДОДЕЛАЙ БЛИН ФУНКЦИЮ
