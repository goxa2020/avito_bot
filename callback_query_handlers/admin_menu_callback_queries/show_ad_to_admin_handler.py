from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import no_photo_id
from datatypes import Ad
from loader import bot, session


async def show_ad_to_admin(callback_query: types.CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split("_")[1])
    ads = session.query(Ad).filter(Ad.posted == False)

    ad_index = int(ad_index % ads.count())
    ad: Ad = ads[ad_index]

    text = f"Объявление {ad_index + 1} из {ads.count()}\n" \
           f"Имя: {ad.owner.user_first_name}\n" \
           f"Название товара: {ad.product_name}\n" \
           f"Количество: {ad.amount}\n" \
           f"Цена: {ad.price}\n" \
           f"Город: {ad.town}\n" \
           f"Описание: {ad.description}\n"

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])
    inline_btn1 = InlineKeyboardButton(text='Отклонить', callback_data=f'deleteAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton(text='Опубликовать', callback_data=f'publishAd_{ad_index}')

    if ads.count() > 1:
        inline_btn3 = InlineKeyboardButton(text='Предыдущее объявление', callback_data=f'showAd_{ad_index - 1}')
        inline_btn4 = InlineKeyboardButton(text='Следующее объявление', callback_data=f'showAd_{ad_index + 1}')
        inline_kb.inline_keyboard.append([inline_btn3, inline_btn4])

    inline_kb.inline_keyboard.append([inline_btn1, inline_btn2])

    if ad.picture_id:
        photo = types.InputMediaPhoto(media=ad.picture_id, caption=text)

        return await bot.edit_message_media(chat_id=callback_query.from_user.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=inline_kb,
                                            media=photo)

    photo = types.InputMediaPhoto(media=no_photo_id, caption=text)

    return await bot.edit_message_media(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb,
                                        media=photo)
