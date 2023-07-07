from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from admin import my_admins_text, my_admins_kb
from datatypes import User
from loader import bot, session
import logging


async def delete_admin(callback_query: types.CallbackQuery):
    await callback_query.answer()

    del_id = callback_query.data.split("_")[1]
    admin_name = session.query(User).filter(User.is_admin and User.user_id == del_id).first().user_first_name

    inline_kb = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton(f'Подтвердить', callback_data=f'confirmCallDelAdm_{del_id}')
    inline_btn2 = InlineKeyboardButton(f'Отмена', callback_data=f'cancelCallDelAdm_{del_id}')
    inline_kb.add(inline_btn1).add(inline_btn2)

    await bot.edit_message_text(f'Точно удалить {admin_name}', callback_query.from_user.id,
                                callback_query.message.message_id, reply_markup=inline_kb)


async def confirm_delete_admin(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    del_id = callback_query.data.split("_")[1]
    try:
        if session.query(User).filter(User.user_id == del_id).first().is_admin:
            admin = session.query(User).filter(User.user_id == del_id).first()
            admin.is_admin = False
            admin.admin_inviter_id = None
            session.commit()
    except Exception as e:
        logging.error(e)
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
            logging.info(f'Не получилось написать удалённому админу, {e}')


async def cancel_delete_admin(callback_query: types.CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id

    await bot.edit_message_text(f'Действие отменено \n{my_admins_text(user_id)}',
                                callback_query.from_user.id,
                                callback_query.message.message_id,
                                reply_markup=my_admins_kb(user_id))
