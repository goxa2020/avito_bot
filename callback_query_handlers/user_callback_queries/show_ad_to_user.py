import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from config import chanel_name, no_photo_id
from loader import db, bot
from markups import mainMenu


async def show_ad_to_user(user_id, ad_index, send_message, message_id=None):
    ads = db.get_user_ads(user_id)
    if len(ads) == 0:
        m_text = 'У вас нет объявлений'
        return await bot.send_message(user_id, m_text, reply_markup=mainMenu(user_id))
    ad_index = int(ad_index % len(ads))
    ad = ads[ad_index]

    text = f"Объявление {ad_index + 1} из {len(ads)}\n" \
           f"Название товара: {ad[2]}\n" \
           f"Количество: {ad[3]}\n" \
           f"Цена: {ad[4]}\n" \
           f"Город: {ad[5]}\n" \
           f"Описание: {ad[7]}\n" \
           f"Опубликовано : {'Да' if ad[10] else 'Нет'}"

    inline_kb = InlineKeyboardMarkup()

    if len(ads) > 1:
        inline_btn1 = InlineKeyboardButton('Предыдущее объявление', callback_data=f'showUsersAd_{ad_index - 1}_0')
        inline_btn2 = InlineKeyboardButton('Следующее объявление', callback_data=f'showUsersAd_{ad_index + 1}_0')
        inline_kb.row(inline_btn1, inline_btn2)

    inline_btn3 = InlineKeyboardButton('Удалить', callback_data=f'deleteUsersAd_{ad_index}')
    inline_kb.row(inline_btn3)

    inline_btn4 = InlineKeyboardButton('Закрепить на канале на месяц', callback_data=f'pinAd_{ad_index}')
    inline_kb.row(inline_btn4)
    # TODO: сделать закрепление за денюшки))
    if ad[10]:
        inline_btn5 = InlineKeyboardButton('Перейти', url=f'https://t.me/{chanel_name[1::]}/{ad[9]}')
        inline_kb.insert(inline_btn5)

    if send_message:
        try:

            if ad[8]:
                return await bot.send_photo(user_id, photo=ad[8], caption=text, reply_markup=inline_kb)

        except Exception as e:
            logging.error(e)

        try:

            return await bot.send_photo(user_id, photo=no_photo_id, caption=text, reply_markup=inline_kb)

        except Exception as e:
            logging.error(e)
            return

    try:

        if ad[8]:
            media = InputMediaPhoto(ad[8], caption=text)
            return await bot.edit_message_media(chat_id=user_id, media=media, message_id=message_id, reply_markup=inline_kb)

    except Exception as e:
        logging.error(e)

    try:

        media = InputMediaPhoto(no_photo_id, caption=text)
        return await bot.edit_message_media(chat_id=user_id, media=media, message_id=message_id, reply_markup=inline_kb)

    except Exception as e:
        logging.error(e)
