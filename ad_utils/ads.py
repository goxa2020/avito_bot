from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils.markdown import text, pre
from loader import db


async def send_user_ads(message: types.Message):
    user_ads = db.get_user_ads(message.from_user.id)

    if len(user_ads) > 1:
        m_text = text('Ваши объявления:')
    elif len(user_ads) == 1:
        m_text = text('Ваше объявление:')
    else:
        m_text = text('У вас ещё нет объявлений')
        return await message.answer(m_text)

    max_len_name = len(max([ad[2] for ad in user_ads], key=len))

    for ad in user_ads:
        publish = "Опубликовано" if ad[10] else "Не опубликовано"
        indent = max_len_name + (12 if ad[10] else 15) - len(ad[2]) + 2
        m_text += pre(f'{ad[2]}{publish.rjust(indent)}')

    inline_kb = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Просмотреть каждый подробнее', callback_data=f'showUsersAd_0_1')
    inline_kb.add(inline_btn)

    await message.answer(text(m_text, sep='\n'), reply_markup=inline_kb, parse_mode=ParseMode.MARKDOWN_V2)
