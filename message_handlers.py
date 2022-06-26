import aiogram.utils.exceptions
from loader import dp, db, bot
from aiogram import types
from markups import *
from admin import *
from add_ad import ad_start
import logging


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if message.chat.type == 'private':
        admin_invited = (True if 'adm' in message.text else False)
        admin_invite = (message.text.split()[1][:2:-1] if admin_invited else False)
        is_admin = db.user_is_admin(message.from_user.id)
        if admin_invited:
            if is_admin:
                await message.answer('Вы и так уже админ', reply_markup=mainMenu(message.from_user.id))
            else:
                try:
                    await bot.send_message(admin_invite, f'Через вашу ссылку человек '
                                                         f'({message.from_user.first_name}) получил права админа')
                except aiogram.utils.exceptions.ChatNotFound:
                    message.answer('Что-то не получилось, попробуйте позже')
                else:
                    try:
                        db.add_admin(message.from_user.id, admin_invite, message.from_user.first_name)
                    except Exception as e:
                        logging.warning(e)
                await message.answer('Поздравляю, теперь вы админ', reply_markup=mainMenu(message.from_user.id))
        elif db.user_exists(message.from_user.id):
            await message.answer('Давно не виделись', reply_markup=mainMenu(message.from_user.id))
        else:
            await message.answer('Привет, приятно познакомиться\n'
                                 'Я бот для добавления объявлений на канал',
                                 reply_markup=mainMenu(message.from_user.id))
            db.add_user(message.from_user.id)


@dp.message_handler(commands=['help'])
async def start_message(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Эта функция на стадии разработки')


@dp.message_handler(content_types=['text'])
async def all_messages(message: types.Message):
    if message.chat.type == 'private':
        is_admin = db.user_is_admin(message.from_user.id)
        if message.text == 'Добавить админа':
            if db.user_is_admin(message.from_user.id):
                await admin_ref(message)
            else:
                await message.answer('Вы не имеете доступа к этой команде')
        elif message.text == 'Мои админы':
            if is_admin:
                await bot.send_message(message.from_user.id, my_admins_text(message.from_user.id),
                                       reply_markup=my_admins_kb(message.from_user.id))
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