import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from config import chanel_name, no_photo_id
from datatypes import Ad, User
from loader import bot, session
from markups import mainMenu


async def show_ad_to_user(user_id, ad_index, send_message: bool, message_id=None):
    user = session.query(User).filter(User.user_id == user_id).first()
    ads = session.query(Ad).filter(Ad.owner == user)
    if ads.count() == 0:
        m_text = 'У вас нет объявлений'
        return await bot.send_message(user_id, m_text, reply_markup=mainMenu(user_id))
    ad_index = int(ad_index % ads.count())
    ad = ads[ad_index]

    text = f"Объявление {ad_index + 1} из {ads.count()}\n" \
           f"Название товара: {ad.product_name}\n" \
           f"Количество: {ad.amount}\n" \
           f"Цена: {ad.price}\n" \
           f"Город: {ad.town}\n" \
           f"Описание: {ad.description}\n" \
           f"Опубликовано: {'Да' if ad.posted else 'Нет'}\n" \
           f"{'Закреплено: Да' if ad.is_pinned else ''}"

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    if ads.count() > 1:
        inline_btn1 = InlineKeyboardButton(text='Предыдущее объявление', callback_data=f'showUsersAd_{ad_index - 1}_0')
        inline_btn2 = InlineKeyboardButton(text='Следующее объявление', callback_data=f'showUsersAd_{ad_index + 1}_0')
        inline_kb.inline_keyboard.append([inline_btn1, inline_btn2])

    inline_btn3 = InlineKeyboardButton(text='Удалить', callback_data=f'deleteUsersAd_{ad_index}')
    inline_kb.inline_keyboard.append([inline_btn3])

    if ad.posted:
        inline_btn4 = InlineKeyboardButton(text='Перейти', url=f'https://t.me/{chanel_name[1::]}/{ad.post_id}')
        inline_kb.inline_keyboard[1].append(inline_btn4)
        if not ad.is_pinned:
            inline_btn5 = InlineKeyboardButton(text='Закрепить на канале на месяц', callback_data=f'pinAd_{ad_index}')
            inline_kb.inline_keyboard.append([inline_btn5])

    if send_message:
        if ad.picture_id:
            try:
                return await bot.send_photo(user_id, photo=ad.picture_id, caption=text, reply_markup=inline_kb)

            except Exception as e:
                return logging.error(e)

        try:

            return await bot.send_photo(user_id, photo=no_photo_id, caption=text, reply_markup=inline_kb)

        except Exception as e:
            return logging.error(e)

    if ad.picture_id:
        try:
            media = InputMediaPhoto(media=ad.picture_id, caption=text)
            return await bot.edit_message_media(chat_id=user_id, media=media, message_id=message_id, reply_markup=inline_kb)

        except Exception as e:
            return logging.error(e)

    try:

        media = InputMediaPhoto(media=no_photo_id, caption=text)
        return await bot.edit_message_media(chat_id=user_id, media=media, message_id=message_id, reply_markup=inline_kb)

    except Exception as e:
        logging.error(e)
