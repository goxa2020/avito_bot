from aiogram import types
from markups import mainMenu
from loader import dp, db
from admin import *
from add_ad import ad_start
# import logging


@dp.message_handler(content_types=['text'])
async def all_messages(message: types.Message):
    # if message.chat.type == 'supergroup':
    #     pass
    if message.chat.type == 'private':
        is_admin = db.user_is_admin(message.from_user.id)
        if message.text == 'Добавить админа':
            if is_admin:
                await admin_ref(message)
            else:
                await message.answer('Вы не имеете доступа к этой команде')
        elif message.text == 'Мои админы':
            if is_admin:
                await message.answer(my_admins_text(message.chat.id), reply_markup=my_admins_kb(message.from_user.id))
            else:
                await message.answer('У вас нет доступа к этой команде', reply_markup=mainMenu(message.from_user.id))
        elif message.text == 'Управление админами':
            if is_admin:
                await message.answer('Управление:', reply_markup=adminMenuProfile())
            else:
                await message.answer('У вас нет доступа к этой команде', reply_markup=mainMenu(message.from_user.id))
        elif message.text == 'Управление объявлениями':
            if is_admin:
                await show_ad(message.from_user.id)
            else:
                await message.answer('У вас нет доступа к этой команде', reply_markup=mainMenu(message.from_user.id))
        elif message.text == "Назад" or message.text == "Отмена":
            await message.answer('Вы вернулись назад', reply_markup=mainMenu(message.from_user.id))
        elif message.text == "Добавить объявление":
            await ad_start(message)
        else:
            await message.answer('Я тебя не понял', reply_markup=mainMenu(message.from_user.id))
