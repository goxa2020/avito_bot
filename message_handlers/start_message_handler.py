import logging

from aiogram import types

from loader import db, bot
from markups import mainMenu


async def start_message(message: types.Message):
    if message.chat.type == 'private':
        admin_invited = ('adm' in message.text)
        admin_invite = (message.text.split()[1][:2:-1] if admin_invited else False)
        is_admin = db.user_is_admin(message.from_user.id)
        if admin_invited:
            if is_admin:
                await message.answer('Вы и так уже админ', reply_markup=mainMenu(message.from_user.id))
            else:
                try:
                    await bot.send_message(admin_invite, f'Через вашу ссылку человек '
                                                         f'({message.from_user.first_name}) получил права админа')
                except Exception as e:
                    logging.error(e)
                else:
                    try:
                        db.add_admin(message.from_user.id, admin_invite, message.from_user.first_name)
                    except Exception as e:
                        logging.warning(e)
                    else:
                        logging.info(f'У нас новый админ, ID: {message.from_user.id}, имя: {message.from_user.first_name}')
                        await message.answer('Поздравляю, теперь вы админ', reply_markup=mainMenu(message.from_user.id))
        elif db.user_exists(message.from_user.id):
            await message.answer('Давно не виделись', reply_markup=mainMenu(message.from_user.id))
        else:
            await message.answer('Привет, приятно познакомиться\n'
                                 'Я бот для добавления объявлений на канал',
                                 reply_markup=mainMenu(message.from_user.id))
            db.add_user(message.from_user.id)
