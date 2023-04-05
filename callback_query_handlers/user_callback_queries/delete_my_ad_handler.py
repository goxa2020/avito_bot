import logging

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from callback_query_handlers.user_callback_queries.show_ad_to_user import show_ad_to_user
from config import chanel_id
from loader import db, bot


async def delete_users_ad(callback_query: CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split("_")[1])

    confirm_del_ad_keyboard = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton(f'Подтвердить', callback_data=f'confirmDeleteUsersAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton(f'Отмена', callback_data=f'cancelDelAd')
    confirm_del_ad_keyboard.add(inline_btn1).add(inline_btn2)

    return await bot.send_message(callback_query.from_user.id, 'Точно удалить это объявление',
                                  reply_markup=confirm_del_ad_keyboard)


async def confirm_delete_users_ad(callback_query: CallbackQuery):
    await callback_query.answer()
    ad_index = int(callback_query.data.split("_")[1])
    ads = db.get_user_ads(callback_query.from_user.id)
    ad = ads[ad_index]

    try:

        db.del_ad(ad[0])

        if ad[10]:
            await bot.delete_message(chanel_id, ad[9])

    except Exception as e:

        logging.error(e)

        await bot.edit_message_text('Что-то не получилось',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id)

        await show_ad_to_user(callback_query.from_user.id, ad_index - 1, True)

    else:

        await bot.edit_message_text(f'Это объявление успешно удалено',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=None)

        await show_ad_to_user(callback_query.from_user.id, ad_index - 1, True)
