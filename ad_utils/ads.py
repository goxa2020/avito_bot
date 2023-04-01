from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from loader import db


async def send_user_ads(message: types.Message):
    user_ads = db.get_user_ads(message.from_user.id)
    if len(user_ads) > 1:
        text = 'Ваши объявления:<code>\n'
    elif len(user_ads) == 1:
        text = 'Ваше объявление:<code>\n'
    else:
        text = 'У вас ещё нет объявлений'
        return await message.answer(text)

    max_len_name = len(max([ad[2] for ad in user_ads], key=len))

    for ad in user_ads:
        publish = "Опубликовано" if ad[10] else "Не опубликовано"
        indent = max_len_name + (12 if ad[10] else 15) - len(ad[2]) + 2
        text += f'{ad[2]}{publish.rjust(indent)}\n'

    text += '</code>'

    print(text)

    inline_kb = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Просмотреть каждый подробнее', callback_data=f'showUsersAd_0')
    inline_kb.add(inline_btn)

    await message.answer(text, reply_markup=inline_kb, parse_mode=ParseMode.HTML)
