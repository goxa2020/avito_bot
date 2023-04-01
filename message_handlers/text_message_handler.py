from aiogram import types

from ad_utils.add_ad import ad_start
from ad_utils.ads import send_user_ads
from admin import my_admins_text, my_admins_kb, admin_menu_profile, show_ad
from config import Bot_name
from loader import db
from markups import mainMenu


# import logging


async def all_messages(message: types.Message):
    # if message.chat.type == 'supergroup':
    #     pass
    if message.chat.type == 'private':
        is_admin = db.user_is_admin(message.from_user.id)
        if message.text == 'Добавить админа':
            if is_admin:
                await message.answer(f'Твоя ссылка для назначения админа⬇\n'
                                     f'https://t.me/{Bot_name}?start=adm{str(message.from_user.id)[::-1]}\n'
                                     f'Человек должен перейти по ней и нажать "Старт", чтобы стать админом\n'
                                     f'Будь осторожен, не передовай эту ссылку неизвестным людям')
            else:
                await message.answer('Вы не имеете доступа к этой команде')
        elif message.text == 'Мои админы':
            if is_admin:
                await message.answer(my_admins_text(message.chat.id), reply_markup=my_admins_kb(message.from_user.id))
            else:
                await message.answer('У вас нет доступа к этой команде', reply_markup=mainMenu(message.from_user.id))
        elif message.text == 'Управление админами':
            if is_admin:
                await message.answer('Управление:', reply_markup=admin_menu_profile())
            else:
                await message.answer('У вас нет доступа к этой команде', reply_markup=mainMenu(message.from_user.id))
        elif message.text == 'Управление объявлениями':
            if is_admin:
                await show_ad(message.from_user.id)
            else:
                await message.answer('У вас нет доступа к этой команде', reply_markup=mainMenu(message.from_user.id))
        elif message.text == "Назад" or message.text == "Отмена":
            await message.answer('Вы вернулись назад', reply_markup=mainMenu(message.from_user.id))
        elif message.text == "Мои объявления":
            await send_user_ads(message)
        elif message.text == "Добавить объявление":
            await ad_start(message)
        else:
            await message.answer('Я тебя не понял', reply_markup=mainMenu(message.from_user.id))
