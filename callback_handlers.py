from loader import dp, db, bot
from aiogram import types
from markups import *
from admin import *
from config import no_photo
import logging


@dp.callback_query_handler(text_contains="callDelAdm_")
async def callback(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    del_id = callback_query.data.split("_")[1]
    admin_name = db.get_admin_name(del_id)

    await bot.edit_message_text(f'Точно удалить {admin_name}', callback_query.from_user.id,
                                callback_query.message.message_id, reply_markup=accept_del_admin_kb(del_id))


@dp.callback_query_handler(text_contains="acceptCallDelAdm_")
async def callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    del_id = callback_query.data.split("_")[1]
    try:
        if db.user_is_admin(del_id):
            db.del_admin(del_id)
    except Exception:
        await bot.edit_message_text('Что-то не получилось', callback_query.from_user.id,
                                    callback_query.message.message_id)
        await bot.send_message(user_id, my_admins_text(user_id), reply_markup=my_admins_kb(user_id))
    else:
        await bot.edit_message_text(f'Человек успешно лишён админки \n{my_admins_text(user_id)}',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=my_admins_kb(user_id))
        try:
            await bot.send_message(del_id, 'Вас лишили прав администратора')
        except Exception as e:
            logging.info(e)


@dp.callback_query_handler(text_contains="cancelCallDelAdm_")
async def callback(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    user_id = callback_query.from_user.id

    await bot.edit_message_text(f'Действие отменено \n{my_admins_text(user_id)}',
                                callback_query.from_user.id,
                                callback_query.message.message_id,
                                reply_markup=my_admins_kb(user_id))


@dp.callback_query_handler(text_contains="showAd_")
async def callback(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    ad_index = int(callback_query.data.split("_")[1])
    ads = db.get_ads()

    ad_index = int(ad_index % len(ads))
    ad = ads[ad_index]

    text = f"Объявление {ad_index+1} из {len(ads)}\n" \
           f"Имя: {ad[0]}\n" \
           f"Название товара: {ad[1]}\n" \
           f"Количество: {ad[2]}\n" \
           f"Цена: {ad[3]}\n" \
           f"Город: {ad[4]}\n" \
           f"Описание: {ad[7]}\n"

    inline_kb = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton('Предыдущее объявление', callback_data=f'showAd_{ad_index-1}')
    inline_btn2 = InlineKeyboardButton('Следующее объявление', callback_data=f'showAd_{ad_index+1}')
    inline_btn3 = InlineKeyboardButton('Отклонить', callback_data=f'deleteAd_{ad_index}')
    inline_btn4 = InlineKeyboardButton('Опубликовать', callback_data=f'publishAd_{ad_index}')
    inline_kb.row(inline_btn1, inline_btn2).row(inline_btn3, inline_btn4)

    if ad[5]:

        photo = types.InputMediaPhoto(ad[5], caption = text)

        return await bot.edit_message_media(chat_id = callback_query.from_user.id,
                                            message_id = callback_query.message.message_id,
                                            reply_markup = inline_kb,
                                            media = photo)
    else:

        photo = types.InputMediaPhoto(no_photo, caption = text)

        return await bot.edit_message_media(chat_id = callback_query.from_user.id,
                                            message_id = callback_query.message.message_id,
                                            reply_markup = inline_kb,
                                            media = photo)


@dp.callback_query_handler(text_contains="deleteAd_")
async def callback(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    ad_index = int(callback_query.data.split("_")[1])

    accept_del_ad_keyboard = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton(f'Подтвердить', callback_data=f'acceptDelAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton(f'Отмена', callback_data=f'cancelDelAd')
    accept_del_ad_keyboard.add(inline_btn1).add(inline_btn2)

    await bot.send_message(callback_query.from_user.id, 'Точно удалить это объявление', reply_markup=accept_del_ad_keyboard)


@dp.callback_query_handler(text_contains="acceptDelAd_")
async def callback(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    ad_index = int(callback_query.data.split("_")[1])

    ads = db.get_ads()

    ad = ads[ad_index]

    ad_id = ad[8]

    try:

        db.del_ad(ad_id)
        print("КУКУ")
    except Exception:

        await bot.edit_message_text('Что-то не получилось',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id)

        await show_ad(callback_query.from_user.id, ad_index-1)

    else:

        await bot.edit_message_text(f'Это объявление успешно отклонено',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=my_admins_kb(callback_query.from_user.id))

        await show_ad(callback_query.from_user.id, ad_index-1)

        try:

            await bot.send_message(ad[6], f'Администратор отклонил вашу запись с товаром {ad[1]}')

        except Exception as e:

            logging.info(e)


@dp.callback_query_handler(text_contains="cancelDelAd")
async def callback(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    await bot.edit_message_text(f'Объявление цело и невредимо',
                                callback_query.from_user.id,
                                callback_query.message.message_id)


@dp.callback_query_handler(text_contains="publishAd_")
async def callback(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    ad_index = int(callback_query.data.split("_")[1])
    ads = db.get_ads()

    ad = ads[ad_index]