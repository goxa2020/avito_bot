import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from config import no_photo
from loader import db


async def show_ad_to_user(callback_query: CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split("_")[1])
    ads = db.get_user_ads(callback_query.from_user.id)

    ad_index = int(ad_index % len(ads))
    ad = ads[ad_index]

    text = f"Объявление {ad_index + 1} из {len(ads)}\n" \
           f"Название товара: {ad[2]}\n" \
           f"Количество: {ad[3]}\n" \
           f"Цена: {ad[4]}\n" \
           f"Город: {ad[5]}\n" \
           f"Описание: {ad[7]}\n" \
           f"Опубликовано : {ad[10]}"

    inline_kb = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton('Удалить', callback_data=f'авап')

    if len(ads) > 1:
        inline_btn3 = InlineKeyboardButton('Предыдущее объявление', callback_data=f'апвпф')
        inline_btn4 = InlineKeyboardButton('Следующее объявление', callback_data=f'вв')
        inline_kb.row(inline_btn3, inline_btn4)

    inline_kb.row(inline_btn1)

    if ad[10]:
        inline_btn2 = InlineKeyboardButton('Перейти', url=f'https://t.me/ttttttttesst/{ad[9]}')
        inline_kb.insert(inline_btn2)

    try:
        if ad[8]:
            photo = InputMediaPhoto(ad[8], caption=text)

            return await callback_query.message.edit_media(reply_markup=inline_kb,
                                                           media=photo)

        photo = InputMediaPhoto(no_photo, caption=text)

        return await callback_query.message.edit_media(reply_markup=inline_kb,
                                                       media=photo)
    except Exception as e:
        logging.error(e)
# TODO: ДОДЕЛАЙ ФУНКЦИЮ
