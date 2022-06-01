from loader import dp, db, bot
from aiogram import types
from markups import *
from admin import *
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