from aiogram import types

# noinspection PyProtectedMember
from ad_utils.add_ad import ad_start
from ad_utils.ads import send_user_ads
from admin import my_admins_text, my_admins_kb, admin_menu_profile, show_ad, not_access, add_admin_text
from datatypes import User
from loader import session
from markups import mainMenu

# import logging


async def all_messages(message: types.Message):
    if message.chat.type == 'private':
        user = session.query(User).filter(User.user_id == message.from_user.id).first()
        is_admin = user.is_admin if user else False
        match message.text:
            case 'Добавить админа':
                if not is_admin:
                    return await not_access(message.from_user.id)
                return await message.answer(add_admin_text(message.from_user.id))
            case 'Мои админы':
                if not is_admin:
                    return await not_access(message.from_user.id)
                return await message.answer(my_admins_text(message.chat.id), reply_markup=my_admins_kb(message.from_user.id))
            case 'Управление админами':
                if not is_admin:
                    return await not_access(message.from_user.id)
                return await message.answer('Управление:', reply_markup=admin_menu_profile())
            case 'Управление объявлениями':
                if not is_admin:
                    return await not_access(message.from_user.id)
                return await show_ad(message.from_user.id)
            case "Мои объявления":
                return await send_user_ads(message)
            case "Добавить объявление":
                return await ad_start(message)
            case 'Назад' | 'Отмена':
                return await message.answer('Вы вернулись назад', reply_markup=mainMenu(message.from_user.id))
            case _:
                return await message.answer('Я тебя не понял', reply_markup=mainMenu(message.from_user.id))
