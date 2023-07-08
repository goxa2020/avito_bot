from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils.markdown import text, pre

from datatypes import Ad, User
from loader import session


async def send_user_ads(message: types.Message):
    user = session.query(User).filter(User.user_id == message.from_user.id).first()
    user_ads = session.query(Ad).filter(Ad.owner == user)
    if user_ads.count() > 1:
        m_text = text('Ваши объявления:')
    elif user_ads.count() == 1:
        m_text = text('Ваше объявление:')
    else:
        m_text = text('У вас ещё нет объявлений')
        return await message.answer(m_text)

    max_len_name = len(max([ad.product_name for ad in user_ads], key=len))

    for ad in user_ads:
        publish = "Опубликовано" if ad.posted else "Не опубликовано"
        indent = max_len_name + (12 if ad.posted else 15) - len(ad.product_name) + 2
        m_text += pre(f'{ad.product_name}{publish.rjust(indent)}')

    inline_kb = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Просмотреть каждый подробнее', callback_data=f'showUsersAd_0_1')
    inline_kb.add(inline_btn)

    await message.answer(text(m_text, sep='\n'), reply_markup=inline_kb, parse_mode=ParseMode.MARKDOWN_V2)
