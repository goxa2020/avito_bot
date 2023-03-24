from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import chanel_name
from loader import db, bot
from admin import show_ad
from aiogram import types
import logging


async def publish_ad(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    ad_index = int(callback_query.data.split("_")[1])

    confirm_publish_ad_keyboard = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton(f'Подтвердить', callback_data=f'confirmPublishAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton(f'Отмена', callback_data=f'cancelPublishAd')
    confirm_publish_ad_keyboard.add(inline_btn1).add(inline_btn2)

    await bot.send_message(callback_query.from_user.id, 'Точно опубликовать это объявление на канал',
                           reply_markup=confirm_publish_ad_keyboard)


async def confirm_publish_ad(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    ad_index = int(callback_query.data.split("_")[1])
    ads = db.get_not_posted_ads()
    ad = ads[ad_index]

    write_to_seller = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Написать продавцу', url=f'https://t.me/{ad[1][1::]}')
    write_to_seller.add(inline_btn)

    text = f'Товар: {ad[2]} \n' \
           f'Количество: {ad[3]} \n' \
           f'Цена за штуку: {ad[4]} \n' \
           f'Описание: {ad[7]} \n' \
           f'Город: {ad[5]}'

    try:

        if ad[8]:

            message = await bot.send_photo(chat_id=chanel_name, photo=ad[8], caption=text, reply_markup=write_to_seller)

        else:

            message = await bot.send_message(chanel_name, text, reply_markup=write_to_seller)

    except Exception as e:

        await bot.edit_message_text('Что-то не получилось',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id)

        await show_ad(callback_query.from_user.id, ad_index - 1)

        logging.warning(e)

    else:
        message_id = message.message_id

        db.update_ad_post_id(ad[0], message_id)

        db.update_ad_status(ad[0])

        await bot.edit_message_text(f'Это объявление успешно опубликованно',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=None)

        await show_ad(callback_query.from_user.id, ad_index - 1)

        try:

            await bot.send_message(ad[6], f'Администратор опубликовал вашу запись с товаром {ad[2]}')

        except Exception as e:

            logging.info(e)


async def cancel_publish_ad(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.edit_message_text(f'Объявление цело и невредимо',
                                callback_query.from_user.id,
                                callback_query.message.message_id)
