import logging

from aiogram import types

from datatypes import User
from loader import session, bot
from markups import mainMenu


async def start_message(message: types.Message):
    if message.chat.type == 'private':
        admin_invited = ('adm' in message.text)
        admin_invite = (message.text.split()[1][:2:-1] if admin_invited else False)
        user = session.query(User).filter(User.user_id == message.from_user.id).first()
        is_admin = user.is_admin if user else False
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
                        user = session.query(User).filter(User.user_id == message.from_user.id).first()
                        if user:
                            user.is_admin = True
                            user.admin_inviter_id = admin_invite
                        else:
                            user = User(user_id=message.from_user.id, user_first_name=message.from_user.first_name,
                                        user_link=message.from_user.url, is_admin=True, admin_inviter_id=admin_invite)
                            session.add(user)
                        session.commit()
                    except Exception as e:
                        logging.warning(e)
                    else:
                        logging.info(
                            f'У нас новый админ, ID: {message.from_user.id}, имя: {message.from_user.first_name}')
                        await message.answer('Поздравляю, теперь вы админ', reply_markup=mainMenu(message.from_user.id))
        elif session.query(User).filter(User.user_id == message.from_user.id).first():
            await message.answer('Давно не виделись', reply_markup=mainMenu(message.from_user.id))
        else:
            await message.answer('Привет, приятно познакомиться\n'
                                 'Я бот для добавления объявлений на канал',
                                 reply_markup=mainMenu(message.from_user.id))
            user = User(user_id=message.from_user.id, user_first_name=message.from_user.first_name, is_admin=False)
            session.add(user)
            session.commit()
