from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from admin import my_admins_kb, show_ad
from datatypes import Ad
from loader import bot, session
import logging


async def delete_ad(callback_query: CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split("_")[1])

    confirm_del_ad_keyboard = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton(f'Подтвердить', callback_data=f'confirmDelAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton(f'Отмена', callback_data=f'cancelDelAd')
    confirm_del_ad_keyboard.add(inline_btn1).add(inline_btn2)

    await bot.send_message(callback_query.from_user.id, 'Точно удалить это объявление',
                           reply_markup=confirm_del_ad_keyboard)


async def confirm_delete_ad(callback_query: CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split("_")[1])

    ads = session.query(Ad).filter(Ad.posted == False)

    ad = ads[ad_index]

    try:

        session.delete(ad)
        session.commit()

    except Exception as e:

        logging.error(e)

        await bot.edit_message_text('Что-то не получилось',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id)

        await show_ad(callback_query.from_user.id, ad_index - 1)

    else:

        await bot.edit_message_text(f'Это объявление успешно отклонено',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=my_admins_kb(callback_query.from_user.id))

        await show_ad(callback_query.from_user.id, ad_index - 1)

        try:

            await bot.send_message(ad.user_id, f'Администратор отклонил вашу запись с товаром {ad.product_name}')

        except Exception as e:

            logging.info(e)


async def cancel_delete_ad(callback_query: CallbackQuery):
    await callback_query.answer()

    await bot.edit_message_text(f'Объявление цело и невредимо',
                                callback_query.from_user.id,
                                callback_query.message.message_id)
