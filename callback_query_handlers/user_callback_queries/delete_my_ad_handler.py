import logging

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from callback_query_handlers.user_callback_queries.show_ad_to_user import show_ad_to_user
from config import chanel_name
from datatypes import Ad, User
from loader import bot, session


async def delete_users_ad(callback_query: CallbackQuery):
    await callback_query.answer()

    ad_index = int(callback_query.data.split("_")[1])

    confirm_del_ad_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    inline_btn1 = InlineKeyboardButton(text=f'Подтвердить', callback_data=f'confirmDeleteUsersAd_{ad_index}')
    inline_btn2 = InlineKeyboardButton(text=f'Отмена', callback_data=f'cancelDelAd')
    confirm_del_ad_keyboard.inline_keyboard.extend([[inline_btn1], [inline_btn2]])

    return await bot.send_message(callback_query.from_user.id, 'Точно удалить это объявление',
                                  reply_markup=confirm_del_ad_keyboard)


async def confirm_delete_users_ad(callback_query: CallbackQuery):
    await callback_query.answer()
    ad_index = int(callback_query.data.split("_")[1])
    user = session.query(User).filter(User.user_id == callback_query.from_user.id).first()
    ads = session.query(Ad).filter(Ad.owner == user)
    ad = ads[ad_index]

    try:

        if ad.posted:
            await bot.delete_message(chanel_name, ad.post_id)

    except Exception as e:

        logging.error(e)

        await bot.edit_message_text('Что-то не получилось',
                                    callback_query.from_user.id,
                                    callback_query.message.message_id)

    else:

        try:
            session.delete(ad)
            session.commit()

        except Exception as e:

            logging.error(e)

            await bot.edit_message_text('Что-то не получилось',
                                        callback_query.from_user.id,
                                        callback_query.message.message_id)

        else:

            await bot.edit_message_text(f'Это объявление успешно удалено',
                                        callback_query.from_user.id,
                                        callback_query.message.message_id,
                                        reply_markup=None)

    finally:

        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id-1)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id-2)

        await show_ad_to_user(callback_query.from_user.id, ad_index - 1, True)
