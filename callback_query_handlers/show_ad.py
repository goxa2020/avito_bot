from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from loader import db, bot
from config import no_photo


async def show_ad(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    ad_index = int(callback_query.data.split("_")[1])
    ads = db.get_not_posted_ads()

    ad_index = int(ad_index % len(ads))
    ad = ads[ad_index]

    text = f"Объявление {ad_index + 1} из {len(ads)}\n" \
           f"Имя: {ad[1]}\n" \
           f"Название товара: {ad[2]}\n" \
           f"Количество: {ad[3]}\n" \
           f"Цена: {ad[4]}\n" \
           f"Город: {ad[5]}\n" \
           f"Описание: {ad[7]}\n"

    inline_kb = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton('Отклонить', callback_data=f'deleteAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton('Опубликовать', callback_data=f'publishAd_{ad_index}')

    if len(ads) > 1:
        inline_btn3 = InlineKeyboardButton('Предыдущее объявление', callback_data=f'showAd_{ad_index - 1}')
        inline_btn4 = InlineKeyboardButton('Следующее объявление', callback_data=f'showAd_{ad_index + 1}')
        inline_kb.row(inline_btn3, inline_btn4)

    inline_kb.row(inline_btn1, inline_btn2)

    if ad[8]:
        photo = types.InputMediaPhoto(ad[8], caption=text)

        return await bot.edit_message_media(chat_id=callback_query.from_user.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=inline_kb,
                                            media=photo)

    photo = types.InputMediaPhoto(no_photo, caption=text)

    return await bot.edit_message_media(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb,
                                        media=photo)
